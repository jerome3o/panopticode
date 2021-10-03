from srv.server import bank_statement_ingress, Statement


def main():
    statement_file = "scraper/data/2021-09-27T09_36_57.704Z/Export20210927223704.csv"
    with open(statement_file, "r") as f:
        bank_statement_ingress(
            Statement(**{"text": f.read()})
        )


if __name__ == "__main__":
    main()