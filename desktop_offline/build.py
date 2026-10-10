"""Build the CFP Toolkit Offline Edition (a Windows program, no Python needed to run it).

Run from the project folder:  python desktop_offline/build.py
Needs Node.js (https://nodejs.org) and an internet connection the first time (downloads Electron and
Pyodide). It copies the app code and the latest fund snapshot into desktop_offline/app, builds the program
into desktop_offline/dist/win-unpacked and puts a "CFP Toolkit Offline" shortcut on the Desktop.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
APP = HERE / "app"
ROOT_FILES = ["app.py", "edition.py", "auth.py", "cfp_modules.py", "i18n.py", "i18n_th.py", "user_settings.py"]
PACKAGES = ["interface", "regulation", "knowledge", "reading", "module2_investment", "career", "calculators"]
EXE = HERE / "dist" / "win-unpacked" / "CFP Toolkit Offline.exe"


def copy_app() -> None:
    shutil.rmtree(APP, ignore_errors=True)
    APP.mkdir()
    for name in ROOT_FILES:
        shutil.copy2(PROJECT / name, APP / name)
    for package in PACKAGES:
        shutil.copytree(PROJECT / package, APP / package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    snapshot = PROJECT / "data" / "snapshot"
    if not (snapshot / "meta.json").exists():
        raise SystemExit("No fund snapshot yet: run  python -m module2_investment.snapshot  first.")
    shutil.copytree(snapshot, APP / "snapshot")  # used until a newer weekly snapshot exists


def make_icon() -> None:
    """A compass icon (assets/icon.ico), drawn once."""
    icon = HERE / "assets" / "icon.ico"
    if icon.exists():
        return
    from PIL import Image, ImageDraw
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 248, 248), fill=(26, 54, 93), outline=(240, 240, 240), width=10)
    c = size // 2
    d.polygon([(c, 34), (c + 26, c), (c, c)], fill=(235, 72, 72))
    d.polygon([(c, 34), (c - 26, c), (c, c)], fill=(200, 50, 50))
    d.polygon([(c, 222), (c + 26, c), (c, c)], fill=(235, 235, 235))
    d.polygon([(c, 222), (c - 26, c), (c, c)], fill=(200, 200, 200))
    d.ellipse((c - 12, c - 12, c + 12, c + 12), fill=(240, 240, 240))
    icon.parent.mkdir(exist_ok=True)
    img.save(icon, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


LOADING_SCREEN = """
    <div id="cfp-loading"><div class="cfp-spin"></div><p>Loading…</p></div>
    <style>
      #cfp-loading { position: fixed; inset: 0; z-index: 999990; display: flex; flex-direction: column;
        align-items: center; justify-content: center; gap: 12px; background: #0e1117; color: #fafafa;
        font: 18px "Source Sans Pro", "Segoe UI", sans-serif; }
      @media (prefers-color-scheme: light) { #cfp-loading { background: #ffffff; color: #31333f; } }
      .cfp-spin { width: 36px; height: 36px; border: 4px solid rgba(128, 128, 128, .3); border-top-color: #ff4b4b;
        border-radius: 50%; animation: cfp-spin 1s linear infinite; }
      @keyframes cfp-spin { to { transform: rotate(360deg); } }
    </style>
    <script>
      // Remove the loading screen once the app has drawn its menu (the empty placeholder page doesn't count).
      new MutationObserver((_, observer) => {
        if (document.querySelector('[data-testid="stSidebar"]')?.innerText.trim()) {
          document.getElementById("cfp-loading")?.remove();
          observer.disconnect();
        }
      }).observe(document.documentElement, { childList: true, subtree: true });
    </script>
"""


def quiet_loading() -> None:
    """Hide the engine's start-up notices ("Loading Pyodide", each package name, ...) and show one simple
    "Loading…" screen instead. Error notices stay on (the loading screen sits below them)."""
    build = HERE / "build"
    entry = next(p for p in (build / "assets").glob("index-*.js")
                 if "readSitePackagesSnapshot" in p.read_text(encoding="utf-8"))
    js = entry.read_text(encoding="utf-8")
    found = re.findall(r"\{kernel:(\w+)\}", js)
    if len(found) != 1:
        raise SystemExit(f"Can't hide the loading notices: {entry.name} changed in this stlite version.")
    entry.write_text(js.replace(f"{{kernel:{found[0]}}}", f"{{kernel:{found[0]},disableProgressToasts:!0}}"),
                     encoding="utf-8")
    page = build / "index.html"
    html = page.read_text(encoding="utf-8").replace("<title>Stlite Desktop</title>", "<title>CFP Toolkit Offline</title>")
    if '<div id="root"></div>' not in html:
        raise SystemExit("Can't add the loading screen: build/index.html changed in this stlite version.")
    page.write_text(html.replace('<div id="root"></div>', '<div id="root"></div>' + LOADING_SCREEN), encoding="utf-8")


def npm(*args: str) -> None:
    subprocess.run(["npm", *args], cwd=HERE, check=True, shell=os.name == "nt")


def desktop_shortcut() -> Path:
    link = Path.home() / "Desktop" / "CFP Toolkit Offline.lnk"
    ps = (f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{link}'); "
          f"$s.TargetPath = '{EXE}'; $s.WorkingDirectory = '{EXE.parent}'; "
          f"$s.IconLocation = '{HERE / 'assets' / 'icon.ico'}'; $s.Description = 'CFP Toolkit – Offline Edition'; $s.Save()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return link


if __name__ == "__main__":
    copy_app()
    make_icon()
    if not (HERE / "node_modules").exists():
        npm("install")
    npm("run", "dump")
    quiet_loading()
    npm("run", "app:dir")
    print("Built:", EXE)
    print("Shortcut:", desktop_shortcut())
