# Stdlib
import os, sys, subprocess
from datetime import date, datetime
from io import StringIO
from html.parser import HTMLParser
from urllib.parse import unquote
from random import randint

# PyPi
from flask import render_template
from better_profanity import profanity

# Custom
from config import settingsloader

s = os.sep

if s != "/":
    print("We only do *nix here.")
    sys.exit(1)

profanity.load_censor_words_from_file("profanity_wordlist.txt")

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
    html = html.lower()
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class postlib:
    def __init__(self, root, tzstr, dc):

        self.do_censor = False
        if dc == "yes":
            self.do_censor = True

        print("Censoring is " + str(self.do_censor))

        self.root = root
        self.tzstr = tzstr

        ensuredir(self.root)

        self.block = []
        if os.path.exists("forbidden.txt"):
            with open("forbidden.txt") as f:
                self.block = f.read().split("\n")

    def mkpost(self, pid, text):

        text = unquote(text)

        print("MAKING POST")
        print("Text: '" + text + "'")

        for thing in self.block:
            if thing in text.lower():
                return (False, "Found restricted string: " + thing)

        if self.do_censor:
            print("Censoring is enabled, checking")
            if profanity.contains_profanity(str(text)):
                print("Filter found bad things")
                return (False, "Profanity filter said: '" + profanity.censor(text, "*") + "'")

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

        return (True, "")

    def getpost(self, pid):
        pid = str(pid)
        if checkp(self.root + s + pid):
            with open(self.root + s + pid, "r") as f:
                return f.read().replace("<script>","").replace("</script>","")
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
        for post in os.listdir(self.root).sort(reverse=True):
            html += self.htmlof(post) + "<hr/>"
        return html

    def mkpostid(self):
        mp = len(os.listdir(self.root)) + 1
        return randint(mp, mp+20)


if __name__ == "__main__":
    pm = postlib("posts", "EST")
    for i in range(1, 10):
        pm.mkpost(i, subprocess.check_output(["fortune"]).decode())
        for j in range(1, 4):
            pm.mkpost(i, subprocess.check_output(["fortune"]).decode())
