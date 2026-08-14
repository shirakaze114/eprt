import importlib
import sys
import tempfile
import types
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch


class FakeConnection:
    def __init__(self):
        self.print_calls = []

    def getPrinters(self):
        return {}

    def printFile(self, *args):
        self.print_calls.append(args)


class FakePage:
    def __init__(self):
        self.content = None
        self.pdf_options = None

    def set_content(self, content):
        self.content = content

    def pdf(self, **kwargs):
        self.pdf_options = kwargs
        Path(kwargs["path"]).write_bytes(b"%PDF-1.4\n")


class FakeBrowser:
    def __init__(self):
        self.page = FakePage()
        self.closed = False

    def new_page(self):
        return self.page

    def close(self):
        self.closed = True


class FakePlaywright:
    def __init__(self):
        self.browser = FakeBrowser()
        self.launch_calls = []
        self.chromium = types.SimpleNamespace(launch=self.launch)

    def launch(self, **kwargs):
        self.launch_calls.append(kwargs)
        return self.browser


class FakeFlask:
    def __init__(self, name):
        self.name = name

    def route(self, *args, **kwargs):
        def register(function):
            return function

        return register


class PrintRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cups_connection = FakeConnection()
        cups_module = types.ModuleType("cups")
        cups_module.Connection = lambda: cls.cups_connection
        sync_api_module = types.ModuleType("playwright.sync_api")
        sync_api_module.sync_playwright = lambda: None
        playwright_module = types.ModuleType("playwright")
        flask_module = types.ModuleType("flask")
        flask_module.Flask = FakeFlask
        flask_module.render_template = lambda template, **context: context["text"]
        flask_module.request = None

        with patch.dict(
            sys.modules,
            {
                "cups": cups_module,
                "flask": flask_module,
                "playwright": playwright_module,
                "playwright.sync_api": sync_api_module,
            },
        ):
            sys.modules.pop("main", None)
            cls.main = importlib.import_module("main")

    def run_print_route(self, executable_path=None, cups_queue=None):
        fake_playwright = FakePlaywright()
        environment = {}
        if executable_path:
            environment["EPRT_BROWSER_EXECUTABLE_PATH"] = executable_path
        if cups_queue:
            environment["EPRT_CUPS_QUEUE"] = cups_queue

        @contextmanager
        def fake_sync_playwright():
            yield fake_playwright

        with tempfile.TemporaryDirectory() as temporary_directory:
            with (
                patch.object(self.main, "PDF_DIRECTORY", Path(temporary_directory)),
                patch.object(self.main, "sync_playwright", fake_sync_playwright),
                patch.object(
                    self.main,
                    "request",
                    types.SimpleNamespace(
                        data=b"",
                        form={
                            "passwd": "kzkhasbigcock",
                            "author": "Author <script>",
                            "title": "Test <title>",
                            "text": "First line\nSecond line",
                        },
                        remote_addr="127.0.0.1",
                    ),
                ),
                patch.dict(
                    self.main.os.environ,
                    environment,
                    clear=not bool(executable_path or cups_queue),
                ),
            ):
                response = self.main.blowjob()

        return response, fake_playwright

    def test_print_renders_a4_pdf_and_submits_it_to_cups(self):
        response, fake_playwright = self.run_print_route()

        self.assertIn('"code":200', response)
        self.assertEqual(fake_playwright.launch_calls, [{}])
        self.assertEqual(fake_playwright.browser.page.pdf_options["format"], "A4")
        self.assertTrue(fake_playwright.browser.page.pdf_options["print_background"])
        self.assertTrue(fake_playwright.browser.page.pdf_options["prefer_css_page_size"])
        self.assertTrue(fake_playwright.browser.page.pdf_options["display_header_footer"])
        self.assertEqual(
            fake_playwright.browser.page.pdf_options["margin"],
            {"top": "3.5cm", "bottom": "2cm"},
        )
        header_template = fake_playwright.browser.page.pdf_options["header_template"]
        self.assertIn("Author &lt;script&gt;", header_template)
        self.assertIn('class="pageNumber"', header_template)
        self.assertIn('class="totalPages"', header_template)
        self.assertIn("border-bottom", header_template)
        self.assertNotIn("Author <script>", header_template)
        self.assertNotIn("IP: 127.0.0.1", header_template)
        self.assertNotIn("Test &lt;title&gt;", header_template)
        self.assertEqual(
            fake_playwright.browser.page.pdf_options["footer_template"],
            "<div></div>",
        )
        self.assertTrue(fake_playwright.browser.closed)
        self.assertIn("First line\nSecond line", fake_playwright.browser.page.content)
        self.assertEqual(self.cups_connection.print_calls[-1][0], "Brother_MFC-7860DN")
        self.assertTrue(self.cups_connection.print_calls[-1][1].endswith(".pdf"))

    def test_print_uses_configured_browser_executable_path(self):
        _, fake_playwright = self.run_print_route(
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        )

        self.assertEqual(
            fake_playwright.launch_calls,
            [
                {
                    "executable_path": (
                        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
                    )
                }
            ],
        )

    def test_print_uses_configured_cups_queue(self):
        _, _ = self.run_print_route(cups_queue="Office_Printer")
        self.assertEqual(self.cups_connection.print_calls[-1][0], "Office_Printer")


if __name__ == "__main__":
    unittest.main()
