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

# 检查是否安装了Homebrew
check_homebrew() {
    info "Checking Homebrew installation..."
    if ! command -v brew &> /dev/null; then
        error "Homebrew is not installed. Please install Homebrew first:
        /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
}

# 检查Python是否安装
check_python() {
    info "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        error "Python3 is not installed. Please install Python3 first:
        brew install python3"
    fi
}

# 检查虚拟环境
check_venv() {
    info "Checking virtual environment..."
    if [ ! -d "venv" ]; then
        info "Creating virtual environment..."
        # 使用完整路径的python3来创建虚拟环境
        /usr/local/bin/python3 -m venv venv || /opt/homebrew/bin/python3 -m venv venv
        if [ $? -ne 0 ]; then
            error "Failed to create virtual environment. Try installing python3-venv:
            brew install python3"
        fi
    fi
}

# 激活虚拟环境
activate_venv() {
    info "Activating virtual environment..."
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        error "Failed to activate virtual environment"
    fi
}

# 安装依赖
install_dependencies() {
    info "Installing dependencies..."
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r requirements.txt
}

# 启动应用
start_app() {
    info "Starting application..."
    venv/bin/python run.py
}

# 主函数
main() {
    check_homebrew
    check_python
    check_venv
    activate_venv
    install_dependencies
    start_app
}

# 运行主函数
main 