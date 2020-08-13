#!/usr/bin/env python3
import os

from aws_cdk import core

from stack import MosexStack

tags = {
    "APPLICATION": "mosex",
    "ENV": os.environ.get("ENV", "dev"),
    "SOURCE": "https://github.com/ciaranevans/mosex",
    "ORG": "Development Seed",
}

app = core.App()
MosexStack(app, f"mosex-{os.environ.get('ENV', 'dev')}")
_ = [core.Tag.add(app, key, val) for key, val in tags.items()]
app.synth()
