# yikchan
bucknell.wtf sourcecode

## deployment
* edit `default.config`, or make a new file, with the same format, suiting your needs.
    * if you make a new file, you'll need to add it to the arguements when running `app.py`. Example: `python3 app.py my_custom.config`
    * `app.py` assumes you'd like to use `default.config` otherwise.
* check the big ol' block at the top of `app.py` to make sure it suits your needs
    * if you use the `yikchan.service`, the port is always `8000`
* check and tweak any of the files under `static` and `templates` as desired
    * In HTML templates, `{{variables}}` are used to insert data from Python code. You can of course edit the surrounding tags, but the underlying data comes from the Flask app. (which is very simple, so you could of course tweak it too.)
* run `python3 app.py` (or gunicorn w/ some proxy if you're doing production. i'm not your mom, i won't judge)
    * You could use `make deploy` to automate above and also copy the example `yikchan.service` automatically.

## sources
* https://stackoverflow.com/a/925630 - for stripping HTML
* https://stackoverflow.com/questions/25674322/post-values-from-an-html-form-and-access-them-in-a-flask-view - multiple answers combined to fix my flask endpoint
* https://stackoverflow.com/a/10965916 - flask aliases
* https://www.edmondchuc.com/deploying-python-flask-with-gunicorn-nginx-and-systemd/ - flask deployment
* https://stackoverflow.com/questions/905144/sed-beginner-changing-all-occurrences-in-a-folder - to fix timestamps w/o editing my code

## CSS
(With some modifications, that can be seen in the static dir)
* https://fonts.xz.style/serve/inter.css
* https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css
* https://newcss.net/theme/terminal.css
