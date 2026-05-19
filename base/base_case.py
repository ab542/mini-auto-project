"""测试用例基类，封装 setUp/tearDown 通用逻辑"""
import minium


class BaseCase(minium.MiniTest):
    """测试用例基类，继承自 minium.MiniTest

    特性：
    - setUp 时自动处理授权弹窗
    - 提供常用的断言和等待方法
    """

    def setUp(self):
        """每个用例执行前自动调用：初始化并处理授权弹窗"""
        super().setUp()
        self.handle_launch_modal()

    def handle_launch_modal(self):
        """处理小程序启动时的授权弹窗，静默忽略异常"""
        try:
            self.app.allow_authorize()
        except Exception:
            pass

    def wait_and_get_text(self, selector: str, timeout: int = 5):
        """等待元素出现后获取其文本内容

        Args:
            selector: 元素选择器
            timeout: 超时等待秒数，默认 5 秒

        Returns:
            元素的 inner_text，超时或找不到返回空字符串
        """
        el = self.page.wait_for(timeout).get_element(selector)
        return el.inner_text if el else ""

    def assert_element_exists(self, selector: str, msg: str = ""):
        """断言元素存在于当前页面

        Args:
            selector: 元素选择器
            msg: 断言失败时的自定义提示信息
        """
        el = self.page.get_element(selector)
        self.assertTrue(el, msg or f"元素不存在: {selector}")

    def assert_text_in_page(self, text: str, msg: str = ""):
        """断言页面中存在指定文本内容

        Args:
            text: 要查找的文本内容（部分匹配）
            msg: 断言失败时的自定义提示信息
        """
        el = self.page.get_element("text", inner_text=text)
        self.assertTrue(el, msg or f"页面未找到文本: {text}")
