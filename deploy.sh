#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 定义变量
APP_NAME="fastapi-crud"
APP_PATH="/opt/power-plants"
VENV_PATH="$APP_PATH/venv"
USER="power-plants"
GROUP="power-plants"
PYTHON_VERSION="3.8"
DEPLOY_TEMP="/tmp/${APP_NAME}.tar.gz"

# 打印带颜色的信息
info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# 检查是否以root运行
if [ "$EUID" -ne 0 ]; then 
    error "Please run as root"
fi

# 创建用户和组
create_user() {
    info "Creating user and group..."
    if ! getent group $GROUP >/dev/null; then
        groupadd $GROUP
    fi
    if ! getent passwd $USER >/dev/null; then
        useradd -m -g $GROUP -s /bin/bash $USER
    fi
}

# 安装系统依赖
install_dependencies() {
    info "Installing system dependencies..."
    apt-get update
    apt-get install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python3-pip nginx supervisor
}

# 创建目录结构
create_directories() {
    info "Creating directory structure..."
    mkdir -p $APP_PATH
    mkdir -p $APP_PATH/logs
    mkdir -p $APP_PATH/config
}

# 部署应用
deploy_application() {
    info "Deploying application..."
    # 解压应用文件
    tar xzf $DEPLOY_TEMP -C /tmp
    # 复制文件到目标目录
    cp -r /tmp/$APP_NAME/* $APP_PATH/
    # 设置权限
    chown -R $USER:$GROUP $APP_PATH
}

# 设置Python虚拟环境
setup_virtualenv() {
    info "Setting up virtual environment..."
    python$PYTHON_VERSION -m venv $VENV_PATH
    chown -R $USER:$GROUP $VENV_PATH
    
    # 安装依赖
    su - $USER -c "source $VENV_PATH/bin/activate && pip install -r $APP_PATH/requirements.txt"
}

# 创建systemd服务
create_systemd_service() {
    info "Creating systemd service..."
    cat > /etc/systemd/system/$APP_NAME.service << EOF
[Unit]
Description=FastAPI CRUD API Service
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$APP_PATH
Environment="PATH=$VENV_PATH/bin"
ExecStart=$VENV_PATH/bin/python run.py
Restart=always
StandardOutput=append:$APP_PATH/logs/fastapi.log
StandardError=append:$APP_PATH/logs/fastapi.error.log

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
}

# 配置Nginx
configure_nginx() {
    info "Configuring Nginx..."
    cat > /etc/nginx/sites-available/$APP_NAME << EOF
server {
    listen 80;
    server_name us.wangjingfei.com;  # 使用实际域名

    access_log $APP_PATH/logs/nginx.access.log;
    error_log $APP_PATH/logs/nginx.error.log;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t || error "Nginx configuration test failed"
}

# 启动服务
start_services() {
    info "Starting services..."
    systemctl start $APP_NAME
    systemctl enable $APP_NAME
    systemctl restart nginx
    systemctl enable nginx
}

# 清理临时文件
cleanup() {
    info "Cleaning up..."
    rm -f $DEPLOY_TEMP
    rm -rf /tmp/$APP_NAME
}

# 主函数
main() {
    info "Starting deployment..."
    create_user
    install_dependencies
    create_directories
    deploy_application
    setup_virtualenv
    create_systemd_service
    configure_nginx
    start_services
    cleanup
    info "Deployment completed successfully!"
}

# 运行主函数
main