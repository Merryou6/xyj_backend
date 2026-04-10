from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'      # 改为完整路径
    label = 'authentication'          # 显式指定短标签