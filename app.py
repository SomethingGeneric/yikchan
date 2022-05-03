# Stdlib
import sys, os

# PyPi
from flask import *

# This project
from postlib import postlib
from config import settingsloader

if os.path.exists(".use_theme"):
    with open(".use_theme") as f:
        settings_fn = f.read().strip()
else:
    if sys.argv[1] == "":
        settings_fn = "default.config"
    else:
        settings_fn = sys.argv[1]

settings = settingsloader(settings_fn)

PRODUCT = settings.settings["PRODUCT"]
TAGLINE = settings.settings["TAGLINE"]
TZ_STRING = settings.settings["TZ_STRING"]

###############################################################################
#                                                                             #
# Data
POST_DIR = "posts"

# Deployment shit
PORT = 8000
HOST = "0.0.0.0"
DEBUG = True
#                                                                             #
###############################################################################

if os.path.exists("static/terminal.css"):
    os.remove("static/terminal.css")

with open("static/terminal_def.css") as f:
    css = f.read()

for color in ["BG_2", "BG_3", "LK_1", "LK_2", "AC_1"]:
    css = css.replace(color, settings.settings[color])

with open("static/terminal.css", "w") as f:
    f.write(css)

app = Flask(__name__)
pm = postlib(POST_DIR, TZ_STRING)


@app.route("/post/<pid>", methods=["GET", "POST"])
def post(pid):
    if request.method == "POST":
        status, msg = pm.mkpost(pid, request.form["post-raw"])
        if status == True:
            return redirect("/post/" + pid)
        else:
            return render_template(
                "page.html",
                product=PRODUCT,
                title="Error making post",
                tagline="Couldn't make your post because: <code>" + msg + "</code>",
                page="<p>You may want to review the <a href='/rules'>rules</a>.</p>",
            )
    else:
        return render_template(
            "page.html",
            product=PRODUCT,
            title="Thread " + str(pid),
            tagline="You can reply to thread " + str(pid) + " down below.",
            page=pm.htmlof(pid)
            + render_template(
                "form.html",
                form_title="Reply to thread " + str(pid),
                next_post_id=pm.mkpostid(),
            ),
        )


@app.route("/all")
@app.route("/recent")
def chonky():
    return render_template(
        "page.html",
        product=PRODUCT,
        title="All Posts",
        tagline=TAGLINE
        + "<br/><br/><b>Click on a thread's title if you'd like to reply to it.</b>",
        page=pm.htmlofall(),
    )


@app.route("/rules")
def rulepg():
    return render_template(
        "page.html",
        product=PRODUCT,
        title="Rules",
        tagline="Please review before posting.",
        page=render_template("rules.html"),
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pid = str(pm.mkpostid())
        status, msg = pm.mkpost(pid, request.form["post-raw"])
        if status == True:
            return redirect("/post/" + pid)
        else:
            return render_template(
                "page.html",
                product=PRODUCT,
                title="Error making post",
                tagline="Couldn't make your post because: <code>" + msg + "</code>",
                page="<p>You may want to review the <a href='/rules'>rules</a>.</p>",
            )
    else:
        return render_template(
            "page.html",
            product=PRODUCT,
            title="Home",
            tagline=TAGLINE,
            page=render_template("landing.html")
            + render_template(
                "form.html", form_title="New Thread", next_post_id=pm.mkpostid()
            ),
        )


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
