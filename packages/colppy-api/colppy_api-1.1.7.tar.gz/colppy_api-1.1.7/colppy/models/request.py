class Request:
    def __init__(self, page_size=50):
        self._page_size = page_size
        self._start = 0
        self._limit = self._page_size

    def next_page(self):
        self._start += self._page_size