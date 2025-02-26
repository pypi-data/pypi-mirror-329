import asyncio
import functools
import inspect
import signal
import sys
import threading
import time
import typing
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from contextvars import ContextVar, copy_context
from functools import partial, wraps
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)
from uuid import UUID, uuid4

import anyio
import anyio.abc
import anyio.from_thread
import anyio.to_thread
import nest_asyncio
import sniffio
import tqdm
from loguru import logger
from typing_extensions import Literal, ParamSpec, TypeGuard

# import threading

# from prefect.logging import get_logger

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])
Async = Literal[True]
Sync = Literal[False]
A = TypeVar("A", Async, Sync, covariant=True)

# Global references to prevent garbage collection for `add_event_loop_shutdown_callback`
EVENT_LOOP_GC_REFS = {}

GLOBAL_THREAD_LIMITER: Optional[anyio.CapacityLimiter] = None

RUNNING_IN_RUN_SYNC_LOOP_FLAG = ContextVar("running_in_run_sync_loop", default=False)
RUNNING_ASYNC_FLAG = ContextVar("run_async", default=False)
BACKGROUND_TASKS: set[asyncio.Task] = set()
background_task_lock = threading.Lock()

# Thread-local storage to keep track of worker thread state
_thread_local = threading.local()


def get_thread_limiter():
    global GLOBAL_THREAD_LIMITER

    if GLOBAL_THREAD_LIMITER is None:
        GLOBAL_THREAD_LIMITER = anyio.CapacityLimiter(250)

    return GLOBAL_THREAD_LIMITER


def is_async_fn(
    func: Union[Callable[P, R], Callable[P, Awaitable[R]]],
) -> TypeGuard[Callable[P, Awaitable[R]]]:
    """
    Returns `True` if a function returns a coroutine.

    See https://github.com/microsoft/pyright/issues/2142 for an example use
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.iscoroutinefunction(func)


def is_async_gen_fn(func):
    """
    Returns `True` if a function is an async generator.
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.isasyncgenfunction(func)


def create_task(coroutine: Coroutine) -> asyncio.Task:
    """
    Replacement for asyncio.create_task that will ensure that tasks aren't
    garbage collected before they complete. Allows for "fire and forget"
    behavior in which tasks can be created and the application can move on.
    Tasks can also be awaited normally.

    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
    for details (and essentially this implementation)
    """

    task = asyncio.create_task(coroutine)

    # Add task to the set. This creates a strong reference.
    # Take a lock because this might be done from multiple threads.
    with background_task_lock:
        BACKGROUND_TASKS.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(BACKGROUND_TASKS.discard)

    return task


def cancel_background_tasks() -> None:
    """
    Cancels all background tasks stored in BACKGROUND_TASKS.
    """
    with background_task_lock:
        tasks = list(BACKGROUND_TASKS)
    for task in tasks:
        task.cancel()


def run_async(coroutine):
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If there's no current event loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Check if we're in a Jupyter notebook
    if "IPython" in sys.modules:
        # If so, apply nest_asyncio to allow nested use of event loops
        nest_asyncio.apply()

    # Now we can safely run our coroutine
    return loop.run_until_complete(coroutine)


async def _async_generator_timeout(async_gen, timeout):
    try:
        while True:
            try:
                item = await asyncio.wait_for(async_gen.__anext__(), timeout)
                yield item
            except StopAsyncIteration:
                break
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(
            "Generator didn't emit a new item within the specified timeout"
        )


T = TypeVar("T")

global_stop = threading.Event()


@overload
def async_iterator(
    func: Callable[..., AsyncIterator[T]],
) -> Callable[..., AsyncIterator[T]]: ...


@overload
def async_iterator(
    func: None = None, iteration_timeout: float | None = None
) -> Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]: ...


def async_iterator(
    func: Callable[..., AsyncIterator[T]] | None = None,
    iteration_timeout: float | None = None,
    use_global_stop: bool = False,
) -> (
    Callable[..., AsyncIterator[T]]
    | Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]
):
    def inner(
        async_iter_func: Callable[..., AsyncIterator[T]],
    ) -> Callable[..., AsyncIterator[T]]:
        @functools.wraps(async_iter_func)
        async def wrapper(*args, **kwargs) -> AsyncIterator[T]:
            stop_event = asyncio.Event() if not use_global_stop else global_stop
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, stop_event.set)
            try:
                if iteration_timeout is not None:
                    async_gen = _async_generator_timeout(
                        async_iter_func(*args, **kwargs), iteration_timeout
                    )
                else:
                    async_gen = async_iter_func(*args, **kwargs)

                async for item in async_gen:
                    if stop_event.is_set():
                        break
                    yield item
                    await asyncio.sleep(0)
            except (KeyboardInterrupt, asyncio.CancelledError):
                # logger.debug("Received interrupt signal")
                stop_event.set()
                raise
            # except* Exception as e:
            #     for exc in e.exceptions:
            #         logger.error(exc)
            finally:
                # logger.info("Cleaning up...")
                loop.remove_signal_handler(signal.SIGINT)
                return

        return wrapper

    if func is not None:
        return inner(func)

    return inner


class FunctionWithStop(Callable):
    global_stop: asyncio.Event

    def __call__(self) -> None: ...


if TYPE_CHECKING:
    async_iterator: FunctionWithStop

setattr(async_iterator, "global_stop", global_stop)


T = TypeVar("T")


async def handle_signals(scope: anyio.abc.CancelScope):
    async with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
        async for signum in signals:
            print(f"Received signal: {signum}")
            scope.cancel()  # This cancels th


async def _run_with(
    fn: Callable[..., Awaitable[T]], idx: int, _stop: asyncio.Event, **kwargs
) -> tuple[int, T]:
    if _stop.is_set():
        return idx, None
    return idx, await fn(**kwargs)


async def map_as_completed(
    fn: Callable[..., Awaitable[T]],
    *inputs: dict[str, Any],
    name: str = None,
    progress: bool = True,
    return_exceptions: bool = True,
    progress_position: int = 0,
) -> list[T]:
    _stop = asyncio.Event()
    output = {}
    tasks: set[asyncio.Task[tuple[int, T]]] = set()
    name = name or fn.__name__
    async with asyncio.TaskGroup() as tg:
        for idx, input in enumerate(inputs):
            task = tg.create_task(_run_with(fn, idx, _stop, **input))
            tasks.add(task)

        for result in tqdm.tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc=name,
            disable=not progress,
            position=progress_position,
        ):
            try:
                if _stop.is_set():
                    break
                idx, value = await result
                output[idx] = value
            except (asyncio.CancelledError, KeyboardInterrupt):
                _stop.set()
                raise
            except Exception as e:
                if return_exceptions:
                    output[idx] = e
                else:
                    raise e

        return list(dict(sorted(output.items(), key=lambda x: x[0])).values())


async def map_as_completed_dict(
    fn: Callable[..., Awaitable[T]],
    inputs: dict[Any, dict[str, Any]],
    name: str = None,
    progress: bool = True,
    return_exceptions: bool = True,
    progress_position: int = 0,
) -> dict[Any, T]:
    """
    Executes an async function `fn` concurrently using a dictionary of inputs.

    Each key in `inputs` identifies a task, and its value is a dictionary of keyword arguments
    that will be passed to `fn`. Results are returned as a dictionary mapping each key to its result.

    Example:
        inputs = {
            'user_1': {'user_id': 1},
            'user_2': {'user_id': 2},
        }
        results = await map_as_completed_dict(fetch_user_data, inputs)
        # results might be: {'user_1': user_data_1, 'user_2': user_data_2}
    """
    _stop = asyncio.Event()
    output: dict[Any, T] = {}
    tasks: list[asyncio.Task[tuple[Any, T]]] = []
    name = name or fn.__name__

    async def run_task(key: Any, params: dict[str, Any]) -> tuple[Any, T]:
        if _stop.is_set():
            return key, None  # or consider raising CancelledError
        return key, await fn(**params)

    async with asyncio.TaskGroup() as tg:
        for key, params in inputs.items():
            tasks.append(tg.create_task(run_task(key, params)))

    for result in tqdm.tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc=name,
        disable=not progress,
        position=progress_position,
    ):
        try:
            key, value = await result
            output[key] = value
        except (asyncio.CancelledError, KeyboardInterrupt):
            _stop.set()
            raise
        except Exception as e:
            if return_exceptions:
                output[key] = e
            else:
                raise e
    # sort final outputs by original key order
    return dict(sorted(output.items(), key=lambda x: list(inputs.keys()).index(x[0])))


async def run_with_semaphore(
    semaphore: asyncio.Semaphore,
    coro: typing.Coroutine,
):
    async with semaphore:
        return await coro


T = TypeVar("T")


def retry_async(
    retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Decorator that implements retry logic for async functions with exponential backoff.

    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == retries:
                        raise
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor

            raise last_exception

        return wrapper

    return decorator


async def gather_with_concurrency(n: int, *tasks) -> list[T]:
    """
    Run coroutines with a concurrency limit.

    Args:
        n: Maximum number of concurrent tasks
        tasks: Coroutines to run
    """
    semaphore = asyncio.Semaphore(n)

    return await asyncio.gather(
        *(run_with_semaphore(semaphore, task) for task in tasks)
    )


@asynccontextmanager
async def timeout_scope(timeout: float, cleanup: Optional[Callable] = None):
    """
    Async context manager that enforces a timeout and allows for cleanup.

    Args:
        timeout: Maximum time in seconds
        cleanup: Optional coroutine to run on timeout
    """
    try:
        async with asyncio.timeout(timeout):
            yield
    except asyncio.TimeoutError:
        if cleanup:
            await cleanup()
        raise


def ensure_async(func: Callable[..., R]) -> Callable[..., Awaitable[R]]:
    """
    Wraps a synchronous function so that it can be awaited.

    If the function is already async, it is returned unchanged.
    """
    if asyncio.iscoroutinefunction(func):
        return func

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> R:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    return async_wrapper


class AsyncBatcher:
    """
    Batches async operations and processes them together when the batch size is reached
    or timeout occurs.
    """

    def __init__(
        self,
        batch_size: int,
        processor: Callable[[Collection[T]], Awaitable[None]],
        timeout: Optional[float] = None,
    ):
        self.batch_size = batch_size
        self.processor = processor
        self.timeout = timeout
        self.batch: list[T] = []
        self.last_process_time = time.time()
        self._stop_event = asyncio.Event()
        self._timeout_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

        # Start timeout checker if timeout is specified
        if timeout is not None:
            self._timeout_task = asyncio.create_task(self._check_timeout())

    async def add(self, item: T) -> None:
        """Add an item to the batch and process if necessary."""
        async with self._lock:
            self.batch.append(item)

            if len(self.batch) >= self.batch_size:
                await self._process_internal()

    async def _process_internal(self) -> None:
        """Internal method to process the current batch."""
        if not self.batch:
            return

        items_to_process = self.batch[:]
        self.batch = []
        self.last_process_time = time.time()

        await self.processor(items_to_process)

    async def _check_timeout(self) -> None:
        """Background task to check for timeouts."""
        while not self._stop_event.is_set():
            if self.timeout is None:
                return

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.timeout)
            except asyncio.TimeoutError:
                async with self._lock:
                    current_time = time.time()
                    if (
                        self.batch
                        and current_time - self.last_process_time >= self.timeout
                    ):
                        await self._process_internal()
                continue

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Process remaining items and cleanup on exit."""
        self._stop_event.set()

        if self._timeout_task:
            await self._timeout_task

        async with self._lock:
            await self._process_internal()


async def periodic(
    interval: float,
    func: Callable[[], Awaitable[None]],
    max_delay: Optional[float] = None,
) -> AsyncIterator[float]:
    """
    Runs a coroutine periodically and yields the actual time between runs.

    Args:
        interval: Desired interval between runs in seconds
        func: Coroutine to run
        max_delay: Maximum acceptable delay before skipping an iteration
    """
    last_run = time.time()

    while True:
        now = time.time()
        elapsed = now - last_run

        if max_delay is None or elapsed <= max_delay:
            await func()

        target_next = last_run + interval
        delay = max(0, target_next - time.time())

        if delay > 0:
            await asyncio.sleep(delay)

        actual_interval = time.time() - last_run
        last_run = time.time()

        yield actual_interval


class AsyncRateLimiter:
    """
    Rate limits async operations using the token bucket algorithm.
    """

    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate  # tokens per second
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
                self.last_update = time.time()
            else:
                self.tokens -= 1
