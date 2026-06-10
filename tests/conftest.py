"""Shared environment setup for droras tests."""

import os

# pygame が import される前に設定し、テスト中の実音声出力を抑止する
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
