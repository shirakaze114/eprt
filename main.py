import cups
import datetime
from html import escape
import os
from pathlib import Path
from re import sub

from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright

conn = cups.Connection()
printers = conn.getPrinters()
PDF_DIRECTORY = Path(__file__).resolve().parent / "pdfs"

app = Flask(__name__)


def render_header_template(title, author, ip, timestamp):
    return (
        "<style>"
        "* { box-sizing: border-box; }"
        ".print-header {"
        "border-bottom: 1px solid #333;"
        "color: #111;"
        'font-family: "Sarasa UI SC", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif;'
        "margin: 0 2cm;"
        "padding-bottom: 0.35cm;"
        "}"
        ".title { font-size: 11pt; font-weight: 600; }"
        ".metadata { font-size: 8pt; margin-top: 0.15cm; }"
        "</style>"
        '<div class="print-header">'
        f'<div class="title">{escape(title)}</div>'
        f'<div class="metadata">Author: {escape(author)} | IP: {escape(ip)} | Date: {escape(timestamp)}</div>'
        "</div>"
    )


def get_printer_name():
    return os.environ.get("EPRT_CUPS_QUEUE", "Brother_MFC-7860DN")


def render_pdf(title, author, text, ip, timestamp):
    filename = sub(r'[\/:*?"<>| ]', '-', title) + f"-{author}-{timestamp}.pdf"
    output_path = PDF_DIRECTORY / filename
    PDF_DIRECTORY.mkdir(parents=True, exist_ok=True)
    document = render_template(
        "print.html",
        title=title,
        author=author,
        text=text,
        ip=ip,
        date=timestamp,
    )

    with sync_playwright() as playwright:
        executable_path = os.environ.get("EPRT_BROWSER_EXECUTABLE_PATH")
        launch_options = {}
        if executable_path:
            launch_options["executable_path"] = executable_path
        browser = playwright.chromium.launch(**launch_options)
        try:
            page = browser.new_page()
            page.set_content(document)
            page.pdf(
                path=str(output_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template=render_header_template(title, author, ip, timestamp),
                footer_template="<div></div>",
                margin={"top": "3.5cm", "bottom": "2cm"},
            )
        finally:
            browser.close()

    return filename

@app.route("/")
def index_page():
    with open("templates/index.html",mode="r",encoding="utf-8") as f:
        return f.read()

@app.route("/act/print", methods=["POST"])
def blowjob():
    if request.form.get('passwd')!="kzkhasbigcock":
        return '{"code":200, "error": "cnm"}'

    print(request.data)
    author = request.form.get('author')
    title = 'ePRT-'+request.form.get('title')
    text = request.form.get('text')
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

    filename = render_pdf(title, author, text, ip, timestamp)
    
    conn.printFile(get_printer_name(), str(PDF_DIRECTORY / filename), timestamp, {})
    return '{"code":200, "file": "'+filename+'"}'

def main():
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

if __name__ == "__main__":
    main()
