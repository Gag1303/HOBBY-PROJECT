# CFP Toolkit – Offline Edition

A Windows program made from the same code as the normal app. Streamlit runs inside the program's window
([stlite](https://github.com/whitphx/stlite) + Electron), so it **needs no Python and no internet**.

| | Normal app | Offline Edition |
|---|---|---|
| Calculator, Law & Regulation, reading list + notes, career guide | ✅ | ✅ |
| SEC update watcher | ✅ | hidden |
| Thai mutual funds, simulator | live from Settrade | weekly snapshot (all funds' latest NAV + full history of the ~300 largest) |

The code knows which edition it runs in by itself (`edition.py`).

Limits: it takes about 20 seconds to start (Python loads inside the window), and links to websites
(Maruey, SEC) don't open from it – the pages say so.

## Where things are saved

`Documents\CFP Toolkit` on the PC:
- `snapshot\` – the weekly fund data,
- `user_settings.json`, `book_notes.json`, `users.json` – language, CFP progress, reading notes, accounts.

These are separate from the normal app's files in the project folder.

## Weekly fund snapshot (every Sunday)

Windows Task Scheduler runs `weekly_snapshot.bat` every **Sunday 10:00** (task "CFP Toolkit weekly fund
snapshot"; if the PC was off it runs at the next start, when there is internet). It runs
`python -m module2_investment.snapshot`, which downloads the data and replaces `Documents\CFP Toolkit\snapshot`.
The program picks the new data up the next time it starts – no rebuild needed. Log: `data\snapshot.log`.

Want more funds with full history? List their symbols, one per line, in `data\snapshot_extra.txt`.

## Building the program

After changing the code, rebuild from the project folder:

```
python desktop_offline/build.py
```

It copies the app and the current snapshot into `desktop_offline/app`, builds
`desktop_offline/dist/win-unpacked/CFP Toolkit Offline.exe` and puts a **CFP Toolkit Offline** shortcut on the
Desktop. Needs [Node.js](https://nodejs.org); the first build downloads Electron and Pyodide.
