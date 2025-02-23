from dataclasses import dataclass
from typing import Optional


@dataclass
class Credentials:
	"""Credentials to use for YNAB

	:ivar token: The YNAB token to use
	:ivar budget: The YNAB budget id to use
	:ivar account: Optionally the YNAB account id to use
	"""
	token: str
	budget: str
	account: Optional[str] = None
