from twat_mp.__version__ import version as __version__
from twat_mp.mp import MultiPool, ProcessPool, ThreadPool, amap, imap, mmap, pmap

__all__ = [
    "MultiPool",
    "ProcessPool",
    "ThreadPool",
    "__version__",
    "amap",
    "imap",
    "mmap",
    "pmap",
]
