# yikchan
bucknell.wtf sourcecode

## deployment
* edit the big ol' block at the top of `app.py` to suit your needs
* check and tweak any of the files under `static` and `templates` as desired
    * In HTML templates, `{{variables}}` are used to insert data from Python code. You can of course edit the surrounding tags, but the underlying data comes from the Flask app. (which is very simple, so you could of course tweak it too.)
* run `python3 app.py` (or gunicorn w/ some proxy if you're doing production. i'm not your mom, i won't judge)

## sources
* https://stackoverflow.com/a/925630 - for stripping HTML
* https://stackoverflow.com/questions/25674322/post-values-from-an-html-form-and-access-them-in-a-flask-view - multiple answers combined to fix my flask endpoint
* https://stackoverflow.com/a/10965916 - flask aliases
* https://www.edmondchuc.com/deploying-python-flask-with-gunicorn-nginx-and-systemd/ - flask deployment
* https://newcss.net/theme/terminal/ - terminal theme
* https://stackoverflow.com/questions/905144/sed-beginner-changing-all-occurrences-in-a-folder - to fix timestamps w/o editing my code