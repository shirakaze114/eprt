# ePRT

A web printing system whose abbreviation is ePRT Printing & Reproduction Toolkit

## How to use

Go <http://localhost:8080/>;

Enter what u want to print;

Press the button;

Catch the papers by the printer.

## Deploy guide

Install Python, CUPS, a Chinese-capable font, and a Chromium-based browser on the server. By default ePRT uses the `Brother_MFC-7860DN` CUPS queue; set `EPRT_CUPS_QUEUE` to use another queue.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Use Brave Browser when it is already installed:

```sh
EPRT_CUPS_QUEUE="Office_Printer" EPRT_BROWSER_EXECUTABLE_PATH="/usr/bin/brave-browser" python main.py
```

For systemd, adjust the paths, user, CUPS queue, and browser path in `deploy/eprt.service`, then install and start it:

```sh
sudo cp deploy/eprt.service /etc/systemd/system/eprt.service
sudo systemctl daemon-reload
sudo systemctl enable --now eprt
sudo systemctl status eprt
```

View service logs with:

```sh
journalctl -u eprt -f
```

Or install Playwright's Chromium, then start ePRT normally:

```sh
python -m playwright install chromium
python main.py
```

ePRT prints A4 PDFs with 2 cm margins. TeX Live, Pandoc, and XeLaTeX are not required.
