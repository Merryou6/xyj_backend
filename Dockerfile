# syntax=docker/dockerfile:1

# 寻遗集 Dockerfile
# 基于 Python 3.14 构建 Django 6.0 应用容器

# 设置 Python 版本参数
ARG PYTHON_VERSION=3.14.2
FROM python:${PYTHON_VERSION}-slim as base

# 禁止 Python 生成 .pyc 文件，减少镜像体积
ENV PYTHONDONTWRITEBYTECODE=1

# 禁用 Python 输出缓冲，确保日志实时输出
# 避免应用崩溃时因缓冲导致日志丢失
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 创建系统用户组和用户，以非特权用户身份运行应用
# 遵循 Docker 安全最佳实践，避免使用 root 用户
ARG UID=1001
ARG GID=1001
RUN addgroup --system --gid ${GID} appgroup && \
    adduser --system --uid ${UID} --ingroup appgroup appuser

# 安装 Python 依赖
# 使用 cache mount 缓存 pip 包，加速后续构建
# 使用 bind mount 直接挂载 requirements.txt，无需复制到镜像中
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# 复制项目源代码到容器
# 使用 --chown 确保文件权限正确，避免权限问题
COPY --chown=appuser:appgroup . .

# 切换到非特权用户运行应用
USER appuser

# 暴露应用监听端口（Gunicorn 默认使用 8000 端口）
EXPOSE 8000

# 启动命令：使用 Gunicorn 作为 WSGI 服务器运行 Django 应用
CMD ["gunicorn", "DjangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]