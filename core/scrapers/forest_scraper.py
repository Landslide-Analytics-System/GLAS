from selenium import webdriver
import sys
import os
import os.path
from time import sleep
from contextlib import contextmanager
from webdriver_manager.chrome import ChromeDriverManager


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stdout


browser = None
with suppress_stdout():
    # Will install latest version or used cached version if already present.
    browser = webdriver.Chrome(ChromeDriverManager().install())
    print("\033[A                             \033[A")


file = open("Forest Gain APIs.txt", "r")
found = False
for idx, line in enumerate(file.readlines()):
    if "30N_070W" in line:
        found = True
        continue
    if not found:
        continue
    # if not "50N" in line:
        # continue
    line = line.replace("gain", "lossyear")
    print("Doing:", line[-35:])
    browser.get(line)
    sleep(0.5)
