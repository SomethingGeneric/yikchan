# Stdlib
# (none yet)

# PyPi
from flask import *

# This project
from postlib import postlib

###############################################################################
#                                                                             #
# Visible to end user
PRODUCT = "bucknell.wtf"
TAGLINE = "the true voice of bucknell (maybe? i'm no scientist)"
# the code automatically uses your local timezone, this is just appended to the output of that
TZ_STRING = "ETC"

# Data
POST_DIR = "posts"

# Deployment shit
PORT = 8080
HOST = "0.0.0.0"
DEBUG = True

#                                                                             #
###############################################################################

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
                page="<p>You may want to review the <a href='/rules'>rules</a>.</p>"
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
                page="<p>You may want to review the <a href='/rules'>rules</a>.</p>"
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
