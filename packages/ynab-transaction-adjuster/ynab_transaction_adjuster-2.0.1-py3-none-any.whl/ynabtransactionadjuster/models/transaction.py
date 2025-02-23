from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Literal, Optional, Tuple

from ynabtransactionadjuster.models.account import Account
from ynabtransactionadjuster.models.category import Category
from ynabtransactionadjuster.models.payee import Payee
from ynabtransactionadjuster.models.subtransaction import SubTransaction


@dataclass(frozen=True, eq=True)
class Transaction:
	"""Represents original transaction from YNAB

	:ivar id: The transaction id
	:ivar account: The account of the transaction
	:ivar amount: The transaction amount in milliunits format
	:ivar category: The category of the original transaction
	:ivar transaction_date: The date of the original transaction
	:ivar memo: The memo of the original transaction
	:ivar payee: The payee of the original transaction
	:ivar flag_color: The flag color of the original transaction
	:ivar import_payee_name: The payee as recorded by YNAB on import
	:ivar import_payee_name_original: The original payee or memo as recorded by the bank
	:ivar approved: approval status of the original transaction
	:ivar cleared: clearance state of the original transaction
	:ivar transfer_transaction_id: id of the originating transaction if transaction is transfer
	"""
	id: str
	account: Account
	transaction_date: date
	category: Optional[Category]
	amount: int
	memo: Optional[str]
	payee: Payee
	flag_color: Optional[Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']]
	import_payee_name_original: Optional[str]
	import_payee_name: Optional[str]
	subtransactions: Tuple[SubTransaction, ...]
	cleared: Literal['uncleared', 'cleared', 'reconciled']
	approved: bool
	transfer_transaction_id: Optional[str]

	@classmethod
	def from_dict(cls, t_dict: dict) -> 'Transaction':

		def build_category(t_dict: dict) -> Optional[Category]:
			if not t_dict['category_name'] in ('Uncategorized', 'Split'):
				return Category(id=t_dict['category_id'], name=t_dict['category_name'])

		def build_payee(t_dict: dict) -> Payee:
			return Payee(id=t_dict['payee_id'], name=t_dict['payee_name'],
						 transfer_account_id=t_dict['transfer_account_id'])

		def build_subtransaction(s_dict: dict) -> SubTransaction:
			return SubTransaction(payee=build_payee(s_dict),
								  category=build_category(s_dict),
								  amount=s_dict['amount'],
								  memo=s_dict['memo'],
								  transfer_transaction_id=s_dict['transfer_transaction_id'])

		return Transaction(id=t_dict['id'],
						   account=Account(id=t_dict['account_id'], name=t_dict['account_name']),
						   transaction_date=datetime.strptime(t_dict['date'], '%Y-%m-%d').date(),
						   category=build_category(t_dict),
						   memo=t_dict['memo'],
						   import_payee_name_original=t_dict['import_payee_name_original'],
						   import_payee_name=t_dict['import_payee_name'],
						   flag_color=t_dict['flag_color'],
						   payee=build_payee(t_dict),
						   subtransactions=tuple([build_subtransaction(st) for st in t_dict['subtransactions']]),
						   amount=t_dict['amount'],
						   approved=t_dict['approved'],
						   cleared=t_dict['cleared'],
						   transfer_transaction_id=t_dict['transfer_transaction_id'])

	def as_dict(self) -> dict:
		return asdict(self)

	def __str__(self) -> str:
		return f"{self.account.name} | {self.transaction_date} | {self.payee.name} | {float(self.amount) / 1000:.2f} | {self.memo}"
