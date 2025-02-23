from datetime import datetime

from pydantic import BaseModel, model_validator

from ynabtransactionadjuster.models import Transaction
from ynabtransactionadjuster.models import Modifier


class ModifiedTransaction(BaseModel):
	transaction: Transaction
	modifier: Modifier

	def is_changed(self) -> bool:
		"""Helper function to determine if transaction has been altered as compared to original one

		:returns: True if values from original transaction have been altered, False otherwise
		"""
		if self.changed_attributes:
			return True
		return False

	def __str__(self) -> str:
		return f"{self.transaction} | {self.changed_attributes}"

	def as_dict(self) -> dict:
		"""Returns a dictionary representation of the transaction which is used for the update call to YNAB"""
		t_dict = dict(id=self.transaction.id,
					  payee_name=self.modifier.payee.name,
					  payee_id=self.modifier.payee.id,
					  date=datetime.strftime(self.modifier.transaction_date, '%Y-%m-%d'),
					  approved=self.modifier.approved,
					  cleared=self.modifier.cleared,
					  account_id=self.modifier.account.id)
		if len(self.modifier.subtransactions) > 0:
			t_dict['subtransactions'] = [s.as_dict() for s in self.modifier.subtransactions]
		if self.modifier.category:
			t_dict['category_id'] = self.modifier.category.id
		if self.modifier.flag_color:
			t_dict['flag_color'] = self.modifier.flag_color
		if self.modifier.memo:
			t_dict['memo'] = self.modifier.memo

		return t_dict

	@property
	def changed_attributes(self) -> dict:
		"""Returns a dictionary representation of the modified values and the original transaction"""
		changed_attributes = dict()

		for a in ('payee', 'category', 'flag_color', 'memo', 'approved', 'cleared', 'account'):
			if self._attribute_changed(a):
				changed_attributes[a] = self._create_changed_dict(a)

		if (self.modifier.transaction_date.isocalendar() !=
				self.transaction.transaction_date.isocalendar()):
			changed_attributes['transaction_date'] = self._create_changed_dict('transaction_date')

		if len(self.modifier.subtransactions) > 0:
			changed_attributes['subtransactions'] = self._create_changed_dict('subtransactions')

		return changed_attributes

	def _attribute_changed(self, attribute: str) -> bool:
		o = self.transaction.__getattribute__(attribute)
		m = self.modifier.__getattribute__(attribute)
		if o != m:
			return True

	def _create_changed_dict(self, attribute: str) -> dict:
		return dict(original=self.transaction.__getattribute__(attribute),
					changed=self.modifier.__getattribute__(attribute))

	@model_validator(mode='after')
	def _check_values(self):
		if len(self.modifier.subtransactions) > 1:
			if len(self.transaction.subtransactions) > 1:
				raise ValueError(f"Existing Subtransactions can not be updated")
			if sum(a.amount for a in self.modifier.subtransactions) != self.transaction.amount:
				raise ValueError('Amount of subtransactions needs to be equal to amount of original transaction')
		return self
