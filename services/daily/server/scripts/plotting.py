from pathlib import Path
import webbrowser

import pandas as pd
from altair import Chart
from requests import get

_URL = "http://localhost:8000/reports/"


def main():
    reports = get(_URL).json()
    df = pd.DataFrame(
        [
            {
                "happiness": report["report"]["happiness"],
                "tiredness": report["report"]["tiredness"],
                "stress": report["report"]["stress"],
                "notes": report["report"]["notes"],
                "date": report["created_timestamp"],
            }
            for report in reports
        ]
    )
    print(df)

    c = Chart(df).mark_line(point=True).encode(x="date", y="happiness", tooltip="notes")
    Path("tmp.html").write_text(c.to_html())
    webbrowser.open("tmp.html")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
