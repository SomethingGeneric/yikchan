import os,sys

class settingsloader:
    def __init__(self, fn):
        self.settings = {}
        if not os.path.exists(fn):
            print("Couldn't find file: " + fn)
            sys.exit(1)
        else:
            with open(fn) as f:
                raw = f.read().split("\n")
            for line in raw:
                if line != "" and line != "\n" and line[0] != "#":
                    if "=" in line:
                        stuff = line.split("=")
                        key = stuff[0]
                        val = stuff[1]
                        self.settings[key] = val.replace("\"","")