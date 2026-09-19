"""TDX client credentials are read from the environment only."""

from __future__ import annotations

import itertools
import os

import requests
from django.conf import settings


class TdxConfigError(RuntimeError):
    pass


def _pairs():
    pairs = []
    primary = (os.getenv("TDX_CLIENT_ID"), os.getenv("TDX_CLIENT_SECRET"))
    if primary[0] and primary[1]:
        pairs.append(primary)
    index = 2
    while True:
        client_id = os.getenv(f"TDX_CLIENT_ID_{index}")
        secret = os.getenv(f"TDX_CLIENT_SECRET_{index}")
        if not client_id or not secret:
            break
        pairs.append((client_id, secret))
        index += 1
    if not pairs:
        raise TdxConfigError(
            "No TDX credentials found. Copy .env.example to .env and set "
            "TDX_CLIENT_ID / TDX_CLIENT_SECRET."
        )
    return pairs


_cycle = None


def next_credential():
    global _cycle
    if _cycle is None:
        _cycle = itertools.cycle(_pairs())
    return next(_cycle)


def request_json(url):
    client_id, client_secret = next_credential()
    token = requests.post(
        settings.TDX_AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    token.raise_for_status()
    access = token.json().get("access_token")
    if not access:
        raise TdxConfigError("TDX token response did not include access_token.")
    response = requests.get(
        url,
        headers={"authorization": f"Bearer {access}"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
