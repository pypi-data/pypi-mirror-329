import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List

class AsyncExecution:
    @staticmethod
    def run_async_tasks_in_executor(
        func: Callable[..., Any],
        *args_list: List[Any]
    ) -> List[Any]:
        """
        Run tasks asynchronously in a thread pool executor.

        :param func: The function to execute.
        :param args_list: A list of argument tuples for each function call.
        :return: A list of results from the function calls.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            with ThreadPoolExecutor() as executor:
                tasks = [
                    loop.run_in_executor(
                        executor,
                        func,
                        *args
                    )
                    for args in args_list
                ]
                return loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()
        
class FakeAsyncExecution:
    @staticmethod
    def run_async_tasks_in_executor(
        func: Callable[..., Any],
        *args_list: List[Any]
    ) -> List[Any]:
        return [func(*args) for args in args_list]