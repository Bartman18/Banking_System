from service.account_service import AccountService
from security.exception import InvalidAmount
import pytest


class TestDeposit:

    def test_deposit_success(self, db_session, test_account):
        service = AccountService(db_session)
        initial_balance = test_account.balance
        deposit_amount = 50.0

        updated_account = service.deposit(test_account.id, deposit_amount)

        assert updated_account.balance == initial_balance + deposit_amount
        assert updated_account.balance == 150.0

    def test_deposit_invalid_amount_error(self, db_session, test_account):
        service = AccountService(db_session)
        invalid_amount = -50.0

        with pytest.raises(InvalidAmount):
            service.deposit(test_account.id, invalid_amount)
