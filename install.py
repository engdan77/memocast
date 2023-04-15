from urllib.request import urlopen
from pathlib import Path
import zipfile
url = "https://github.com/engdan77/memocast/archive/refs/heads/master.zip"
zipf = "memocast.zip"
with urlopen(url) as file:
    content = file.read()
with open(zipf, 'wb') as dl:
    dl.write(content)
with zipfile.ZipFile(zipf, "r") as zipr:
    zipr.extractall(".")
Path(zipf).unlink()