import sys

def display(msg, end="\n"):
    sys.stdout.write(msg + end)
    sys.stdout.flush()