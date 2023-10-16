from contextlib import contextmanager


class FakePage:

    def screenshot(self, full_page: bool) -> str:
        return 'some_bytes_that_represent_a_screenshot'


class FakePageInspector:

    @contextmanager
    def load_page(self, url: str):
        yield FakePage()
