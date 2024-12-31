# 定义变量
APP_NAME="power-plants-web"
BUILD_DIR="dist"
REMOTE_HOST="plant.wjf.me"  # 修改这里
REMOTE_USER="your_ssh_user"
SSH_KEY_PATH="$HOME/.ssh/id_rsa" 

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
    server_name plant.wjf.me;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Prefix /api;
    }

    location / {
        root /var/www/$APP_NAME;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    access_log /var/log/nginx/$APP_NAME-access.log;
    error_log /var/log/nginx/$APP_NAME-error.log;
}
EOF
    fi

    # 创建软链接并检查配置
    ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t || error "Nginx configuration test failed"
} 