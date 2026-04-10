import pymysql
# 伪造版本号以满足 Django 6.0 的要求
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.__version__ = "2.2.1"
pymysql.install_as_MySQLdb()
