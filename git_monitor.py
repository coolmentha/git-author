#!/usr/bin/env python3
"""
Git配置监控器
监控指定目录下.git文件夹的创建，自动添加[user]配置
"""

import os
import json
import time
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from logging.handlers import RotatingFileHandler

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)


class GitConfigManager:
    """Git配置管理器"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.log_info(f"配置文件加载成功: {self.config_path}")
            return config
        except FileNotFoundError:
            self.log_error(f"配置文件不存在: {self.config_path}")
            self.log_info("请复制 config.example.json 为 config.json 并修改配置")
            raise
        except json.JSONDecodeError as e:
            self.log_error(f"配置文件格式错误: {e}")
            raise
            
    def setup_logging(self):
        """设置日志"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        
        # 创建logger
        self.logger = logging.getLogger('GitMonitor')
        self.logger.setLevel(level)
        
        # 清除现有handlers
        self.logger.handlers.clear()
        
        # 文件handler
        log_file = log_config.get('file', 'git_monitor.log')
        max_bytes = log_config.get('max_size_mb', 10) * 1024 * 1024
        backup_count = log_config.get('backup_count', 5)
        
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
    def log_info(self, message: str):
        """记录信息日志"""
        if hasattr(self, 'logger'):
            self.logger.info(message)
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} {message}")
        
    def log_warning(self, message: str):
        """记录警告日志"""
        if hasattr(self, 'logger'):
            self.logger.warning(message)
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")
        
    def log_error(self, message: str):
        """记录错误日志"""
        if hasattr(self, 'logger'):
            self.logger.error(message)
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
        
    def is_excluded(self, path: str) -> bool:
        """检查路径是否被排除"""
        exclude_patterns = self.config.get('monitoring', {}).get('exclude_patterns', [])
        path_str = str(path).replace('\\', '/')
        
        for pattern in exclude_patterns:
            if pattern.replace('*', '') in path_str:
                return True
        return False
        
    def has_user_config(self, git_config_path: str) -> bool:
        """检查git config是否已有[user]配置"""
        try:
            with open(git_config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return '[user]' in content
        except Exception as e:
            self.log_error(f"读取git config失败: {git_config_path}, 错误: {e}")
            return False
            
    def backup_config(self, git_config_path: str) -> bool:
        """备份原始配置文件"""
        if not self.config.get('behavior', {}).get('backup_original', True):
            return True
            
        try:
            backup_path = f"{git_config_path}.backup.{int(time.time())}"
            shutil.copy2(git_config_path, backup_path)
            self.log_info(f"配置文件已备份: {backup_path}")
            return True
        except Exception as e:
            self.log_error(f"备份配置文件失败: {e}")
            return False
            
    def add_user_config(self, git_config_path: str) -> bool:
        """添加[user]配置到git config"""
        try:
            user_config = self.config.get('user', {})
            user_name = user_config.get('name', '')
            user_email = user_config.get('email', '')
            
            if not user_name or not user_email:
                self.log_error("配置文件中缺少用户名或邮箱")
                return False
                
            # 备份原文件
            if not self.backup_config(git_config_path):
                return False
                
            # 读取现有内容
            content = ""
            if os.path.exists(git_config_path):
                with open(git_config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
            # 添加[user]配置
            user_section = f"""
[user]
	name = {user_name}
	email = {user_email}
"""
            
            # 写入文件
            with open(git_config_path, 'a', encoding='utf-8') as f:
                if content and not content.endswith('\n'):
                    f.write('\n')
                f.write(user_section)
                
            self.log_info(f"已添加[user]配置到: {git_config_path}")
            self.log_info(f"  name = {user_name}")
            self.log_info(f"  email = {user_email}")
            return True
            
        except Exception as e:
            self.log_error(f"添加[user]配置失败: {e}")
            return False
            
    def process_git_directory(self, git_dir: str):
        """处理.git目录"""
        git_config_path = os.path.join(git_dir, 'config')
        
        if not os.path.exists(git_config_path):
            self.log_warning(f"Git配置文件不存在: {git_config_path}")
            return
            
        if self.has_user_config(git_config_path):
            self.log_info(f"Git配置已包含[user]信息: {git_config_path}")
            return
            
        if self.config.get('behavior', {}).get('auto_add_user', True):
            self.add_user_config(git_config_path)
        else:
            self.log_info(f"检测到缺少[user]配置但未启用自动添加: {git_config_path}")


class GitDirectoryHandler(FileSystemEventHandler):
    """Git目录监控处理器"""
    
    def __init__(self, config_manager: GitConfigManager):
        self.config_manager = config_manager
        
    def on_created(self, event):
        """文件/目录创建事件"""
        if isinstance(event, DirCreatedEvent):
            path = Path(event.src_path)
            
            # 检查是否为.git目录
            if path.name == '.git':
                if self.config_manager.is_excluded(str(path)):
                    self.config_manager.log_info(f"跳过排除的.git目录: {path}")
                    return
                    
                self.config_manager.log_info(f"检测到新的.git目录: {path}")
                
                # 等待一小段时间确保目录完全创建
                time.sleep(0.5)
                
                self.config_manager.process_git_directory(str(path))


class GitMonitor:
    """Git监控器主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_manager = GitConfigManager(config_path)
        self.observers = []
        
    def scan_existing_git_directories(self):
        """扫描现有的.git目录"""
        self.config_manager.log_info("开始扫描现有的.git目录...")
        
        directories = self.config_manager.config.get('monitoring', {}).get('directories', [])
        recursive = self.config_manager.config.get('monitoring', {}).get('recursive', True)
        
        for directory in directories:
            if not os.path.exists(directory):
                self.config_manager.log_warning(f"监控目录不存在: {directory}")
                continue
                
            self.config_manager.log_info(f"扫描目录: {directory}")
            
            if recursive:
                for root, dirs, files in os.walk(directory):
                    if '.git' in dirs:
                        git_path = os.path.join(root, '.git')
                        if not self.config_manager.is_excluded(git_path):
                            self.config_manager.process_git_directory(git_path)
            else:
                git_path = os.path.join(directory, '.git')
                if os.path.exists(git_path) and not self.config_manager.is_excluded(git_path):
                    self.config_manager.process_git_directory(git_path)
                    
        self.config_manager.log_info("现有.git目录扫描完成")
        
    def start_monitoring(self):
        """开始监控"""
        directories = self.config_manager.config.get('monitoring', {}).get('directories', [])
        recursive = self.config_manager.config.get('monitoring', {}).get('recursive', True)
        
        if not directories:
            self.config_manager.log_error("未配置监控目录")
            return
            
        handler = GitDirectoryHandler(self.config_manager)
        
        for directory in directories:
            if not os.path.exists(directory):
                self.config_manager.log_warning(f"监控目录不存在，跳过: {directory}")
                continue
                
            observer = Observer()
            observer.schedule(handler, directory, recursive=recursive)
            observer.start()
            self.observers.append(observer)
            
            self.config_manager.log_info(f"开始监控目录: {directory} (递归: {recursive})")
            
    def stop_monitoring(self):
        """停止监控"""
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.observers.clear()
        self.config_manager.log_info("监控已停止")
        
    def run(self):
        """运行监控器"""
        try:
            self.config_manager.log_info("Git配置监控器启动")
            self.config_manager.log_info(f"配置文件: {self.config_manager.config_path}")
            
            # 扫描现有目录
            self.scan_existing_git_directories()
            
            # 开始监控
            self.start_monitoring()
            
            if not self.observers:
                self.config_manager.log_error("没有有效的监控目录，程序退出")
                return
                
            self.config_manager.log_info("监控运行中，按 Ctrl+C 停止...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.config_manager.log_info("收到停止信号")
                
        except Exception as e:
            self.config_manager.log_error(f"运行时错误: {e}")
        finally:
            self.stop_monitoring()
            self.config_manager.log_info("Git配置监控器已停止")


def main():
    """主函数"""
    try:
        monitor = GitMonitor()
        monitor.run()
    except Exception as e:
        print(f"{Fore.RED}启动失败: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
