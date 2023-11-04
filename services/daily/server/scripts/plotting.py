from pathlib import Path
import webbrowser

import pandas as pd
from altair import Chart
from requests import get
import datetime

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
                "date": datetime.datetime.fromisoformat(report["created_timestamp"]),
            }
            for report in reports
        ]
    )
    print(df)

    df = df.melt(
        value_vars=["happiness", "tiredness", "stress"],
        value_name="level",
        var_name="metric",
        id_vars=["date", "notes"],
    )

    c = (
        Chart(df)
        .mark_line(point=True)
        .encode(x="date", y="level", color="metric", tooltip="notes")
        .properties(width="container")
    )
    Path("tmp.html").write_text(c.to_html())
    webbrowser.open("tmp.html")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
