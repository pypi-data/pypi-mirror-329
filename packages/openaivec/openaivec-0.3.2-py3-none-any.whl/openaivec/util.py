from concurrent.futures.thread import ThreadPoolExecutor
from itertools import chain
from typing import List, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


def split_to_minibatch(b: List[T], batch_size: int) -> List[List[T]]:
    """Splits the list into sublists of size `batch_size`."""
    return [b[i : i + batch_size] for i in range(0, len(b), batch_size)]


def map_minibatch(b: List[T], batch_size: int, f: Callable[[List[T]], List[U]]) -> List[U]:
    """
    Splits the list `b` into batches of size `batch_size` and applies the function `f` to each batch.
    The results (each a list) are then flattened into a single list.
    """
    batches = split_to_minibatch(b, batch_size)
    return list(chain.from_iterable(f(batch) for batch in batches))


def map_minibatch_parallel(b: List[T], batch_size: int, f: Callable[[List[T]], List[U]]) -> List[U]:
    """
    Splits the list `b` into batches of size `batch_size` and applies the function `f` to each batch.
    The results (each a list) are then flattened into a single list.
    This version uses parallel processing to apply the function to each batch.
    """
    batches = split_to_minibatch(b, batch_size)
    with ThreadPoolExecutor() as executor:
        results = executor.map(f, batches)
    return list(chain.from_iterable(results))


def map_unique(b: List[T], f: Callable[[List[T]], List[U]]) -> List[U]:
    """
    Applies the function `f` only once to the unique values in the list `b` (preserving their order),
    and then maps the resulting values back to match the original list.
    This avoids repeated execution of `f` for duplicate values.
    """
    # Use dict.fromkeys to remove duplicates while preserving the order
    unique_values = list(dict.fromkeys(b))
    value_to_index = {v: i for i, v in enumerate(unique_values)}
    results = f(unique_values)
    return [results[value_to_index[value]] for value in b]


def map_unique_minibatch(b: List[T], batch_size: int, f: Callable[[List[T]], List[U]]) -> List[U]:
    """
    Uses minibatch processing on the unique values of the list `b`.
    The function `f` is applied to these unique values in batches,
    and the results are mapped back to match the order of the original list.
    """
    return map_unique(b, lambda x: map_minibatch(x, batch_size, f))


def map_unique_minibatch_parallel(b: List[T], batch_size: int, f: Callable[[List[T]], List[U]]) -> List[U]:
    """
    Uses minibatch processing on the unique values of the list `b`.
    The function `f` is applied to these unique values in batches using parallel processing,
    and the results are mapped back to match the order of the original list.
    """
    return map_unique(b, lambda x: map_minibatch_parallel(x, batch_size, f))
