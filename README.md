# Nx Programming Language - 官方下载

Nx 是一个全场景覆盖、双范式统一、AI 原生、全语言生态融合的新型编程语言。

## 特性

- **全场景覆盖** - 从内核驱动到 AI 大模型，一种语言贯穿全栈
- **双范式统一** - 面向过程与面向对象无缝切换
- **AI 原生** - 意图驱动编程，intent 关键字用自然语言描述功能
- **全语言生态融合** - 统一 import 语法直接调用 Python/Java/C++/JS/Go/Rust 生态
- **Hindley-Milner 类型推断** - 无需繁琐类型声明，编译期类型安全
- **零成本抽象 + 内存安全** - 借鉴 Rust 所有权模型与 Go 并发原语
- **极简主义** - 摒弃样板代码，新手几分钟上手

## 快速安装

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/231ljk/midownload/main/install.ps1 | iex
```

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/231ljk/midownload/main/install.sh | bash
```

### 验证安装

```bash
nx version
nx help
```

## 快速开始

```bash
# 创建新项目
nx new my-first-nx-project

# 进入项目
cd my-first-nx-project

# 运行程序
nx run src/main.nx

# 进入交互式解释器
nx repl
```

## 代码示例

```nx
// Nx Programming Language - Hello World
// 双范式统一：面向过程 + 面向对象

func greet(name) {
    print("Hello, " + name + "! Welcome to Nx!")
}

class Circle : Shape {
    var radius
    func init(radius) { this.radius = radius }
    func area() { return pi * this.radius * this.radius }
}

func main() {
    greet("Developer")
    circle = Circle(10)
    print("Area: " + circle.area())
    print("Nx program ran successfully!")
}

main()
```

## 项目结构

```
midownload/
├── index.html          # 官方下载页面
├── README.md           # 项目说明
├── install.sh          # Linux/macOS 安装脚本
├── install.ps1         # Windows PowerShell 安装脚本
├── bin/
│   ├── nx              # Nx 命令行工具 (Linux/macOS)
│   └── nx.cmd          # Nx 命令行工具 (Windows)
└── examples/
    └── hello.nx        # Nx 示例代码
```

## 支持平台

| 平台 | 直接下载 | 命令安装 |
|------|---------|---------|
| Windows 10/11 | ✅ 安装脚本 | ✅ PowerShell / winget |
| Linux (x86_64/ARM64) | ✅ 安装脚本 | ✅ curl / wget |
| macOS (Intel/Apple Silicon) | ✅ 安装脚本 | ✅ curl / Homebrew |
| Docker | - | ✅ docker pull |
| Android (Termux) | - | ✅ curl |
| HarmonyOS 鸿蒙 | 开发中 | 开发中 |

## Nx 命令

```
nx new <项目名>     创建新的 Nx 项目
nx run <文件.nx>    运行 Nx 脚本
nx build <文件.nx>  编译 Nx 程序
nx test             运行测试
nx deps             管理依赖
nx fmt              格式化代码
nx doc              生成文档
nx repl             进入交互式解释器
nx version          显示版本信息
nx help             显示帮助信息
```

## 技术栈

- 编译器前端：Rust（内存安全 + 高性能）
- IR 与优化器：LLVM 基础设施
- 类型系统：扩展的 Hindley-Milner 算法
- 并发模型：Actor + CSP 混合模型
- 内存管理：GC + 手动管理双轨制
- 代码生成：C/C++ / RISC-V / x86_64 多后端

## 版本信息

- **当前版本**：v0.1.0 (Developer Preview)
- **许可证**：MIT License
- **仓库**：https://github.com/231ljk/midownload

## 路线图

### v0.1.0 (已发布)
- 基础语法：变量、函数、控制流
- 面向对象：类、继承、接口、泛型、Mixin
- Hindley-Milner 类型推断引擎
- 标准库：List、Dict、Tuple、Set、String
- 编译器流水线：Lexer → Parser → AST → IR → CodeGen
- 跨平台安装脚本

### v0.2.0 (规划中)
- AI 意图驱动编程（intent 关键字）
- 全语言生态融合（Python/Java/C++/JS/Go/Rust）
- 并发模型：async/await + Actor + CSP
- 内存管理：GC + 手动管理双轨制

### v1.0.0 (规划中)
- 生产就绪稳定版
- 操作系统开发支持
- 智能家居 IoT 协议栈
- AI 项目一键开发脚手架
- 积木-代码双向映射系统

## 贡献

欢迎参与 Nx 语言的开发！您可以：

1. 提交 Issue 报告 Bug 或提出功能建议
2. 提交 PR 贡献代码
3. 编写文档和教程
4. 分享使用经验和最佳实践

## 许可证

MIT License
