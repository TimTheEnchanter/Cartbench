Cartbench with live emulator preview

This folder has to be served by a small web server, because browsers won't
start the emulator's background worker from a file opened directly.

1. Open a terminal in this folder.
2. Run:  python3 -m http.server 8000
3. Visit http://localhost:8000

Exported ROMs download as plain .bin or .a26 files in this version.

The folder can also be hosted as-is on any static web host, such as GitHub Pages.

stellerator-embedded.js and worker/stellerator.js are the prebuilt Stellerator
files from the 6502ts/6502ts.github.io repository, MIT license, copyright
Christian Speckner and contributors. See stellerator-LICENSE.txt.
worker/stellerator.js has a small activity recorder added by tools/patch-worker.py.
It records which ROM bytes run and reach the display. Nothing leaves your browser.
sample-cart.asm is the source of the built-in sample (assemble with dasm).
