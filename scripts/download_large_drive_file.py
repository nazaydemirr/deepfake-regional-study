#!/usr/bin/env python3
"""Download large Google Drive files that require the virus-scan confirmation form."""

from __future__ import annotations

import argparse
import http.cookiejar
import html.parser
import sys
import urllib.parse
import urllib.request
from pathlib import Path


class DownloadFormParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_form = False
        self.action = ""
        self.inputs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "form" and attr.get("id") == "download-form":
            self.in_form = True
            self.action = attr.get("action", "")
        elif self.in_form and tag == "input" and "name" in attr:
            self.inputs[attr["name"]] = attr.get("value", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "form" and self.in_form:
            self.in_form = False


def build_opener() -> urllib.request.OpenerDirector:
    cookie_jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def fetch(opener: urllib.request.OpenerDirector, url: str) -> bytes:
    with opener.open(url, timeout=60) as response:
        return response.read()


def download(opener: urllib.request.OpenerDirector, url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".download")
    with opener.open(url, timeout=60) as response, tmp.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    tmp.replace(target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id")
    parser.add_argument("target")
    args = parser.parse_args()

    opener = build_opener()
    first_url = f"https://drive.google.com/uc?export=download&id={args.file_id}"
    initial = fetch(opener, first_url)
    if not initial.lstrip().startswith(b"<!DOCTYPE html>"):
        target = Path(args.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(initial)
        return 0

    page = initial.decode("utf-8", errors="replace")
    form = DownloadFormParser()
    form.feed(page)
    if not form.action or "id" not in form.inputs:
        print("Could not find Google Drive download confirmation form.", file=sys.stderr)
        return 1

    url = form.action + "?" + urllib.parse.urlencode(form.inputs)
    download(opener, url, Path(args.target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
