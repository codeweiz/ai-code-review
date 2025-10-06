import concurrent.futures
import threading
from typing import Optional


class ThreadPoolService:
    """线程池服务类，管理全局线程池"""

    def __init__(self):
        self._thread_pool: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._lock = threading.Lock()

    @property
    def thread_pool(self) -> concurrent.futures.ThreadPoolExecutor:
        """获取线程池"""
        if self._thread_pool is not None:
            return self._thread_pool

        with self._lock:
            if self._thread_pool is not None:
                return self._thread_pool

            # 创建线程池，设置合适的线程数
            self._thread_pool = concurrent.futures.ThreadPoolExecutor(
                max_workers=20, thread_name_prefix="GlobalPool"
            )

        return self._thread_pool

    def get_thread_pool(self) -> concurrent.futures.ThreadPoolExecutor:
        """获取线程池（保持向后兼容）"""
        return self.thread_pool

    def shutdown(self):
        """关闭线程池"""
        if self._thread_pool is not None:
            self._thread_pool.shutdown(wait=True)
            self._thread_pool = None
