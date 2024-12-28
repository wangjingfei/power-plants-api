#!/bin/bash

# 定义颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() {
    echo -e "${GREEN}[INFO] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# 检查Python是否安装
check_python() {
    info "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        error "Python3 is not installed. Please install Python3 first:
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv"
    fi
}

# 检查是否安装了python3-venv
check_python_venv() {
    info "Checking python3-venv installation..."
    if ! dpkg -l | grep -q python3-venv; then
        info "Installing python3-venv..."
        sudo apt update
        sudo apt install -y python3-venv
    fi
}

# 清理旧的虚拟环境
cleanup_venv() {
    info "Cleaning up old virtual environment..."
    if [ -d "venv" ]; then
        rm -rf venv
    fi
}

# 检查虚拟环境
check_venv() {
    info "Creating virtual environment..."
    cleanup_venv
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        error "Failed to create virtual environment. Please check your Python installation."
    fi
    
    # 验证虚拟环境是否创建成功
    if [ ! -f "venv/bin/activate" ]; then
        error "Virtual environment creation failed. Missing activation script."
    fi
}

# 激活虚拟环境
activate_venv() {
    info "Activating virtual environment..."
    if [ ! -f "venv/bin/activate" ]; then
        error "Virtual environment activation script not found"
    fi
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        error "Failed to activate virtual environment"
    fi
    
    # 验证虚拟环境是否正确激活
    if [ -z "$VIRTUAL_ENV" ]; then
        error "Virtual environment not properly activated"
    fi
}

# 安装依赖
install_dependencies() {
    info "Installing dependencies..."
    if [ ! -f "venv/bin/pip" ]; then
        error "pip not found in virtual environment"
    fi
    
    # 升级pip
    venv/bin/pip install --upgrade pip
    if [ $? -ne 0 ]; then
        error "Failed to upgrade pip"
    fi
    
    # 安装依赖
    venv/bin/pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        error "Failed to install dependencies"
    fi
}

# 启动应用
start_app() {
    info "Starting application..."
    if [ ! -f "venv/bin/python" ]; then
        error "Python not found in virtual environment"
    fi
    venv/bin/python run.py
}

# 主函数
main() {
    check_python
    check_python_venv
    check_venv
    activate_venv
    install_dependencies
    start_app
}

# 运行主函数
main 