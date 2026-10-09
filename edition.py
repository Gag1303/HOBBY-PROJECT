"""Which edition of the app is running, and where its personal files and fund data live.

- Normal app: Python + Streamlit on this computer (`streamlit run app.py`). Everything works.
- Offline Edition: the desktop program built from desktop_offline/ (Streamlit running inside the app
  window, no Python needed). It has no live internet features: the SEC watcher is hidden and the fund
  pages use the weekly snapshot (see module2_investment/snapshot.py).

The Offline Edition is detected by itself (Python inside the app reports sys.platform "emscripten"),
so both editions run the same code.
"""

import sys
from pathlib import Path

OFFLINE = sys.platform == "emscripten"

PROJECT = Path(__file__).resolve().parent

# Personal files (settings, accounts, reading notes). The Offline Edition keeps them in
# Documents\CFP Toolkit on the PC (mounted at /cfp by the desktop program).
USER_DIR = Path("/cfp") if OFFLINE else PROJECT

# Weekly fund snapshot: written by the Sunday job, read by the Offline Edition.
SNAPSHOT_DIR = USER_DIR / "snapshot" if OFFLINE else PROJECT / "data" / "snapshot"
BUNDLED_SNAPSHOT = PROJECT / "snapshot"  # copy built into the Offline Edition, used until a newer one exists
