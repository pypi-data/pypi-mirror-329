import odoorpc
from types import MethodType, FunctionType, CoroutineType
from typing import Coroutine, List, Callable, Any, Dict
import inspect
from functools import wraps, partial
from .types import *
from inspect import Parameter, Signature
from concurrent.futures import ThreadPoolExecutor
import asyncio
import sys
import logging
import threading

logger = logging.getLogger(__name__)

def create_odoo_function(func, client):
    """Create a function that can operate in both sync and async contexts."""

    # Create the core function that will be returned
    def odoo_function(*args, **kwargs):
        # Get the calling frame
        frame = sys._getframe(1)
        while frame:
            if frame.f_code.co_flags & inspect.CO_COROUTINE:
                # We're in an async context - return a coroutine
                async def async_impl():
                    return await client._run_in_executor(func, client, *args, **kwargs)
                return async_impl()
            frame = frame.f_back

        # We're in a sync context - run directly
        return func(client, *args, **kwargs)

    # Copy function metadata
    odoo_function.__name__ = func.__name__
    odoo_function.__doc__ = func.__doc__
    odoo_function.__module__ = func.__module__
    odoo_function.__qualname__ = func.__qualname__
    odoo_function.__annotations__ = getattr(func, '__annotations__', {})

    # Create correct signature without 'self'
    sig = inspect.signature(func)
    odoo_function.__signature__ = Signature(
        parameters=list(sig.parameters.values())[1:],
    )


    return odoo_function

class OdooQuery:
    def __init__(self, db_url, db_name, username, password, max_workers: int = 10):
        self.db_url = db_url
        self.db_name = db_name
        self.username = username
        self.password = password
        self.connection = None
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="odoo_query_worker"
        )
        self._executor_semaphore = asyncio.Semaphore(max_workers)
        self.loop = asyncio.get_event_loop()
        self._functions = {}  # Store function references

    def connect(self):
        """Connect to Odoo server using JSONRPC over SSL."""
        try:
            logger.info("Connecting to Odoo server...")
            self.connection = odoorpc.ODOO(self.db_url, protocol='jsonrpc+ssl', port=443)
            self.connection.login(self.db_name, self.username, self.password)
            logger.info("Successfully connected to Odoo")
        except Exception as e:
            logger.error(f"Failed to connect to Odoo: {e}", exc_info=True)

    async def _run_in_executor(self, func, *args, **kwargs):
        """Run a synchronous function in the thread pool executor with timeout."""
        async with self._executor_semaphore:
            logger.debug(f"Submitting {func.__name__} to executor")
            try:
                future = self.loop.run_in_executor(
                    self.executor,
                    lambda: self._wrapped_execution(func, *args, **kwargs)
                )
                result = await asyncio.wait_for(future, timeout=30.0)  # 30 second timeout
                logger.debug(f"Executor completed {func.__name__}")
                return result
            except asyncio.TimeoutError:
                logger.error(f"Timeout executing {func.__name__}")
                raise
            except Exception as e:
                logger.error(f"Error in executor for {func.__name__}: {e}", exc_info=True)
                raise

    def _wrapped_execution(self, func, *args, **kwargs):
        """Wrapper to catch and log exceptions in thread pool."""
        thread_name = threading.current_thread().name
        logger.debug(f"[{thread_name}] Starting execution of {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"[{thread_name}] Completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"[{thread_name}] Error in {func.__name__}: {e}", exc_info=True)
            raise

    async def execute_functions(self, function_calls: List[Dict[str, Any]]) -> []:
        """Execute multiple functions in parallel."""
        tasks = []
        for call in function_calls:
            func_name = call['name']
            kwargs = call.get('kwargs', {})

            if func_name in self._functions:
                func = getattr(self, func_name)
                # The descriptor will automatically handle async execution
                tasks.append(func(**kwargs))
            else:
                raise ValueError(f"Function {func_name} not found")

        return await asyncio.gather(*tasks)

    def execute_functions_sync(self, function_calls: List[Dict[str, Any]]) -> []:
        """Synchronous wrapper for execute_functions."""
        return asyncio.run(self.execute_functions(function_calls))

    def disconnect(self):
        """Safely disconnect from Odoo server."""
        if self.connection:
            try:
                self.connection.logout()
            except:
                pass  # Ignore errors during logout
            finally:
                self.connection = None
        self.executor.shutdown(wait=True)

    def functions(self):
        """Return list of callable functions."""
        return list(self._functions.values())

    def add_functions(self, *modules):
        """Add functions from modules."""
        for module in modules:
            for name, func in module.__dict__.items():
                if inspect.isfunction(func) and not name.startswith('_'):
                    annotations = getattr(func, '__annotations__', {})
                    if not annotations:
                        continue

                    # Create function and bind it to the instance
                    bound_func = create_odoo_function(func, self)
                    setattr(self, name, bound_func)
                    self._functions[name] = bound_func