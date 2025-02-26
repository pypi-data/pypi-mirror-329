from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional

from loguru import logger


def get_all_with_pagination(
    get_fn: Callable, count_fn: Optional[Callable] = None, **kwargs
):
    """Convenience function to retrieve all resources from an endpoint that supports pagination.

    Args:
        get_fn (Callable): The function that retrieves a page of items.
            It must have parameters `offset` and `limit`
        count_fn (Optional[Callable]): Optional function to get total count of items.
            If provided, it will be used to optimize the number of requests.
            Must return an integer.
        **kwargs: Additional keyword arguments to pass to the `get_fn`.

    Returns:
        List: the full list of resources
    """
    limit = 50
    items = []

    # If we have a count function, use it to determine total pages
    if count_fn:
        total_count = count_fn(**kwargs)
        total_pages = (total_count + limit - 1) // limit

        logger.debug(f"Multiprocessing for a total of {total_pages} pages")
        if total_pages > 0:
            # Fetch all pages in parallel
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(get_fn, offset=offset, limit=limit, **kwargs)
                    for offset in range(0, total_pages * limit, limit)
                ]
                for future in as_completed(futures):
                    items.extend(future.result())
        return items

    # Otherwise, use the traditional sequential approach
    offset = 0
    while True:
        page = get_fn(offset=offset, limit=limit, **kwargs)
        items.extend(page)
        if len(page) < limit:
            return items
        offset = offset + limit


def collect_from_ids(ids: List[int], get_fn: Callable):
    arr = []
    for id in ids:
        resource = get_fn(id)
        arr.append(resource)
    return arr
