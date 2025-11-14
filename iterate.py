import os


# Specify the directory where the files are located
names = ["nn"]

for name in names:
    os.system(f" python scripts/visualizations.py {name}")
