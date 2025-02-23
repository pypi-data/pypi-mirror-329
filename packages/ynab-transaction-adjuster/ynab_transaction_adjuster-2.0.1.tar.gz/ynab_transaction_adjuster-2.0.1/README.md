# ynab-transaction-adjuster

[![GitHub Release](https://img.shields.io/github/release/dnbasta/ynab-transaction-adjuster?style=flat)]() 
[![Maintained](https://img.shields.io/maintenance/yes/2100)]()
[![Monthly downloads](https://img.shields.io/pypi/dm/ynab-transaction-adjuster)]()

[!["Buy Me A Coffee"](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/dnbasta)

This library helps you to automatically adjust transactions in YNAB based on your logic. It allows you to implement 
your adjustments in a simple factory class which you can run against your existing transactions and update relevant 
fields like date, payee, category, memo and flags. It also allows you to split transactions.

## Preparations
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)
2. Get the IDs of your budget and account which records are faulty. You can find both IDs if you go to 
https://app.ynab.com/ and open the target account by clicking on the name on the left hand side menu. 
The URL does now contain both IDs `https://app.ynab.com/<budget_id>/accounts/<account_id>`

## Installation 
Install library from PyPI
```bash
pip install ynab-transaction-adjuster
```

## Usage
A detailed documentation is available at https://ynab-transaction-adjuster.readthedocs.io

# Basic Usage

### Create an Adjuster
Create a child class of `Adjuster`. This class needs to implement a `filter()` and an `adjust()` method which contain 
the intended logic. The `filter()` method receives a list of `Transaction` objects which can be filtered before 
adjustement. The `adjust()` method receives a single `Transaction` and a `Modifier`.The latter is prefilled with values 
from the original transaction and can be altered. The modifier needs to be returned at the end of the function. 
Please check the [detailed usage](https://ynab-transaction-adjuster.readthedocs.io/en/latest/detailed_usage/) section 
for explanations how to change different attributes.

```py
from ynabtransactionadjuster import Adjuster, Transaction, Modifier


class MyAdjuster(Adjuster):

	def filter(self, transactions: List[Transaction]) -> List[Transaction]:
		# your implementation

		# return the filtered list of transactions
		return transactions

	def adjust(self, transaction: Transaction, modifier: Modifier) -> Modifier:
		# your implementation

		# return the altered modifier
		return modifier
```

### Initialize
Create a `Credentials` object and initialize Adjuster class with it. Providing `account` for the credentials is 
optional. If not set the Adjuster will work on all transactions in the budget.  
```py
from ynabtransactionadjuster import Credentials

my_credentials = Credentials(token='<token>', budget='<budget>', account='<account>')
my_adjuster = MyAdjuster(my_credentials)
```

### Apply
Apply the filter and adjust function on the fetched transactions from YNAB via the `apply()` method. It 
returns a filtered list of `ModifiedTransaction` which can be inspected for the changed properties via the 
`changed_attributes` attribute. Only actually changed transactions are returned. 
```py
modified_transactions = my_adjuster.apply()
```

### Update
The modified transactions can be upated in YNAB passing them to the `update()` function. The method returns a list 
with the updated `Transaction` objects.
```py
updated_transactions = my_adjuster.update(modified_transactions)
```
