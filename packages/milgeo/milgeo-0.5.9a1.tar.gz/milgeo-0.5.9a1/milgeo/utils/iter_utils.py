from itertools import islice

def batched(iterable, n, *, strict=False):
    """
    batched('ABCDEFG', 3) → ABC DEF G

    Yield successive n-sized chunks from iterable.

    Args:
        iterable: The iterable to divide into batches.
        n: The size of each batch.
        strict: If True, raise ValueError if the last batch is incomplete.

    Yields:
        Tuples of size n from the iterable.

    Raises:
        ValueError: If n is less than 1 or if strict is True and the last batch is incomplete.
    """
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch