from typing import List

from ynabtransactionadjuster.exceptions import NoMatchingAccountError
from ynabtransactionadjuster.models.account import Account


class AccountRepo:
	"""Repository which holds all accounts from your YNAB budget

	"""
	def __init__(self, accounts: List[Account]):
		self._accounts = accounts

	def fetch_by_name(self, account_name: str) -> Account:
		"""Fetches a YNAB account by its name

		:param account_name: Name of the account to fetch
		:return: Matched account
		:raises NoMatchingAccountError: if no matching account is found
		"""
		try:
			return next(a for a in self._accounts if a.name == account_name)
		except StopIteration:
			raise NoMatchingAccountError(account_name)

	def fetch_by_id(self, account_id: str) -> Account:
		"""Fetches a YNAB account by its ID
		:param account_id: ID of the account
		:return: Matched account
		:raises NoMatchingAccountError: if no matching account is found
		"""
		try:
			return next(a for a in self._accounts if a.id == account_id)
		except StopIteration:
			raise NoMatchingAccountError(account_id)

	def fetch_all(self) -> List[Account]:
		"""Fetches all accounts from YNAB budget

		:return: list with accounts
		"""
		return self._accounts
