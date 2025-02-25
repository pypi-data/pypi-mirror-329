import os
import yaml
from typing import Dict, Optional

class Config:
    """配置管理类，用于处理全局配置。
    
    支持从配置文件或环境变量加载配置信息。
    配置优先级：函数参数 > 环境变量 > 配置文件 > 默认值
    """
    
    _instance = None
    _config: Dict = {
        'reference': None,
        'bam': None
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """加载配置信息"""
        # 1. 首先尝试从环境变量加载
        if 'NGSTOOLKITS_REFERENCE' in os.environ:
            self._config['reference'] = os.environ['NGSTOOLKITS_REFERENCE']
        if 'NGSTOOLKITS_BAM' in os.environ:
            self._config['bam'] = os.environ['NGSTOOLKITS_BAM']
            
        # 2. 然后尝试从配置文件加载
        config_paths = [
            os.path.expanduser('~/.ngstoolkits/config.yaml'),  # 用户目录
            '/etc/ngstoolkits/config.yaml',  # 系统目录
            os.path.join(os.getcwd(), 'ngstoolkits_config.yaml')  # 当前目录
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                with open(path) as f:
                    try:
                        file_config = yaml.safe_load(f)
                        if file_config:
                            # 只更新None的值
                            for key in self._config:
                                if self._config[key] is None and key in file_config:
                                    self._config[key] = file_config[key]
                    except yaml.YAMLError:
                        continue
    
    @property
    def reference(self) -> Optional[str]:
        """获取参考基因组路径"""
        return self._config['reference']
    
    @property
    def bam(self) -> Optional[str]:
        """获取BAM文件路径"""
        return self._config['bam']
    
    def set_reference(self, path: str):
        """设置参考基因组路径"""
        self._config['reference'] = path
    
    def set_bam(self, path: str):
        """设置BAM文件路径"""
        self._config['bam'] = path

# 全局配置实例
config = Config() 