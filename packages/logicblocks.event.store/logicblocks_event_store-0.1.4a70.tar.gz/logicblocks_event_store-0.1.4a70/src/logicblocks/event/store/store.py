import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence, Set
from typing import Any

import structlog
from structlog.typing import FilteringBoundLogger

from logicblocks.event.store.adapters import EventStorageAdapter
from logicblocks.event.store.conditions import WriteCondition
from logicblocks.event.store.constraints import QueryConstraint
from logicblocks.event.store.exceptions import UnmetWriteConditionError
from logicblocks.event.types import (
    CategoryIdentifier,
    EventSourceIdentifier,
    NewEvent,
    StoredEvent,
    StreamIdentifier,
)

_default_logger = structlog.get_logger("logicblocks.event.store")


class EventSource[I: EventSourceIdentifier](ABC):
    @property
    @abstractmethod
    def identifier(self) -> I:
        raise NotImplementedError()

    @abstractmethod
    async def latest(self) -> StoredEvent | None:
        pass

    async def read(
        self,
        *,
        constraints: Set[QueryConstraint] = frozenset(),
    ) -> Sequence[StoredEvent]:
        return [event async for event in self.iterate(constraints=constraints)]

    @abstractmethod
    def iterate(
        self, *, constraints: Set[QueryConstraint] = frozenset()
    ) -> AsyncIterator[StoredEvent]:
        raise NotImplementedError()

    def __aiter__(self) -> AsyncIterator[StoredEvent]:
        return self.iterate()


class EventStream(EventSource[StreamIdentifier]):
    """A class for interacting with a specific stream of events.

    Events can be published into the stream using the `publish` method, and
    the entire stream can be read using the `read` method. Streams are also
    iterable, supporting `aiter`.
    """

    def __init__(
        self,
        adapter: EventStorageAdapter,
        stream: StreamIdentifier,
        logger: FilteringBoundLogger = _default_logger,
    ):
        self._adapter = adapter
        self._logger = logger.bind(
            category=stream.category, stream=stream.stream
        )
        self._identifier = stream

    @property
    def identifier(self) -> StreamIdentifier:
        return self._identifier

    async def latest(self) -> StoredEvent | None:
        await self._logger.adebug("event.stream.reading-latest")
        return await self._adapter.latest(target=self._identifier)

    async def publish(
        self,
        *,
        events: Sequence[NewEvent],
        conditions: Set[WriteCondition] = frozenset(),
    ) -> Sequence[StoredEvent]:
        """Publish a sequence of events into the stream."""
        await self._logger.adebug(
            "event.stream.publishing",
            category=self._identifier.category,
            stream=self._identifier.stream,
            events=[event.dict() for event in events],
            conditions=conditions,
        )

        try:
            stored_events = await self._adapter.save(
                target=self._identifier,
                events=events,
                conditions=conditions,
            )

            if self._logger.is_enabled_for(logging.DEBUG):
                await self._logger.ainfo(
                    "event.stream.published",
                    events=[event.dict() for event in stored_events],
                )
            else:
                await self._logger.ainfo(
                    "event.stream.published",
                    events=[event.envelope() for event in stored_events],
                )

            return stored_events
        except UnmetWriteConditionError as ex:
            await self._logger.awarn(
                "event.stream.publish-failed",
                category=self._identifier.category,
                stream=self._identifier.stream,
                events=[event.envelope() for event in events],
                reason=repr(ex),
            )
            raise

    def iterate(
        self, *, constraints: Set[QueryConstraint] = frozenset()
    ) -> AsyncIterator[StoredEvent]:
        """Iterate over the events in the stream.

        Args:
            constraints: A set of query constraints defining which events to
                   include in the iteration

        Returns:
            an async iterator over the events in the stream.
        """
        self._logger.debug(
            "event.stream.iterating", constraints=list(constraints)
        )

        return self._adapter.scan(
            target=self._identifier,
            constraints=constraints,
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EventStream):
            return NotImplemented
        return (
            self._adapter == other._adapter
            and self._identifier == other._identifier
        )


class EventCategory(EventSource[CategoryIdentifier]):
    """A class for interacting with a specific category of events.

    Since a category consists of zero or more streams, the category
    can be narrowed to a specific stream using the `stream` method.

    Events in the category can be read using the `read` method. Categories are
    also iterable, supporting `iter`.
    """

    def __init__(
        self,
        adapter: EventStorageAdapter,
        category: CategoryIdentifier,
        logger: FilteringBoundLogger = _default_logger,
    ):
        self._adapter = adapter
        self._logger = logger.bind(category=category.category)
        self._identifier = category

    @property
    def identifier(self) -> CategoryIdentifier:
        return self._identifier

    async def latest(self) -> StoredEvent | None:
        await self._logger.adebug("event.category.reading-latest")
        return await self._adapter.latest(target=self._identifier)

    def stream(self, *, stream: str) -> EventStream:
        """Get a stream of events in the category.

        Args:
            stream (str): The name of the stream.

        Returns:
            an event store scoped to the specified stream.
        """
        return EventStream(
            adapter=self._adapter,
            logger=self._logger,
            stream=StreamIdentifier(
                category=self._identifier.category, stream=stream
            ),
        )

    def iterate(
        self, *, constraints: Set[QueryConstraint] = frozenset()
    ) -> AsyncIterator[StoredEvent]:
        """Iterate over the events in the category.

        Args:
            constraints: A set of query constraints defining which events to
                   include in the iteration

        Returns:
            an async iterator over the events in the category.
        """
        self._logger.debug(
            "event.category.iterating", constraints=list(constraints)
        )
        return self._adapter.scan(
            target=self._identifier,
            constraints=constraints,
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EventCategory):
            return NotImplemented
        return (
            self._adapter == other._adapter
            and self._identifier == other._identifier
        )


class EventStore:
    """The primary interface into the store of events.

    An [`EventStore`][logicblocks.event.store.EventStore] is backed by a
    [`EventStorageAdapter`][logicblocks.event.store.adapters.EventStorageAdapter]
    which implements event storage. Typically, events are stored in an immutable
    append only log, the details of which are storage implementation specific.

    The event store is partitioned into _streams_, a sequence of events relating
    to the same "thing", such as an entity, a process or a state machine, and
    _categories_, a logical grouping of streams that share some characteristics.

    For example, a stream might exist for each order in a commerce system, with
    the category of such streams being "orders".

    Streams and categories are each identified by a string name. The combination
    of a category name and a stream name acts as an identifier for a specific
    stream of events.
    """

    def __init__(
        self,
        adapter: EventStorageAdapter,
        logger: FilteringBoundLogger = _default_logger,
    ):
        self._adapter = adapter
        self._logger = logger

    def stream(self, *, category: str, stream: str) -> EventStream:
        """Get a stream of events from the store.

        This method alone doesn't result in any IO, it instead returns a scoped
        event store for the stream identified by the category and stream names,
        as part of a fluent interface.

        Categories and streams implicitly exist, i.e., calling this method for a
        category or stream that has never been written to will not result in an
        error.

        Args:
            category (str): The name of the category of the stream.
            stream (str): The name of the stream.

        Returns:
            an event store scoped to the specified stream.
        """
        return EventStream(
            adapter=self._adapter,
            logger=self._logger,
            stream=StreamIdentifier(category=category, stream=stream),
        )

    def category(self, *, category: str) -> EventCategory:
        """Get a category of events from the store.

        This method alone doesn't result in any IO, it instead returns a scoped
        event store for the category identified by the category name,
        as part of a fluent interface.

        Categories implicitly exist, i.e., calling this method for a category
        that has never been written to will not result in an error.

        Args:
            category (str): The name of the category.

        Returns:
            an event store scoped to the specified category.
        """
        return EventCategory(
            adapter=self._adapter,
            logger=self._logger,
            category=CategoryIdentifier(category=category),
        )
