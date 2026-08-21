# Nx Programming Language - Windows Installer (PowerShell)
# Usage: irm https://raw.githubusercontent.com/231ljk/midownload/main/install.ps1 | iex
$ErrorActionPreference = "Stop"
$NX_VERSION = "0.1.0"
$NX_REPO = "231ljk/midownload"
$NX_BRANCH = "main"
$NX_INSTALL_DIR = "$env:USERPROFILE\.nx"
$NX_BIN_DIR = "$NX_INSTALL_DIR\bin"
function Write-Info($msg)    { Write-Host "[信息] " -ForegroundColor Blue -NoNewline; Write-Host $msg }
function Write-Success($msg) { Write-Host "[成功] " -ForegroundColor Green -NoNewline; Write-Host $msg }
function Write-Warn($msg)    { Write-Host "[警告] " -ForegroundColor Yellow -NoNewline; Write-Host $msg }
function Write-Error($msg)   { Write-Host "[错误] " -ForegroundColor Red -NoNewline; Write-Host $msg }
function Get-Arch {
    switch ($env:PROCESSOR_ARCHITECTURE) {
        "AMD64" { return "x86_64" }
        "ARM64" { return "arm64" }
        default { Write-Error "不支持的架构: $env:PROCESSOR_ARCHITECTURE"; exit 1 }
    }
}
function Download-File($url, $output) {
    try { Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing }
    catch { Write-Error "下载失败: $url"; Write-Error $_.Exception.Message; exit 1 }
}
function Main {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║" -ForegroundColor Cyan -NoNewline
    Write-Host "     Nx Programming Language 安装程序          " -NoNewline
    Write-Host "║" -ForegroundColor Cyan
    Write-Host "║" -ForegroundColor Cyan -NoNewline
    Write-Host "     v$NX_VERSION - Developer Preview                " -NoNewline
    Write-Host "║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    $arch = Get-Arch
    Write-Info "操作系统: Windows"
    Write-Info "系统架构: $arch"
    Write-Info "安装目录: $NX_INSTALL_DIR"
    Write-Host ""
    Write-Info "创建安装目录..."
    New-Item -ItemType Directory -Force -Path $NX_BIN_DIR | Out-Null
    $releaseUrl = "https://github.com/$NX_REPO/releases/download/v$NX_VERSION/nx-windows-$arch.zip"
    $rawUrl = "https://raw.githubusercontent.com/$NX_REPO/$NX_BRANCH/bin/nx.cmd"
    Write-Info "正在下载 Nx 工具链..."
    try {
        $response = Invoke-WebRequest -Uri $releaseUrl -Method Head -UseBasicParsing -ErrorAction Stop
        Write-Info "从 GitHub Releases 下载..."
        $zipFile = "$env:TEMP\nx-install.zip"
        Download-File $releaseUrl $zipFile
        Expand-Archive -Path $zipFile -DestinationPath $NX_BIN_DIR -Force
        Remove-Item $zipFile -Force
    } catch {
        Write-Info "从仓库源码下载（开发预览版）..."
        Download-File $rawUrl "$NX_BIN_DIR\nx.cmd"
    }
    Write-Info "配置环境变量..."
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$NX_BIN_DIR*") {
        $newPath = if ($currentPath) { "$currentPath;$NX_BIN_DIR" } else { $NX_BIN_DIR }
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        $env:Path = "$env:Path;$NX_BIN_DIR"
        Write-Success "已将 Nx 添加到用户 PATH"
    } else { Write-Info "Nx 已在 PATH 中" }
    Write-Host ""
    Write-Info "验证安装..."
    if (Test-Path "$NX_BIN_DIR\nx.cmd") {
        Write-Success "Nx 已安装: $NX_BIN_DIR\nx.cmd"
        Write-Host ""
        & "$NX_BIN_DIR\nx.cmd" version
        Write-Host ""
        Write-Success "Nx 安装成功！"
        Write-Host ""
        Write-Host "快速开始:" -ForegroundColor Yellow
        Write-Host "  # 创建新项目"
        Write-Host "  nx new my-first-nx-project"
        Write-Host ""
        Write-Host "  # 运行 Nx 脚本"
        Write-Host "  nx run src\main.nx"
        Write-Host ""
        Write-Host "  # 进入交互式解释器"
        Write-Host "  nx repl"
        Write-Host ""
        Write-Host "Nx - 全场景覆盖，双范式统一，AI 原生，全语言生态融合" -ForegroundColor Cyan
        Write-Host ""
    } else { Write-Error "安装验证失败"; exit 1 }
}
Main
