class Disposable:
    def __init__(self, disposable):
        self.disposable = disposable

    def stop(self):
        self.disposable.Dispose()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
