import json
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent


def main():
    (ROOT / "pseudo").mkdir(exist_ok=True)
    sources = json.loads((ROOT / "reference" / "pseudopotential_sources.json").read_text())
    for source in sources:
        with urlopen(source["url"], timeout=60) as response:
            (ROOT / "pseudo" / source["filename"]).write_bytes(response.read())
        print(source["filename"])


if __name__ == "__main__":
    main()
