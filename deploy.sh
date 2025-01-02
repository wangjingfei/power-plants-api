#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 定义变量
APP_NAME="power-plants-api"
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
    # 创建临时解压目录
    mkdir -p /tmp/app_temp
    
    # 解压应用文件
    tar xzf $DEPLOY_TEMP -C /tmp/app_temp
    
    # 复制文件到目标目录
    cp -r /tmp/app_temp/* $APP_PATH/
    
    # 设置权限
    chown -R $USER:$GROUP $APP_PATH
    
    # 清理临时目录
    rm -rf /tmp/app_temp
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
Description=Power Plants API Service
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$APP_PATH
Environment="PATH=$VENV_PATH/bin"
ExecStart=$VENV_PATH/bin/python run.py
Restart=always
StandardOutput=append:/var/log/power-plant/app.log
StandardError=append:/var/log/power-plant/error.log

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
}

# 配置Nginx
configure_nginx() {
    info "Configuring Nginx..."
    NGINX_CONF="/etc/nginx/sites-available/$APP_NAME"
    
    # 检查配置文件是否存在
    if [ -f "$NGINX_CONF" ]; then
        info "Nginx configuration file already exists, skipping creation..."
    else
        info "Creating Nginx configuration file..."
        cat > $NGINX_CONF << EOF
server {
    listen 80;
    server_name api.wjf.me;

    access_log /var/log/power-plant/nginx/access.log;
    error_log /var/log/power-plant/nginx/error.log;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    fi

    # 创建软链接并检查配置
    ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t || error "Nginx configuration test failed"
}

# 配置应用
configure_application() {
    info "Configuring application..."
    
    # 创建日志目录
    mkdir -p /var/log/power-plant
    touch /var/log/power-plant/app.log
    touch /var/log/power-plant/error.log
    chown -R $USER:$GROUP /var/log/power-plant
    chmod 755 /var/log/power-plant
    chmod 644 /var/log/power-plant/app.log
    chmod 644 /var/log/power-plant/error.log

    CONFIG_FILE="/etc/power-plant/config.ini"
    
    # 创建配置目录
    mkdir -p /etc/power-plant
    
    # 检查配置文件是否存在
    if [ -f "$CONFIG_FILE" ]; then
        info "Configuration file already exists, skipping creation..."
    else
        info "Creating default configuration file..."
        # 创建配置文件
        cat > $CONFIG_FILE << EOF
[database]
host = 127.0.0.1
port = 3306
username = plant
password = xxxxx
database = plants
debug = false

[app]
DEBUG=false
WORKERS=4
HOST=0.0.0.0
PORT=8000

[logging]
LEVEL=INFO
FILE=/var/log/power-plant/app.log
EOF
        
        # 设置配置文件权限
        chown $USER:$GROUP $CONFIG_FILE
        chmod 640 $CONFIG_FILE
    fi
}

# 启动服务
start_services() {
    info "Starting services..."
    
    # 启动应用服务
    systemctl start $APP_NAME
    systemctl enable $APP_NAME
    
    # 检查 Nginx 配置文件是否存在
    NGINX_CONF="/etc/nginx/sites-available/$APP_NAME"
    if [ ! -f "$NGINX_CONF" ]; then
        info "Restarting Nginx due to new configuration..."
        systemctl restart nginx
        systemctl enable nginx
    else
        info "Nginx configuration exists, skipping restart..."
    fi
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
    configure_application
    setup_virtualenv
    create_systemd_service
    configure_nginx
    start_services
    cleanup
    info "Deployment completed successfully!"
}

# 运行主函数
main