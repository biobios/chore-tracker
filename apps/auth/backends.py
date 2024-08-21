from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get('email')
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # 存在しないユーザーと存在するユーザーの時間差をわからないようにする
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

class UsernameAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # 存在しないユーザーと存在するユーザーの時間差をわからないようにする
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user