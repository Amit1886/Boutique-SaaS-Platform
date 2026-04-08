from __future__ import annotations

import os
import sys

import requests


def main() -> int:
    username = os.environ.get("PA_USERNAME", "")
    token = os.environ.get("PA_API_TOKEN", "")
    domain = os.environ.get("PA_WEBAPP_DOMAIN", "")  # e.g. yourusername.pythonanywhere.com
    host = os.environ.get("PA_HOST", "www.pythonanywhere.com")  # or eu.pythonanywhere.com

    if not (username and token and domain):
        print("Missing env vars: PA_USERNAME, PA_API_TOKEN, PA_WEBAPP_DOMAIN")
        return 2

    url = f"https://{host}/api/v0/user/{username}/webapps/{domain}/reload/"
    res = requests.post(url, headers={"Authorization": f"Token {token}"}, timeout=30)
    if res.status_code not in (200, 201, 204):
        print(f"Reload failed: {res.status_code} {res.text}")
        return 1

    print("Reload triggered OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

