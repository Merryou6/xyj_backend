from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User, Credential, CredentialType

class PhonePasswordBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            cred = Credential.objects.get(user=user, credential_type=CredentialType.PASSWORD)
            if check_password(password, cred.credential):
                return user
        except (User.DoesNotExist, Credential.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None