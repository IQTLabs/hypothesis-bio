import sys

sections = sys.stdin.read().split("\n# ")
for section in sections:
    filename = section.split("\n")[0].replace("`", "").replace("#", "").replace(" ", "")
    if section[0] == "#":
        section = section[1:]
    with open("api/" + filename + ".md", "w+") as f:
        print("# " + section, file=f)
