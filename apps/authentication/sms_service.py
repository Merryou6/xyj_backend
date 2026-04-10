from alibabacloud_dypnsapi20170525.client import Client as DypnsapiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dypnsapi20170525 import models as dypnsapi_models
from alibabacloud_tea_util import models as util_models
from django.conf import settings

class AliSmsService:
    def __init__(self):
        config = open_api_models.Config(
            access_key_id=settings.ALIYUN_ACCESS_KEY_ID,
            access_key_secret=settings.ALIYUN_ACCESS_KEY_SECRET,
        )
        config.endpoint = 'dypnsapi.aliyuncs.com'
        self.client = DypnsapiClient(config)

    def send_verify_code(self, phone_number: str):
        """
        发送短信验证码
        返回: (success, message, request_id)
        """
        request = dypnsapi_models.SendSmsVerifyCodeRequest(
            phone_number=phone_number,
            sign_name=settings.ALIYUN_SMS_SIGN_NAME,
            template_code=settings.ALIYUN_SMS_TEMPLATE_CODE,
            # 模板参数：阿里云要求格式为 {"code":"123456"}，这里让阿里云自动生成随机码
            template_param='{"code":"##code##","min":"5"}'   # 5分钟有效期
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = self.client.send_sms_verify_code_with_options(request, runtime)
            # 阿里云返回格式: resp.body.code 为 "OK" 表示成功
            if resp.body.code == 'OK':
                return True, "验证码发送成功", resp.body.request_id
            else:
                return False, resp.body.message, resp.body.request_id
        except Exception as e:
            return False, str(e), None

    def check_verify_code(self, phone_number: str, code: str):
        """
        校验验证码
        返回: (is_valid, message)
        """
        request = dypnsapi_models.CheckSmsVerifyCodeRequest(
            phone_number=phone_number,
            code=code
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = self.client.check_sms_verify_code_with_options(request, runtime)
            # 根据阿里云文档，校验成功时 resp.body.code 为 "OK"，且 resp.body.verify_result 可能为 true
            if resp.body.code == 'OK' and resp.body.verify_result:
                return True, "验证码正确"
            else:
                return False, resp.body.message or "验证码错误"
        except Exception as e:
            return False, str(e)