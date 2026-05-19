"""测试用例基类，封装 setUp/tearDown 通用逻辑"""
import minium


class BaseCase(minium.MiniTest):
    """测试用例基类，继承自 minium.MiniTest

    特性：
    - setUp 时自动处理授权弹窗
    - 提供常用的断言和等待方法
    - 提供 Toast 捕获方法（解决 Toast 一闪而过的断言问题）
    """

    def setUp(self):
        """每个用例执行前自动调用：初始化并处理授权弹窗"""
        super().setUp()
        self.handle_launch_modal()
        self._toast_messages = []       # 存放捕获到的 toast 内容

    def handle_launch_modal(self):
        """处理小程序启动时的授权弹窗，静默忽略异常"""
        try:
            self.app.allow_authorize()
        except Exception:
            pass

    # ========== Toast 捕获 ==========

    def start_capture_toast(self):
        """开始捕获 Toast

        通过 Hook wx.showToast 将每次弹窗的 title 记录下来，
        解决 Toast 一闪而过来不及断言的问题。

        用法：
            self.start_capture_toast()        # 操作前调用
            cart.tap("#submit-btn")           # 触发操作
            self.assert_toast("购物车为空")      # 断言捕捉到的 Toast
        """
        self._toast_messages = []

        def on_show_toast(args):
            title = args.get("title", "")
            if title:
                self._toast_messages.append(title)

        try:
            self.app.hook_wx_method("showToast", on_show_toast)
        except Exception:
            pass

    def get_captured_toast(self) -> str:
        """获取最近一次捕获的 Toast 内容

        Returns:
            Toast 文本，没有捕获到返回空字符串
        """
        return self._toast_messages[0] if self._toast_messages else ""

    def assert_toast(self, expected: str, msg: str = ""):
        """断言弹出了指定内容的 Toast（需先调用 start_capture_toast）

        Args:
            expected: 期望的 Toast 内容
            msg: 断言失败时的自定义提示信息
        """
        captured = self.get_captured_toast()
        self.assertTrue(
            expected in captured,
            msg or f"Toast 断言失败，期望'{expected}'，实际'{captured}'"
        )

    # ========== 等待与查找 ==========

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

    # ========== 断言 ==========

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
