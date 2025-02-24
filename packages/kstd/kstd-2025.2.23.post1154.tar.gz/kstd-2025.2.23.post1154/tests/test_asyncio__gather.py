from asyncio import CancelledError, sleep

import pytest
from more_itertools import one

from kstd.asyncio import gather, gather_iterable


class CoroutineGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.finished = list[str]()
        self.cancelled = list[str]()

    async def succeeds(self, label: str, wait_ms: int) -> str:
        try:
            await sleep(wait_ms / 1000)
        except CancelledError:
            self.cancelled.append(label)
            raise

        self.finished.append(label)
        return label

    async def fails(self, label: str, wait_ms: int) -> str:
        try:
            await sleep(wait_ms / 1000)
        except CancelledError:
            self.cancelled.append(label)
            raise

        self.finished.append(label)
        raise RuntimeError(f"{label} failed")


async def test_gather_returns_tuple_of_results_when_all_are_successful() -> None:
    generator = CoroutineGenerator()

    results = await gather(
        generator.succeeds("first", 10),
        generator.succeeds("second", 20),
    )
    assert results == ("first", "second")

    assert generator.finished == ["first", "second"]
    assert generator.cancelled == []


async def test_gather_raises_exception_group__one_exception() -> None:
    generator = CoroutineGenerator()

    with pytest.raises(ExceptionGroup) as exc_info:
        _ = await gather(
            generator.succeeds("first", 10),
            generator.fails("second", 20),
            generator.fails("third", 30),
        )

    exc_group = exc_info.value
    assert isinstance(exc_group, ExceptionGroup)
    assert len(exc_group.exceptions) == 1
    exception = one(exc_group.exceptions)
    assert str(exception) == "second failed"

    assert generator.finished == ["first", "second"]
    assert generator.cancelled == ["third"]


async def test_gather_raises_exception_group__two_exceptions() -> None:
    generator = CoroutineGenerator()

    with pytest.raises(ExceptionGroup) as exc_info:
        _ = await gather(
            generator.fails("first", 10),
            generator.fails("second", 10),
        )

    exc_group = exc_info.value
    assert isinstance(exc_group, ExceptionGroup)
    assert len(exc_group.exceptions) == 2
    assert {str(exception) for exception in exc_group.exceptions} == {
        "first failed",
        "second failed",
    }

    assert generator.finished == ["first", "second"]


async def test_gather_iterable_returns_list_of_results_when_all_are_successful() -> None:
    generator = CoroutineGenerator()

    results = await gather_iterable([
        generator.succeeds("first", 10),
        generator.succeeds("second", 20),
    ])
    assert results == ["first", "second"]

    assert generator.finished == ["first", "second"]
    assert generator.cancelled == []


async def test_gather_iterable_raises_exception_group() -> None:
    generator = CoroutineGenerator()

    with pytest.raises(ExceptionGroup) as exc_info:
        _ = await gather_iterable([
            generator.succeeds("first", 10),
            generator.fails("second", 20),
            generator.fails("third", 30),
        ])

    exc_group = exc_info.value
    assert isinstance(exc_group, ExceptionGroup)
    assert len(exc_group.exceptions) == 1
    exception = one(exc_group.exceptions)
    assert str(exception) == "second failed"

    assert generator.finished == ["first", "second"]
    assert generator.cancelled == ["third"]
