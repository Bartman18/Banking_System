import pytest
from service.account_service import AccountService
from security.exception import InsufficientFunds


class TestWithdraw:

    def test_withdraw_success(self, db_session, test_account):
        service = AccountService(db_session)
        initial_balance = test_account.balance
        withdraw_amount = 30.0

        updated_account = service.withdraw(test_account.id, withdraw_amount)

        assert updated_account.balance == initial_balance - withdraw_amount
        assert updated_account.balance == 70.0

    def test_withdraw_insufficient_funds_error(self, db_session, test_account):
        service = AccountService(db_session)
        withdraw_amount = 150.0

        with pytest.raises(InsufficientFunds):
            service.withdraw(test_account.id, withdraw_amount)
