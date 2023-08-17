import os
from requests import get

_key = os.environ["PANOPTICODE_API_KEYS"].split(",")[0]


def main():
    resp = get(
        "http://localhost:8000/ps",
        headers={"X-API-Key": _key},
    )
    print(resp.json())



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
