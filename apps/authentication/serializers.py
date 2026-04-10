from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Credential, CredentialType
from .sms_service import AliSmsService
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class SendSmsCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    def validate_phone(self, value):
        # 要求未注册才能发送验证码
        from .models import User
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已注册")
        return value

class PhoneRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=64,write_only=True, min_length=6)
    username = serializers.CharField(max_length=150)
    user_type = serializers.CharField(max_length=150)
    code = serializers.CharField(write_only=True, max_length=6, min_length=6)   # 新增验证码字段

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已注册")
        return value

    def validate(self, attrs):
        # 验证短信验证码
        phone = attrs.get('phone')
        code = attrs.get('code')
        sms_service = AliSmsService()
        is_valid, message = sms_service.check_verify_code(phone, code)
        if not is_valid:
            raise serializers.ValidationError({"code": message})
        return attrs

    def create(self, validated_data):
        phone = validated_data['phone']
        password = validated_data['password']
        username = validated_data.get('username', phone)
        user_type = validated_data.get['user_type']


        user = User.objects.create(
            phone=phone,
            username=username,
            user_type=user_type
        )
        Credential.objects.create(
            user=user,
            credential_type=CredentialType.PASSWORD,
            identifier=phone,
            credential=make_password(password),
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        if not phone or not password:
            raise serializers.ValidationError("请提供手机号和密码")

        user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("手机号或密码错误")

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'phone': user.phone,
                'username': user.username,
                'user_type': user.user_type
            }
        }
        return data