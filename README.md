# 寻遗集

## 技术栈

- **框架**: Django 6.0.4
- **数据库**: MySQL 8.0+
- **认证**: JWT (djangorestframework-simplejwt)
- **API**: Django REST Framework

## 环境要求

### 推荐方式（强烈推荐）- 使用 Docker
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 传统方式
- **Python**: 3.12+
- **MySQL**: 8.0+
- **Git**: 用于版本控制

---

## 本地运行指南

> **强烈推荐使用 Docker 方式**，无需配置 Python 环境和 MySQL，一键启动，环境统一。

### 一、克隆项目

```bash
git clone <项目仓库地址>
cd DjangoProject
```

---

### 二、Docker 方式运行（推荐）

#### 1. 检查 Docker 安装

```bash
docker --version
docker-compose --version
```

> 如果未安装 Docker，请参考：
> - Mac: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
> - Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

#### 2. 一键启动项目

```bash
docker-compose up -d
```

#### 3. 查看运行状态

```bash
docker-compose logs -f
```

#### 4. 访问项目

- API 地址：`http://localhost:8000`
- Django 管理后台：`http://localhost:8000/admin/`

#### 5. 创建超级管理员（可选）

```bash
docker-compose exec web python manage.py createsuperuser
```

#### 6. 停止服务

```bash
docker-compose down
```

#### 7. 重启服务

```bash
docker-compose restart
```

> **Docker 方式优势**：
> - 无需安装 Python、MySQL 等依赖软件
> - 环境统一，避免"在我机器上可以运行"问题
> - 一键启动，快速开始开发
> - 数据持久化存储，重启容器数据不丢失

---

### 三、传统方式运行（Mac 系统）

> 如需使用传统方式运行，请确保已安装 Python 3.12+ 和 MySQL 8.0+

#### 1. 检查 Python 版本

```bash
python3 --version
# 应显示 Python 3.12+
```

> 如果版本低于 3.12，建议使用 pyenv 安装：
> ```bash
> brew install pyenv
> pyenv install 3.12.0
> pyenv local 3.12.0
> ```

#### 2. 配置数据库

```sql
CREATE DATABASE xyj_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'admin'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON xyj_test.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 使用项目已有的虚拟环境

```bash
source .venv/bin/activate
```

> 如果虚拟环境需要重建：
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> ```

#### 4. 安装依赖

```bash
pip install -r requirements.txt
```

#### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

#### 7. 启动开发服务器

```bash
python manage.py runserver
```

访问地址：`http://localhost:8000`

---

### 四、传统方式运行（Windows 系统）

> 如需使用传统方式运行，请确保已安装 Python 3.12+ 和 MySQL 8.0+

#### 1. 检查 Python 版本

打开 **命令提示符** 或 **PowerShell**：

```cmd
python --version
```

> 如果未安装 Python 或版本低于 3.12，请从 [python.org](https://www.python.org/downloads/windows/) 下载 Python 3.12+ 版本，安装时务必勾选 "Add Python to PATH"。

#### 2. 配置数据库

打开 MySQL 客户端，执行以下命令：

```sql
CREATE DATABASE xyj_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'admin'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON xyj_test.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 使用项目已有的虚拟环境

**命令提示符 (CMD)：**
```cmd
.venv\Scripts\activate.bat
```

**PowerShell：**
```powershell
.venv\Scripts\Activate.ps1
```

> 如果 PowerShell 执行策略阻止运行脚本，执行以下命令：
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

> 如果虚拟环境需要重建：
> ```cmd
> python -m venv .venv
> .venv\Scripts\activate.bat
> ```

#### 4. 安装依赖

```cmd
pip install -r requirements.txt
```

> **注意**: 如果安装 PyMySQL 失败，可能需要安装 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)。

#### 5. 数据库迁移

```cmd
python manage.py makemigrations
python manage.py migrate
```

#### 6. 创建超级管理员（可选）

```cmd
python manage.py createsuperuser
```

#### 7. 启动开发服务器

```cmd
python manage.py runserver
```

访问地址：`http://localhost:8000`

---

## Docker Compose 配置说明

`docker-compose.yml` 包含两个服务：

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| db | mysql:8.0 | 3306 | MySQL 数据库 |
| web | 本地构建 | 8000 | Django 应用 |

### 数据库连接信息（Docker 内部）
- **数据库名**: `xyj_test`
- **用户名**: `admin`
- **密码**: `123456`
- **主机**: `db`（Docker 内部服务名）

### 数据持久化

MySQL 数据存储在 Docker 卷 `mysql_data` 中，即使删除容器，数据也不会丢失。

---

## 配置说明

### 主要配置文件

`DjangoProject/settings.py` 中的关键配置：

```python
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xyj_test',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'localhost',  # Docker 方式使用 'db'
        'PORT': '3306',
    }
}

# JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# 阿里云短信配置（如需使用短信功能）
ALIYUN_ACCESS_KEY_ID = ''
ALIYUN_ACCESS_KEY_SECRET = ''
ALIYUN_SMS_SIGN_NAME = '速通互联验证码'
ALIYUN_SMS_TEMPLATE_CODE = '100001'
```

### 阿里云短信配置（可选）

如需使用短信验证码功能，请在阿里云控制台申请：
1. 开通短信服务
2. 获取 `ACCESS_KEY_ID` 和 `ACCESS_KEY_SECRET`
3. 申请短信签名和模板
4. 更新 `settings.py` 中的配置

---

## 常用命令

### Docker 命令

```bash
# 启动服务（后台运行）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec web bash

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

# 停止服务
docker-compose down

# 停止服务并删除数据卷（谨慎使用）
docker-compose down -v

# 重新构建镜像
docker-compose build
```

### Django 命令（传统方式）

```bash
# 启动开发服务器
python manage.py runserver

# 创建应用
python manage.py startapp <app_name>

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 进入 Django shell
python manage.py shell

# 运行测试
python manage.py test
```

---

## 项目结构

```
DjangoProject/
├── apps/                    # 应用目录
│   └── authentication/      # 用户认证应用
│       ├── models.py        # 数据模型
│       ├── views.py         # 视图函数
│       ├── urls.py          # 路由配置
│       └── auth_backends.py # 自定义认证后端
├── DjangoProject/           # 项目配置
│   ├── settings.py          # 全局配置
│   ├── urls.py              # 根路由
│   └── wsgi.py              # WSGI 入口
├── .venv/                   # Python 虚拟环境
├── Dockerfile               # Docker 镜像构建文件
├── docker-compose.yml       # Docker Compose 配置
├── manage.py                # Django 管理命令
└── requirements.txt         # 依赖列表
```

---

## 常见问题

### 1. Docker 服务启动失败
- 检查端口 8000 和 3306 是否被占用
- 确保 Docker Desktop 已启动
- 查看日志：`docker-compose logs`

### 2. 数据库连接失败（传统方式）
- 确保 MySQL 服务已启动
- 检查数据库用户名和密码是否正确
- 确认 MySQL 监听端口为 3306

### 3. 虚拟环境激活失败（Windows）
- 使用正确的激活脚本（CMD 使用 `.bat`，PowerShell 使用 `.ps1`）
- 检查执行策略设置

### 4. 依赖安装失败
- 更新 pip 版本：`pip install --upgrade pip`
- 确保已安装 Python 开发工具

### 5. 端口被占用

```bash
# Mac/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

---

## 开发规范

1. 所有数据库操作使用 Django ORM
2. API 接口使用 REST Framework
3. 代码遵循 PEP 8 规范
4. 提交代码前运行测试
5. 推荐使用 Docker 进行开发和部署

---

## License

MIT License