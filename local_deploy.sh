#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 定义变量
REMOTE_HOST="plant.wjf.me"
REMOTE_USER="root"
SSH_KEY_PATH="$HOME/.ssh/id_rsa"  # SSH私钥路径
APP_NAME="power-plants-api"
REMOTE_APP_PATH="/opt/power-plants"
LOCAL_TEMP_DIR="/tmp/$APP_NAME"

# 打印带颜色的信息
info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# 检查SSH密钥
check_ssh_key() {
    info "Checking SSH key..."
    if [ ! -f "$SSH_KEY_PATH" ]; then
        error "SSH key not found at $SSH_KEY_PATH"
    fi
}

# 检查SSH连接
check_ssh() {
    info "Checking SSH connection..."
    if ! ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no -q $REMOTE_USER@$REMOTE_HOST exit; then
        error "SSH connection failed. Please check your SSH configuration."
    fi
}

# 准备部署文件
prepare_files() {
    info "Preparing deployment files..."
    # 创建临时目录
    rm -rf $LOCAL_TEMP_DIR
    mkdir -p $LOCAL_TEMP_DIR

    # 复制项目文件
    cp -r app requirements.txt run.py start.sh deploy.sh config $LOCAL_TEMP_DIR/
    cp -r .env $LOCAL_TEMP_DIR/ 2>/dev/null || true  # 如果.env不存在也不报错

    # 创建部署包
    cd /tmp
    tar czf ${APP_NAME}.tar.gz -C $LOCAL_TEMP_DIR .

    # 回到原目录
    cd - > /dev/null

    # 复制deploy.sh到当前目录，方便后续上传
    cp $LOCAL_TEMP_DIR/deploy.sh ./
}

# 上传文件到远程服务器
upload_files() {
    info "Uploading files to remote server..."
    scp -i "$SSH_KEY_PATH" /tmp/${APP_NAME}.tar.gz $REMOTE_USER@$REMOTE_HOST:/tmp/
    scp -i "$SSH_KEY_PATH" deploy.sh $REMOTE_USER@$REMOTE_HOST:/tmp/
}

# 执行远程部署
execute_remote_deploy() {
    info "Executing remote deployment..."
    ssh -i "$SSH_KEY_PATH" $REMOTE_USER@$REMOTE_HOST "bash -s" << 'EOF'
        cd /tmp
        sudo bash deploy.sh
EOF
}

# 清理临时文件
cleanup() {
    info "Cleaning up temporary files..."
    rm -rf $LOCAL_TEMP_DIR
    rm -f /tmp/${APP_NAME}.tar.gz
}

# 主函数
main() {
    info "Starting deployment process..."
    check_ssh_key
    check_ssh
    prepare_files
    upload_files
    execute_remote_deploy
    #cleanup
    info "Deployment completed successfully!"
}

# 运行主函数
main