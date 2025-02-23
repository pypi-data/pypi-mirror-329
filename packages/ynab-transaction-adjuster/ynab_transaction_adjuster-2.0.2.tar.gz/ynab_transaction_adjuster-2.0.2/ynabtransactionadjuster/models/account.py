from dataclasses import dataclass


@dataclass
class Account:
	"""Account object from YNAB

	:ivar id: the id of the account
	:ivar name: the name of the account
	"""
	id: str
	name: str
