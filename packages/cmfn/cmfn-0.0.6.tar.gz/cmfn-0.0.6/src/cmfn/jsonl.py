class JsonLWriter:

    def __init__(self, f):
        self.file_path = f

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def open(self):
        if file_path.endswith('.gz'):
            return gzip.open(file_path, mode + 't') if 'b' not in mode else gzip.open(file_path, mode)
        elif file_path.endswith('.bz2'):
            return bz2.open(file_path, mode + 't') if 'b' not in mode else bz2.open(file_path, mode)
        else:
            return open(file_path, mode)

    def add(self, item):
        self.f.write()

    def add_all(self, **items):
        for item in items:
            self.f.write(item)
