import os

text = open("new.service").read()
text = text.replace("PATH", os.getcwd())
os.remove("new.service")
with open("new.service", "w") as f:
    f.write(text)
