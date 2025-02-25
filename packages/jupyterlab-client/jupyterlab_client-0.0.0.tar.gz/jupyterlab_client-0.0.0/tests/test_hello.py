from jupyterlab_client import hello


def test_hello():
    """测试 hello 函数是否返回预期的问候语"""
    assert hello() == "Hello from jupyterlab-client!"
