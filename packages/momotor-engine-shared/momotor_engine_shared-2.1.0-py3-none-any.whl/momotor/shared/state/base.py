from abc import ABC, abstractmethod
from contextlib import asynccontextmanager


class StateABC(ABC):
    """ Abstract base class to implement shared locks
    """
    @asynccontextmanager  # type: ignore
    @abstractmethod
    async def get_lock(self, key: str, *, exclusive: bool = True):
        """ Context manager to get a lock. The lock is held while the context is active.

        The lock is an 'exclusive' or 'read/write' lock:

        * Many processes can hold the lock when `exclusive` is ``False`` (*read* mode), but
        * Only one process can hold the lock when `exclusive` is ``True`` (*write* mode).
          No other processes can hold the lock while one process has it locked exclusively.

        :param key: global name for the lock
        :param exclusive: get an exclusive lock
        :return:
        :raises: :py:class:`~momotor.shared.state.LockFailed`
        """
        ...

    @abstractmethod
    async def test_lock(self, key: str, *, exclusive: bool = True) -> bool:
        """ Test the lock. Returns ``True`` if the lock is currently not being held.

        Not that this is very transient information. The lock could be acquired immediately after this method
        returns.

        :param key: global name for the lock
        :param exclusive: get an exclusive lock
        :return:
        """
        ...
