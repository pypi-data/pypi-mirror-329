from dataclasses import dataclass
from typing import Optional

from ynabtransactionadjuster.models.category import Category
from ynabtransactionadjuster.models.payee import Payee


@dataclass(frozen=True)
class SubTransaction:
	"""Represents an YNAB Subtransaction as part of an existing split transaction

	:ivar payee: The payee of the subtransaction
	:ivar category: The category of the subtransaction
	:ivar amount: The amount of the subtransaction in milliunits
	:ivar memo: The memo of the subtransaction
	:ivar transfer_transaction_id: The transaction id of the correlated transaction in the transfer account
	"""
	payee: Payee
	category: Optional[Category]
	memo: Optional[str]
	amount: int
	transfer_transaction_id: Optional[str]
