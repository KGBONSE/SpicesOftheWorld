"""Shared helpers: base64-encode the committed brand assets for inlining into label HTML."""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = os.path.dirname(HERE)                       # graphics/labels/chilli-oil
REPO = os.path.abspath(os.path.join(LABELS, "..", "..", ".."))
LOGO_DIR = os.path.join(REPO, "brand-assets", "logo")


def b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def logo_black():
    return b64_file(os.path.join(LOGO_DIR, "fudi-people-logo-black-bold.png"))


def logo_maroon():
    return b64_file(os.path.join(LOGO_DIR, "fudi-people-logo-maroon.png"))


def emblem(name):
    """name: fudi-heart-emblem | fudi-buddha-emblem | fudi-dragon-emblem"""
    return b64_file(os.path.join(LABELS, name + ".svg"))


def out_path(filename):
    return os.path.join(LABELS, filename)
