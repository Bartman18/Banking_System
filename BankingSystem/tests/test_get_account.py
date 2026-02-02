import pytest
from service.account_service import AccountService
from service.user_service import UserService

class TestRetrivedAccount:

    def test_get_account_by_user_id(self,db_session,user_data):
        service = AccountService(db_session)
        user_service = UserService(db_session)

        user = user_service.create_user(user_data)

        account = service.get_account_by_user_id(user.id)
        
        assert account is not None
        assert account.id is not None



    def test_get_account(self,db_session,test_account):
        service = AccountService(db_session)
        account = service.get_account(test_account.id)

        assert account is not None
        

    