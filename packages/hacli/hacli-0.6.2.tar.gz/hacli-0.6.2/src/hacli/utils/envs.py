import os
from pathlib import Path
from typing import Dict, Any

import yaml


def convert_to_env_vars(config_dict: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
    """
    将嵌套的配置字典转换为扁平化的环境变量字典。

    此函数递归处理嵌套的字典结构，生成符合环境变量命名规范的键值对。
    键名会自动转换为大写，并使用下划线连接层级关系。

    Args:
        config_dict: 要转换的配置字典
        prefix: 环境变量前缀，用于处理嵌套结构

    Returns:
        Dict[str, str]: 转换后的环境变量字典

    Examples:
        >>> config = {"app": {"name": "myapp", "port": 8080}}
        >>> convert_to_env_vars(config)
        {'APP_NAME': 'myapp', 'APP_PORT': '8080'}
    """
    env_vars = {}

    for key, value in config_dict.items():
        if isinstance(value, dict):
            # 递归处理嵌套字典
            nested_vars = convert_to_env_vars(value, prefix + key.upper() + "_")
            env_vars.update(nested_vars)
        else:
            # 将所有值转换为字符串
            env_vars[prefix + key.upper()] = str(value)

    return env_vars


def load_yaml_env_vars() -> None:
    """
    从 YAML 配置文件加载环境变量。

    从用户主目录下的配置文件 ~/.config/hacli/setting.yaml 读取配置，
    并将其转换为环境变量。配置文件支持嵌套结构，会自动转换为扁平化的环境变量。

    Raises:
        FileNotFoundError: 当配置文件不存在时抛出
        yaml.YAMLError: 当 YAML 文件格式错误时抛出

    配置文件示例:
        ```yaml
        project:
          name: myproject
          version: 1.0.0
        azure:
          devops:
            org: myorg
            pat: xxx
        ```

    将转换为环境变量:
        PROJECT_NAME=myproject
        PROJECT_VERSION=1.0.0
        AZURE_DEVOPS_ORG=myorg
        AZURE_DEVOPS_PAT=xxx
    """
    config_path = Path.home() / ".config" / "hacli" / "setting.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在：{config_path}\n"
            f"请创建配置文件并设置必要的配置项"
        )

    try:
        with config_path.open('r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            if not config:
                return

            env_vars = convert_to_env_vars(config)
            os.environ.update(env_vars)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"配置文件格式错误：{e}")
