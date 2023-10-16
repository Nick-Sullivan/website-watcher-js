from contextlib import contextmanager
from subprocess import call

from playwright.sync_api import sync_playwright


class PageInspector:

    @contextmanager
    def load_page(self, url: str):
        print(f'Going to {url}')
        with sync_playwright() as p:
            with p.chromium.launch(args=["--disable-gpu", "--single-process"]) as browser:
                page = browser.new_page(viewport={'width': 600, 'height': 600})
                page.goto(url)
                page.wait_for_timeout(3_000)
                yield page

        self._clear_temporary_files()

    def _clear_temporary_files(self):
        call('rm -rf /tmp/*', shell=True)
