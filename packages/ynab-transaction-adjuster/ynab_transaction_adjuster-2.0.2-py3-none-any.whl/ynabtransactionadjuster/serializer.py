import inspect
from typing import List, Optional, Callable

from ynabtransactionadjuster.repos import CategoryRepo
from ynabtransactionadjuster.exceptions import AdjustError
from ynabtransactionadjuster.models import Transaction, ModifiedTransaction, Modifier, Category


class Serializer:

	def __init__(self, transactions: List[Transaction], categories: CategoryRepo, adjust_func: Callable):
		self._transactions = transactions
		self._adjust_func = adjust_func
		self._categories = categories

	def run(self) -> List[ModifiedTransaction]:
		modified_transactions = [self.adjust_single(transaction=t)
								 for t in self._transactions]
		filtered_transactions = [t for t in modified_transactions if t.is_changed()]
		return filtered_transactions

	def adjust_single(self, transaction: Transaction) -> ModifiedTransaction:
		modifier = Modifier.from_transaction(transaction=transaction)
		transaction_field, modifier_field = self.find_field_names()
		modifier_return = self._adjust_func(**{transaction_field: transaction, modifier_field: modifier})
		try:
			self.validate_instance(modifier_return)
			self.validate_attributes(modifier_return)
			self.validate_category(modifier_return.category)
			modified_transaction = ModifiedTransaction(transaction=transaction,
													   modifier=modifier_return)
			return modified_transaction
		except Exception as e:
			raise AdjustError(f"Error while adjusting {transaction.as_dict()}") from e

	def validate_category(self, category: Category):
		if category:
			self._categories.fetch_by_id(category.id)

	@staticmethod
	def validate_attributes(modifier: Modifier):
		Modifier.model_validate(modifier.__dict__)

	@staticmethod
	def validate_instance(modifier: Optional[Modifier]):
		if not isinstance(modifier, Modifier):
			raise AdjustError(f"Adjust function doesn't return TransactionModifier object")

	def find_field_names(self) -> (str, str):
		args_dict = inspect.signature(self._adjust_func).parameters

		# Find transaction field by annotation
		try:
			transaction_field = next(k for k, v in args_dict.items() if v.annotation == Transaction)
		except StopIteration:
			transaction_field = None

		# Find modifier field by annotation
		try:
			modifier_field = next(k for k, v in args_dict.items() if v.annotation == Modifier)
		except StopIteration:
			modifier_field = None

		if transaction_field and modifier_field:
			pass
		elif transaction_field and not modifier_field:
			modifier_field = next(k for k, _ in iter(args_dict.items()) if k != transaction_field)
		elif modifier_field and not transaction_field:
			transaction_field = next(k for k, _ in iter(args_dict.items()) if k != modifier_field)
		else:
			field_iterator = iter(args_dict.keys())
			transaction_field = next(field_iterator)
			modifier_field = next(field_iterator)
		return transaction_field, modifier_field
