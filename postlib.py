# Stdlib
import os, sys, subprocess
from datetime import date, datetime
from io import StringIO
from html.parser import HTMLParser

# PyPi
from flask import render_template

s = os.sep

if s != "/":
    print(
        "We only do *nix here, sir\n(or ma'am or them/they (or ze/zir (uhhhhh i'm out of the loop)))"
    )
    sys.exit(1)


def checkp(p):
    if not os.path.exists(p):
        return False
    else:
        return True


def ensuredir(tdir):
    if not checkp(tdir):
        os.mkdir(tdir)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class postlib:
    def __init__(self, root, tzstr):
        self.root = root
        self.tzstr = tzstr

        ensuredir(self.root)

    def mkpost(self, pid, text):
        pid = str(pid)  # flask might int-ify it

        # strip dangerous tags
        text = strip_tags(text)
        # obv do before the following

        dt = datetime.now()
        text += "<h5><code>" + str(dt) + " " + self.tzstr + "</code></h5>"

        if not checkp(self.root + s + pid):
            print("New post, id: " + pid)
            with open(self.root + s + pid, "w") as f:
                f.write(text + "\n")
        else:
            print("Post already exists, appending. id: " + pid)
            with open(self.root + s + pid, "a") as f:
                f.write("--REPLY--\n" + text + "\n")

    def getpost(self, pid):
        pid = str(pid)
        if checkp(self.root + s + pid):
            with open(self.root + s + pid, "r") as f:
                return f.read()
        else:
            return "Post not found"

    def htmlof(self, pid):
        pid = str(pid)
        raw = self.getpost(pid)
        if raw == "Post not found":
            print("Failed to get " + pid)
            return "<p>" + raw + "</p>"
        else:
            html = (
                "<h3><a class='unlink' href=\"/post/"
                + pid
                + '">Thread '
                + pid
                + "</a></h3>"
            )
            if "--REPLY--" in raw:
                replies = raw.split("--REPLY--")
                for reply in replies:
                    html += render_template("post.html", content=reply) + "<br/>"
            else:
                html += render_template("post.html", content=raw)
            return html

    def htmlofall(self):
        html = ""
        for post in os.listdir(self.root):
            html += self.htmlof(post) + "<hr/>"
        return html

    def mkpostid(self):
        return len(os.listdir(self.root)) + 1


if __name__ == "__main__":
    pm = postlib("posts", "EST")
    for i in range(1, 10):
        pm.mkpost(i, subprocess.check_output(["fortune"]).decode())
        for j in range(1, 4):
            pm.mkpost(i, subprocess.check_output(["fortune"]).decode())
