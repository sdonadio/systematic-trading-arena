#!/usr/bin/env python3
"""tools/build_finale.py — embed the season data into finale.html.

    python3 tools/build_finale.py path/to/finale_data.json
    python3 tools/build_finale.py finale_data.json --rename "Registered=Shown"

finale_data.json is written by the teacher-only AlgoArena script
`scripts/season_finale_data.py`. This tool swaps it into the single
<script type="application/json" id="finale-data"> block of finale.html,
in place (nothing else in the page changes), after dropping fields the
page never shows (seat/bot ids). Regenerating after a new block is two
commands: the data script, then this one.

Team names are shown exactly as registered unless --rename is given; a
warning is printed for any name that looks like an e-mail address, since
the page may be published.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
START = '<script type="application/json" id="finale-data">'
END = '</script>'


def slim(data: dict, rename: dict[str, str]) -> dict:
    for t in data.get("teams", []):
        t.pop("bots", None)
        t.pop("scorer_badges", None)
        if t["name"] in rename:
            t["display"] = rename[t["name"]]
        for b in t.get("blocks", []):
            if b and b.get("tape"):
                b["tape"].pop("ipo_bids", None)
        cf = t.get("cashflow")
        if isinstance(cf, dict) and isinstance(cf.get("blocks"), dict):
            keep = ("cash_open", "cash_close", "inventory_open", "inventory_close",
                    "pnl", "price_result", "net_fees", "carry", "interest", "reading")
            cf["blocks"] = {w: {k: r.get(k) for k in keep if k in r}
                            for w, r in cf["blocks"].items()}
    for b in data.get("blocks", []):
        b.pop("tape_files", None)
        b.pop("eod_files", None)
    return data


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("data", help="finale_data.json from season_finale_data.py")
    ap.add_argument("--page", default=str(ROOT / "finale.html"))
    ap.add_argument("--rename", action="append", default=[],
                    help='"Registered name=Shown name" (repeatable)')
    args = ap.parse_args(argv)
    rename = dict(x.split("=", 1) for x in args.rename if "=" in x)
    data = slim(json.loads(pathlib.Path(args.data).read_text(encoding="utf-8")), rename)
    for t in data.get("teams", []):
        if "@" in str(t.get("display") or t["name"]):
            print("WARNING: team name looks like an e-mail address: %r "
                  "(use --rename to show it differently)" % (t.get("display") or t["name"]),
                  file=sys.stderr)
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    text = text.replace("<", "\\u003c")          # never closes the <script>
    page = pathlib.Path(args.page)
    html = page.read_text(encoding="utf-8")
    i = html.find(START)
    if i < 0:
        raise SystemExit("no finale-data block in %s" % page)
    j = html.find(END, i + len(START))
    html = html[:i + len(START)] + text + html[j:]
    page.write_text(html, encoding="utf-8")
    print("embedded %d bytes (%d teams, %d blocks) into %s"
          % (len(text), len(data.get("teams", [])), len(data.get("blocks", [])), page),
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
