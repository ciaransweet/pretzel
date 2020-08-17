#!/usr/bin/env python3
import os

from aws_cdk import core

from stack import PretzelStack

tags = {
    "APPLICATION": "pretzel",
    "ENV": os.environ.get("ENV", "dev"),
    "SOURCE": "https://github.com/ciaranevans/pretzel",
    "ORG": "Development Seed",
}

app = core.App()
PretzelStack(app, f"pretzel-{os.environ.get('ENV', 'dev')}")
_ = [core.Tag.add(app, key, val) for key, val in tags.items()]
app.synth()
