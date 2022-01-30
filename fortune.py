# This is a thing i used for testing, might end up adding back later
# in some form idk

# Stdlib
import subprocess

# PyPi
from flask import render_template


def fakepost():
    t = subprocess.check_output(["fortune"]).decode()
    return render_template("post.html", content=t)


def mkposts():
    html = ""
    for i in range(1, 10):
        html += fakepost() + "<br/>"
    return html
