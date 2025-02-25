import pytest
import os
import yaml
from ngstoolkits.config import Config

@pytest.fixture
def config_file(tmp_path):
    """创建测试配置文件"""
    config_path = tmp_path / "config.yaml"
    config_data = {
        'reference': '/path/to/test/reference.fa',
        'bam': '/path/to/test/sample.bam'
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    
    return str(config_path)

def test_config_from_env():
    """测试从环境变量加载配置"""
    os.environ['NGSTOOLKITS_REFERENCE'] = '/env/path/reference.fa'
    os.environ['NGSTOOLKITS_BAM'] = '/env/path/sample.bam'
    
    config = Config()
    assert config.reference == '/env/path/reference.fa'
    assert config.bam == '/env/path/sample.bam'
    
    # 清理环境变量
    del os.environ['NGSTOOLKITS_REFERENCE']
    del os.environ['NGSTOOLKITS_BAM']

def test_config_from_file(config_file, monkeypatch):
    """测试从文件加载配置"""
    # 模拟配置文件路径
    monkeypatch.setattr('os.path.exists', lambda x: x == config_file)
    
    config = Config()
    assert config.reference == '/path/to/test/reference.fa'
    assert config.bam == '/path/to/test/sample.bam'

def test_config_priority(config_file, monkeypatch):
    """测试配置优先级"""
    # 设置环境变量
    os.environ['NGSTOOLKITS_REFERENCE'] = '/env/path/reference.fa'
    
    # 模拟配置文件
    monkeypatch.setattr('os.path.exists', lambda x: x == config_file)
    
    config = Config()
    assert config.reference == '/env/path/reference.fa'  # 环境变量优先
    assert config.bam == '/path/to/test/sample.bam'  # 从配置文件加载
    
    # 清理环境变量
    del os.environ['NGSTOOLKITS_REFERENCE'] 