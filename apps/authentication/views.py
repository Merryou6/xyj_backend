from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PhoneRegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import SendSmsCodeSerializer
from .sms_service import AliSmsService


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "code": 201,
            "message": "注册成功",
            "data": {
                "phone": user.phone,
                "username": user.username
            }
        }, status=status.HTTP_201_CREATED)


class SendSmsCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        sms_service = AliSmsService()
        success, message, _ = sms_service.send_verify_code(phone)
        if success:
            return Response({
                "code": 200,
                "message": message,
                "data": None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "code": 400,
                "message": message,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # 假设原始响应数据包含 access 和 refresh
        original_data = response.data
        return Response({
            "code": 200,
            "message": "登录成功",
            "data": original_data
        }, status=response.status_code)