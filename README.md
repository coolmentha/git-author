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

### 启动监控器

```bash
python git_monitor.py
```

### 程序运行流程

1. **启动扫描**: 程序启动时会扫描所有配置的监控目录，检查现有的.git文件夹
2. **实时监控**: 使用watchdog监控新.git文件夹的创建
3. **自动配置**: 检测到新的.git文件夹时，自动检查并添加[user]配置
4. **日志记录**: 所有操作都会记录到日志文件中

### 停止监控

按 `Ctrl+C` 停止监控程序。

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

## 故障排除

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
