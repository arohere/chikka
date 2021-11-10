import os
os.system("python -m pip freeze > requirements.txt")
with open("requirements.txt") as f:
    s = "\n".join(i.split("==")[0] for i in f.readlines())
with open("requirements.txt", "w") as f:
    print(s)
    f.write(s)
