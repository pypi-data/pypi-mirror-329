import requests
from queue import Queue

class ConnectionPool:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self._pool = Queue(maxsize=max_size)
        
    def get_session(self, host):
        if not self._pool.empty():
            return self._pool.get_nowait()
        return requests.Session()
    
    def release_session(self, session):
        if self._pool.qsize() < self.max_size:
            self._pool.put_nowait(session)
        else:
            session.close()