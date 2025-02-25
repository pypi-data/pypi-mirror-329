import threading

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._condition = threading.Condition()

    def acquire_read(self):
        with self._condition:
            while self._writer:
                self._condition.wait()
            self._readers += 1

    def release_read(self):
        with self._condition:
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write(self):
        with self._condition:
            while self._writer or self._readers > 0:
                self._condition.wait()
            self._writer = True

    def release_write(self):
        with self._condition:
            self._writer = False
            self._condition.notify_all()
