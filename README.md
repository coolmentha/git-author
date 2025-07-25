# Git配置监控器

自动监控指定目录下.git文件夹的创建，并为缺少[user]配置的Git仓库自动添加用户信息。

## 功能特性

- 🔍 **实时监控**: 使用watchdog实时监控.git文件夹的创建
- ⚙️ **配置化管理**: 支持灵活的配置文件管理
- 🚀 **自动配置**: 自动为新Git仓库添加[user]配置
- 📝 **日志记录**: 完整的操作日志和错误记录
- 🛡️ **安全备份**: 修改前自动备份原始配置文件
- 🎯 **智能过滤**: 支持排除特定目录模式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

1. 复制配置模板：
```bash
cp config.example.json config.json
```

2. 编辑 `config.json` 配置文件：

```json
{
  "user": {
    "name": "Your Name",           // Git用户名
    "email": "your.email@example.com"  // Git邮箱
  },
  "monitoring": {
    "directories": [               // 监控的根目录列表
      "C:/Users/kpy/PycharmProjects",
      "D:/Projects"
    ],
    "exclude_patterns": [          // 排除的目录模式
      "*/node_modules/*",
      "*/venv/*",
      "*/.*cache*",
      "*/temp/*"
    ],
    "recursive": true              // 是否递归监控子目录
  },
  "logging": {
    "level": "INFO",               // 日志级别
    "file": "git_monitor.log",     // 日志文件名
    "max_size_mb": 10,             // 日志文件最大大小(MB)
    "backup_count": 5              // 日志备份文件数量
  },
  "behavior": {
    "auto_add_user": true,         // 是否自动添加[user]配置
    "backup_original": true,       // 是否备份原始配置文件
    "notification": true           // 是否显示通知
  }
}
```

## 使用方法

### 方式一：直接运行Python脚本

```bash
python git_monitor.py
```

### 方式二：使用启动脚本（推荐）

项目提供了 `start_monitor.bat` 启动脚本，具有以下优势：
- ✅ **环境检查**：自动检查Python安装和依赖包
- ✅ **配置验证**：自动检查config.json文件是否存在
- ✅ **依赖安装**：自动安装缺失的依赖包
- ✅ **错误处理**：完善的错误检查和提示机制

**Windows系统**：
```cmd
# 双击运行或在命令行执行
start_monitor.bat
```

### 程序运行流程

1. **启动扫描**: 程序启动时会扫描所有配置的监控目录，检查现有的.git文件夹
2. **实时监控**: 使用watchdog监控新.git文件夹的创建
3. **自动配置**: 检测到新的.git文件夹时，自动检查并添加[user]配置
4. **日志记录**: 所有操作都会记录到日志文件中

### 停止监控

按 `Ctrl+C` 停止监控程序。

## Windows服务注册

为了让Git配置监控器在Windows系统启动时自动运行，可以使用NSSM（Non-Sucking Service Manager）将其注册为Windows服务。

### 什么是NSSM

NSSM是一个免费的Windows服务管理工具，可以将任何可执行程序注册为Windows服务，支持自动启动、崩溃重启等功能。

### 下载和安装NSSM

1. **下载NSSM**
   - 访问官网：https://nssm.cc/download
   - 下载最新版本的NSSM压缩包
   - 解压到任意目录（建议：`C:\nssm`）

2. **添加到系统PATH**（可选）
   - 将NSSM目录添加到系统环境变量PATH中
   - 或者直接使用完整路径调用NSSM

### 注册为Windows服务

#### 方法一：使用Python文件直接注册

**使用GUI方式**：
1. **打开NSSM GUI**
   ```cmd
   # 以管理员身份运行命令提示符
   C:\nssm\win64\nssm.exe install GitMonitor
   ```

2. **配置服务参数**
   - **Application Path**: 选择Python解释器路径
     ```
     C:\Python\python.exe
     ```
   - **Startup directory**: 设置为项目目录
     ```
     C:\path\to\your\git-author
     ```
   - **Arguments**: 设置启动参数
     ```
     git_monitor.py
     ```

3. **高级配置**（可选）
   - 切换到"Details"标签页
   - **Display name**: `Git配置监控器`
   - **Description**: `自动监控Git仓库并配置用户信息`
   - **Startup type**: `Automatic`

**使用命令行方式**：
```cmd
# 以管理员身份运行命令提示符

# 注册服务
C:\nssm\win64\nssm.exe install GitMonitor C:\Python\python.exe

# 设置启动目录（请修改为实际项目路径）
C:\nssm\win64\nssm.exe set GitMonitor AppDirectory "C:\path\to\your\git-author"

# 设置启动参数
C:\nssm\win64\nssm.exe set GitMonitor AppParameters git_monitor.py

# 设置服务显示名称
C:\nssm\win64\nssm.exe set GitMonitor DisplayName "Git配置监控器"

# 设置服务描述
C:\nssm\win64\nssm.exe set GitMonitor Description "自动监控Git仓库并配置用户信息"

# 设置自动启动
C:\nssm\win64\nssm.exe set GitMonitor Start SERVICE_AUTO_START
```

#### 方法二：使用现有的start_monitor.bat文件（推荐）

项目已经提供了`start_monitor.bat`启动脚本，可以直接使用NSSM将此批处理文件注册为服务：

**使用GUI方式**：
1. 以管理员身份运行命令提示符
2. 执行：`C:\nssm\win64\nssm.exe install GitMonitor`
3. 在弹出的配置界面中设置：
   - **Application Path**: `C:\Windows\System32\cmd.exe`
   - **Startup directory**: `C:\path\to\your\git-author`
   - **Arguments**: `/c start_monitor.bat`
   - **Display name**: `Git配置监控器`
   - **Description**: `自动监控Git仓库并配置用户信息`

**使用命令行方式**：
```cmd
# 以管理员身份运行命令提示符

# 注册服务，使用cmd.exe执行bat文件
C:\nssm\win64\nssm.exe install GitMonitor C:\Windows\System32\cmd.exe

# 设置启动目录为项目目录（请修改为实际项目路径）
C:\nssm\win64\nssm.exe set GitMonitor AppDirectory "C:\path\to\your\git-author"

# 设置启动参数，使用/c参数执行bat文件后关闭cmd窗口
C:\nssm\win64\nssm.exe set GitMonitor AppParameters "/c start_monitor.bat"

# 设置服务显示名称
C:\nssm\win64\nssm.exe set GitMonitor DisplayName "Git配置监控器"

# 设置服务描述
C:\nssm\win64\nssm.exe set GitMonitor Description "自动监控Git仓库并配置用户信息"

# 设置自动启动
C:\nssm\win64\nssm.exe set GitMonitor Start SERVICE_AUTO_START

# 设置服务日志输出（可选）
C:\nssm\win64\nssm.exe set GitMonitor AppStdout "C:\path\to\your\git-author\service_stdout.log"
C:\nssm\win64\nssm.exe set GitMonitor AppStderr "C:\path\to\your\git-author\service_stderr.log"
```

**使用start_monitor.bat的优势**：
- ✅ **环境检查**：自动检查Python安装和依赖包
- ✅ **配置验证**：自动检查config.json文件是否存在
- ✅ **依赖安装**：自动安装缺失的依赖包
- ✅ **错误处理**：完善的错误检查和提示机制
- ✅ **中文支持**：UTF-8编码支持中文显示

### 服务管理操作

#### 启动服务
```cmd
# 方法1：使用NSSM
C:\nssm\win64\nssm.exe start GitMonitor

# 方法2：使用Windows服务管理
net start GitMonitor

# 方法3：使用PowerShell
Start-Service GitMonitor
```

#### 停止服务
```cmd
# 方法1：使用NSSM
C:\nssm\win64\nssm.exe stop GitMonitor

# 方法2：使用Windows服务管理
net stop GitMonitor

# 方法3：使用PowerShell
Stop-Service GitMonitor
```

#### 重启服务
```cmd
# 使用NSSM
C:\nssm\win64\nssm.exe restart GitMonitor

# 使用PowerShell
Restart-Service GitMonitor
```

#### 查看服务状态
```cmd
# 使用NSSM
C:\nssm\win64\nssm.exe status GitMonitor

# 使用Windows服务管理
sc query GitMonitor

# 使用PowerShell
Get-Service GitMonitor
```

#### 编辑服务配置
```cmd
# 打开NSSM配置界面
C:\nssm\win64\nssm.exe edit GitMonitor
```

#### 删除服务
```cmd
# 首先停止服务
C:\nssm\win64\nssm.exe stop GitMonitor

# 删除服务
C:\nssm\win64\nssm.exe remove GitMonitor confirm
```

### 服务日志配置

NSSM支持重定向程序的输出到日志文件：

```cmd
# 设置标准输出日志
C:\nssm\win64\nssm.exe set GitMonitor AppStdout "C:\path\to\your\git-author\service_stdout.log"

# 设置错误输出日志
C:\nssm\win64\nssm.exe set GitMonitor AppStderr "C:\path\to\your\git-author\service_stderr.log"

# 设置日志轮转（可选）
C:\nssm\win64\nssm.exe set GitMonitor AppStdoutCreationDisposition 4
C:\nssm\win64\nssm.exe set GitMonitor AppStderrCreationDisposition 4
```

### Windows服务故障排除

#### 常见问题

1. **服务无法启动**
   - 检查Python路径是否正确
   - 确保项目目录路径正确
   - 验证config.json文件是否存在
   - 检查文件权限

2. **服务启动后立即停止**
   - 查看Windows事件日志
   - 检查NSSM重定向的日志文件
   - 确认Python脚本可以正常运行

3. **权限问题**
   - 确保服务运行账户有足够权限
   - 可以设置服务使用特定用户账户运行：
   ```cmd
   C:\nssm\win64\nssm.exe set GitMonitor ObjectName ".\username" "password"
   ```

#### 调试步骤

1. **手动测试**
   ```cmd
   # 切换到项目目录
   cd "C:\path\to\your\git-author"

   # 手动运行程序
   python git_monitor.py
   ```

2. **查看服务日志**
   - 检查service_stdout.log和service_stderr.log
   - 查看git_monitor.log应用程序日志

3. **Windows事件日志**
   - 打开"事件查看器"
   - 查看"Windows日志" > "系统"
   - 搜索与GitMonitor相关的事件

### 服务配置最佳实践

1. **环境变量**：如果程序依赖特定环境变量，可以通过NSSM设置
2. **工作目录**：确保AppDirectory设置正确
3. **自动重启**：配置服务在崩溃时自动重启
4. **日志管理**：定期清理日志文件，避免磁盘空间不足

## 工作原理

1. **目录监控**: 使用watchdog库监控指定目录的文件系统事件
2. **事件过滤**: 只处理.git目录的创建事件
3. **配置检查**: 检查.git/config文件是否包含[user]配置
4. **自动添加**: 如果缺少[user]配置，自动添加配置的用户信息
5. **安全备份**: 修改前创建带时间戳的备份文件

## 日志说明

程序会生成详细的日志文件 `git_monitor.log`，包含：

- 监控启动和停止信息
- 检测到的.git目录
- 配置文件的修改操作
- 错误和警告信息

## 注意事项

1. **权限要求**: 确保程序对监控目录和.git/config文件有读写权限
2. **配置备份**: 程序会自动备份原始配置文件，文件名格式为 `config.backup.{timestamp}`
3. **排除规则**: 合理配置排除规则，避免监控不必要的目录
4. **资源占用**: 监控大量目录可能会占用一定的系统资源

## 应用程序故障排除

### 常见问题

1. **配置文件不存在**
   - 确保 `config.json` 文件存在
   - 可以从 `config.example.json` 复制并修改

2. **权限不足**
   - 确保对监控目录有读权限
   - 确保对.git/config文件有写权限

3. **监控目录不存在**
   - 检查配置文件中的目录路径是否正确
   - 确保目录存在且可访问

### 调试模式

修改配置文件中的日志级别为 `DEBUG` 可以获得更详细的调试信息：

```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## 许可证

MIT License
