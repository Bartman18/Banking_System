from service.user_service import UserService
import pytest
from security.exception import UserNotFound, InvalidAmount, UserAlreadyExists

class TestUserService:

    def test_create_user(self, db_session, user_data):
        service = UserService(db_session)
        user = service.create_user(user_data)
        account = service.get_user_account(user.id)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert account.id is not None

    def test_get_by_id(self, db_session, user_data):
        service = UserService(db_session)
        user = service.create_user(user_data)

        id = service.get_by_id(user.id)

        assert id is not None

    def test_get_by_email(self, db_session, user_data):
        service = UserService(db_session)
        user = service.create_user(user_data)

        email = service.get_by_email(user.email)

        assert email is not None

    
    def test_delete_user_error(self,db_session,test_user):
        service = UserService(db_session)

        with pytest.raises(UserNotFound):
             service.delete_user(test_user.id+1)


    def test_create_user_error_invalid_balanace(self,db_session,user_invalid_balance):
        service  = UserService(db_session)
        with pytest.raises(InvalidAmount):
            service.create_user(user_invalid_balance)


    def test_create_user_error_user_exist(self,db_session,test_user, user_data):
        service  = UserService(db_session)
        with pytest.raises(UserAlreadyExists):
            service.create_user(user_data)