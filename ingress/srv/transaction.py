from typing import Optional
from apitools.mongodb import MongoCrud


class TransactionsCrud(MongoCrud):
    def find(self, account: str = None):
        kwargs = {**({"account": account} if account is not None else {})}

        return list(
            filter(
                lambda x: x is not None,
                map(
                    lambda doc: self._to_dto(self._try_parse_dict(doc)),
                    self._collection.find({"account": account}),
                ),
            )
        )
