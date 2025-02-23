import inspect
from collections import Counter
from typing import Callable

from ynabtransactionadjuster.exceptions import SignatureError


class SignatureChecker:

	def __init__(self, func: Callable, parent_func: Callable):
		self.func_name = func.__name__
		self.parameters = list(inspect.signature(func).parameters.values())
		self.expected_parameters = [v for v in inspect.signature(parent_func).parameters.values() if v.name != 'self']

	def check(self):
		self.check_parameter_count()
		self.check_parameter_annotations()

	def check_parameter_count(self):
		if len(self.expected_parameters) != len(self.parameters):
			raise SignatureError(SignatureError(f"Function '{self.func_name}' needs to have exactly "
												f"{len(self.expected_parameters)} parameter(s)"))

	def check_parameter_annotations(self):
		annotations = [p.annotation for p in self.parameters if p.annotation != inspect._empty]
		expected_annotations = [p.annotation for p in self.expected_parameters if p.annotation != inspect._empty]

		counter = Counter(annotations)
		expected_counter = Counter(expected_annotations)
		if counter - expected_counter:
			raise SignatureError(f"Function '{self.func_name}' with {annotations} does not have expected "
								 f"annotations {expected_annotations}")


