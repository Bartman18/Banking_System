from service.user_service import UserService


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

    def test_delete_user(self, db_session, user_data):
        service = UserService(db_session)
        user = service.create_user(user_data)

        service.delete_user(user.id)

        assert service.get_by_id(user.id) is None
