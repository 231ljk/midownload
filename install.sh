#!/usr/bin/env bash
# Nx Programming Language - Installer Script
# Supports: Linux (x86_64, arm64), macOS (x86_64, arm64)
# Usage: curl -fsSL https://raw.githubusercontent.com/231ljk/midownload/main/install.sh | bash
set -e
NX_VERSION="0.1.0"
NX_REPO="231ljk/midownload"
NX_BRANCH="main"
NX_INSTALL_DIR="${NX_INSTALL_DIR:-$HOME/.nx}"
NX_BIN_DIR="$NX_INSTALL_DIR/bin"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
info() { echo -e "${BLUE}[信息]${NC} $1"; }
success() { echo -e "${GREEN}[成功]${NC} $1"; }
warn() { echo -e "${YELLOW}[警告]${NC} $1"; }
error() { echo -e "${RED}[错误]${NC} $1"; }
detect_os() {
    local os
    case "$(uname -s)" in
        Linux*)  os="linux" ;;
        Darwin*) os="macos" ;;
        *)       error "不支持的操作系统: $(uname -s)"; exit 1 ;;
    esac
    echo "$os"
}
detect_arch() {
    local arch
    case "$(uname -m)" in
        x86_64|amd64) arch="x86_64" ;;
        aarch64|arm64) arch="arm64" ;;
        *)             error "不支持的架构: $(uname -m)"; exit 1 ;;
    esac
    echo "$arch"
}
detect_pkg_manager() {
    if command -v apt-get &> /dev/null; then echo "apt"
    elif command -v yum &> /dev/null; then echo "yum"
    elif command -v dnf &> /dev/null; then echo "dnf"
    elif command -v pacman &> /dev/null; then echo "pacman"
    elif command -v brew &> /dev/null; then echo "brew"
    else echo "unknown"; fi
}
install_dependencies() {
    local pkg_manager
    pkg_manager=$(detect_pkg_manager)
    info "检测到包管理器: $pkg_manager"
    if ! command -v curl &> /dev/null; then
        warn "curl 未安装，正在安装..."
        case "$pkg_manager" in
            apt)    sudo apt-get update && sudo apt-get install -y curl ;;
            yum)    sudo yum install -y curl ;;
            dnf)    sudo dnf install -y curl ;;
            pacman) sudo pacman -S --noconfirm curl ;;
            brew)   brew install curl ;;
            *)      error "请手动安装 curl 后重试"; exit 1 ;;
        esac
    fi
}
download_file() {
    local url="$1" output="$2"
    if command -v curl &> /dev/null; then
        curl -fsSL "$url" -o "$output"
    elif command -v wget &> /dev/null; then
        wget -q "$url" -O "$output"
    else
        error "需要 curl 或 wget 来下载文件"; exit 1
    fi
}
main() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}     ${GREEN}Nx Programming Language 安装程序${NC}          ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     ${YELLOW}v${NX_VERSION} - Developer Preview${NC}                ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    local os arch
    os=$(detect_os)
    arch=$(detect_arch)
    info "操作系统: $os"
    info "系统架构: $arch"
    info "安装目录: $NX_INSTALL_DIR"
    echo ""
    install_dependencies "$os"
    info "创建安装目录..."
    mkdir -p "$NX_BIN_DIR"
    local release_url="https://github.com/${NX_REPO}/releases/download/v${NX_VERSION}/nx-${os}-${arch}.tar.gz"
    local raw_url="https://raw.githubusercontent.com/${NX_REPO}/${NX_BRANCH}/bin/nx"
    info "正在下载 Nx 工具链..."
    if curl -fsSLI "$release_url" &> /dev/null; then
        info "从 GitHub Releases 下载..."
        local tmp_file
        tmp_file=$(mktemp /tmp/nx-XXXXXX.tar.gz)
        download_file "$release_url" "$tmp_file"
        tar -xzf "$tmp_file" -C "$NX_BIN_DIR"
        rm -f "$tmp_file"
    else
        info "从仓库源码下载（开发预览版）..."
        download_file "$raw_url" "$NX_BIN_DIR/nx"
    fi
    chmod +x "$NX_BIN_DIR/nx"
    info "配置环境变量..."
    local shell_config=""
    case "$SHELL" in
        */bash) shell_config="$HOME/.bashrc" ;;
        */zsh)  shell_config="$HOME/.zshrc" ;;
        */fish) shell_config="$HOME/.config/fish/config.fish" ;;
        *)      shell_config="$HOME/.profile" ;;
    esac
    local path_entry='export PATH="$HOME/.nx/bin:$PATH"'
    if [ ! -f "$shell_config" ] || ! grep -qF '.nx/bin' "$shell_config"; then
        echo "" >> "$shell_config"
        echo "# Nx Programming Language" >> "$shell_config"
        echo "$path_entry" >> "$shell_config"
        success "已将 Nx 添加到 PATH ($shell_config)"
    else
        info "Nx 已在 PATH 中"
    fi
    echo ""
    info "验证安装..."
    if [ -x "$NX_BIN_DIR/nx" ]; then
        success "Nx 二进制文件已安装: $NX_BIN_DIR/nx"
        echo ""
        "$NX_BIN_DIR/nx" version
        echo ""
        success "Nx 安装成功！"
        echo ""
        echo -e "${YELLOW}快速开始:${NC}"
        echo "  # 立即使用（当前终端）"
        echo "  export PATH=\"\$HOME/.nx/bin:\$PATH\""
        echo ""
        echo "  # 创建新项目"
        echo "  nx new my-first-nx-project"
        echo ""
        echo "  # 运行 Nx 脚本"
        echo "  nx run my-project/src/main.nx"
        echo ""
        echo "  # 进入交互式解释器"
        echo "  nx repl"
        echo ""
        echo -e "${CYAN}Nx - 全场景覆盖，双范式统一，AI 原生，全语言生态融合${NC}"
        echo ""
    else
        error "安装验证失败，二进制文件不可执行"
        exit 1
    fi
}
main "$@"
