"""pytest 配置文件，定义 minium 相关的 fixtures"""
import json
import os
import pytest
import minium


def load_config():
    """加载 config.json 配置文件

    Returns:
        配置字典
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def mini_config():
    """session 级别的配置 fixture，整个测试会话共享"""
    return load_config()


@pytest.fixture(scope="session")
def mini(mini_config):
    """session 级别的 minium 实例 fixture

    整个测试会话中只创建一次，所有用例共享同一个连接。
    会话结束时自动调用 shutdown() 释放资源。

    Args:
        mini_config: 由 mini_config fixture 注入的配置

    Yields:
        minium.Minium 实例
    """
    m = minium.Minium(
        project_path=mini_config["project_path"],
        dev_tool_path=mini_config["dev_tool_path"],
        platform=mini_config.get("platform", "ide"),
        debug_mode=mini_config.get("debug_mode", "debug"),
        auto_port=mini_config.get("auto_port", 9420),
        request_timeout=mini_config.get("request_timeout", 60),
    )
    yield m
    m.shutdown()


@pytest.fixture
def mini_page(mini):
    """function 级别的 page fixture，每个用例独立的 page 引用

    Args:
        mini: 由 mini fixture 注入的 minium 实例

    Returns:
        minium.Page 对象
    """
    return mini.page


@pytest.fixture
def mini_app(mini):
    """function 级别的 app fixture，每个用例独立的 app 引用

    Args:
        mini: 由 mini fixture 注入的 minium 实例

    Returns:
        minium.App 对象
    """
    return mini.app
