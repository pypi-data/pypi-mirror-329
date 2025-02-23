from pydantic import BaseModel, model_validator
from datetime import date
from typing import List, Literal, Optional

from ynabtransactionadjuster.models import Category
from ynabtransactionadjuster.models import Transaction
from ynabtransactionadjuster.models import ModifierSubTransaction
from ynabtransactionadjuster.models import Payee
from ynabtransactionadjuster.models.account import Account


class Modifier(BaseModel):
	"""Transaction object prefilled with values from original transaction which can take modified values

	:ivar category: The category of the transaction
	:ivar transaction_date: The date of the transaction
	:ivar memo: The memo of the transaction
	:ivar payee: The payee of the transaction
	:ivar flag_color: The flag color of the transaction
	:ivar subtransactions: The subtransactions of the transaction
	:ivar cleared: Clearance status
	:ivar approved: Approval status of the transaction
	:ivar account: The account of the transaction
	"""

	transaction_date: date
	category: Optional[Category]
	memo: Optional[str]
	payee: Payee
	flag_color: Optional[Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']]
	subtransactions: List[ModifierSubTransaction]
	approved: bool
	cleared: Literal['uncleared', 'cleared', 'reconciled']
	account: Account

	@classmethod
	def from_transaction(cls, transaction: Transaction):
		return cls(transaction_date=transaction.transaction_date,
				   category=transaction.category,
				   payee=transaction.payee,
				   memo=transaction.memo,
				   flag_color=transaction.flag_color,
				   approved=transaction.approved,
				   cleared=transaction.cleared,
				   subtransactions=[],
				   account=transaction.account)

	@model_validator(mode='after')
	def check_values(self):
		if len(self.subtransactions) == 1:
			raise ValueError(f"There must be at least two subtransactions for a split")
		return self
