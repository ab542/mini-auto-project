"""Page Object 基类，封装通用页面操作"""
import time


class BasePage:
    """页面对象基类，所有 Page Object 继承此类"""

    def __init__(self, mini):
        """
        Args:
            mini: minium 实例 / BaseCase 实例（self）
        """
        self.mini = mini

    @property
    def app(self):
        """minium 应用对象，用于页面跳转、Mock 等"""
        return self.mini.app

    @property
    def page(self):
        """minium 页面对象，用于元素查找、等待等"""
        return self.mini.page

    @property
    def native(self):
        """minium 原生控件对象，用于处理弹窗、授权等"""
        return self.mini.native

    def navigate_to(self, route: str):
        """保留当前页跳转（非 tab 页面用此方法跳转）

        Args:
            route: 页面路径，如 '/pages/detail/detail?id=1'
        """
        self.app.navigate_to(route)

    def redirect_to(self, route: str):
        """关闭当前页跳转（替换当前页面，无法返回）

        Args:
            route: 页面路径
        """
        self.app.redirect_to(route)

    def switch_tab(self, route: str):
        """跳转到 tabBar 页面

        Args:
            route: tab 页面路径，如 '/pages/index/index'
        """
        self.app.switch_tab(route)

    def wait_for_page(self, seconds: int = 3):
        """等待页面渲染完成

        Args:
            seconds: 等待秒数，默认 3 秒
        """
        self.page.wait_for(seconds)

    def get_by_text(self, inner_text: str):
        """通过文本内容定位单个元素

        Args:
            inner_text: 元素的文本内容（部分匹配）

        Returns:
            minium 元素对象，找不到返回 None
        """
        return self.page.get_element("text", inner_text=inner_text)

    def get_by_selector(self, selector: str):
        """通过 CSS 选择器定位单个元素

        Args:
            selector: CSS 选择器，如 '.my-class'、'#my-id'

        Returns:
            minium 元素对象
        """
        return self.page.get_element(selector)

    def get_elements(self, selector: str):
        """通过 CSS 选择器获取元素列表

        Args:
            selector: CSS 选择器

        Returns:
            元素列表，找不到返回空列表
        """
        return self.page.get_elements(selector)

    def screenshot(self, name: str = None):
        """截取当前页面截图，保存到 outputs 目录

        Args:
            name: 截图文件名（不含 .png 后缀），默认使用时间戳
        """
        if name is None:
            name = f"screenshot_{int(time.time())}"
        self.mini.capture(f"{name}.png")

    # ========== 元素点击 ==========

    def tap(self, selector: str):
        """点击元素（CSS 选择器定位）

        Args:
            selector: CSS 选择器，如 '.btn'、'#submit'
        """
        self.get_by_selector(selector).tap()

    def tap_text(self, inner_text: str):
        """点击包含指定文本的元素

        Args:
            inner_text: 元素的文本内容（部分匹配）
        """
        self.get_by_text(inner_text).tap()

    def longpress(self, selector: str, duration: int = 500):
        """长按元素

        Args:
            selector: CSS 选择器
            duration: 长按持续时间（ms），默认 500
        """
        self.get_by_selector(selector).longpress(duration=duration)

    # ========== 文本输入 ==========

    def input(self, selector: str, value: str):
        """向输入框输入文本

        Args:
            selector: 输入框元素的选择器
            value: 要输入的文本内容
        """
        self.get_by_selector(selector).input(value)

    def input_clear(self, selector: str):
        """清空输入框

        Args:
            selector: 输入框元素的选择器
        """
        self.get_by_selector(selector).input_clear()

    def input_confirm(self, selector: str):
        """确认输入（回车 / 点击完成按钮）

        Args:
            selector: 输入框元素的选择器
        """
        self.get_by_selector(selector).input_confirm()

    # ========== 滚动 ==========

    def scroll_to_element(self, selector: str):
        """滚动页面直到元素可见

        Args:
            selector: 元素选择器
        """
        self.get_by_selector(selector).scroll_to()

    def scroll_to(self, top: int = None, bottom: int = None):
        """滚动页面到指定位置

        Args:
            top: 距离顶部的像素值
            bottom: 距离底部的像素值
        """
        if top is not None:
            self.page.scroll_to(top=top)
        elif bottom is not None:
            self.page.scroll_to(bottom=bottom)

    def slide(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """手指滑动操作（如切换 tab、滑动列表）

        Args:
            start_x: 起始 X 坐标
            start_y: 起始 Y 坐标
            end_x: 结束 X 坐标
            end_y: 结束 Y 坐标
        """
        self.page.slide(start_x, start_y, end_x, end_y)

    # ========== 元素信息 ==========

    def get_inner_text(self, selector: str) -> str:
        """获取元素文本内容

        Args:
            selector: 元素选择器

        Returns:
            元素的 inner_text
        """
        return self.get_by_selector(selector).inner_text

    def get_attribute(self, selector: str, attr: str) -> str:
        """获取元素属性值

        Args:
            selector: 元素选择器
            attr: 属性名，如 'class'、'id'、'data-key'

        Returns:
            属性值
        """
        return self.get_by_selector(selector).attribute(attr)

    def get_element_rect(self, selector: str) -> dict:
        """获取元素的位置和尺寸

        Args:
            selector: 元素选择器

        Returns:
            {'left': int, 'top': int, 'width': int, 'height': int}
        """
        return self.get_by_selector(selector).offset

    # ========== 状态判断 ==========

    def is_visible(self, selector: str) -> bool:
        """判断元素是否可见

        Args:
            selector: 元素选择器

        Returns:
            True 可见，False 不可见（或元素不存在）
        """
        el = self.get_by_selector(selector)
        return el.visible if el else False

    def is_enabled(self, selector: str) -> bool:
        """判断元素是否可用

        Args:
            selector: 元素选择器

        Returns:
            True 可用，False 不可用
        """
        el = self.get_by_selector(selector)
        return el.enabled if el else False

    # ========== 弹窗 ==========

    def handle_native_modal(self):
        """处理原生弹窗（如授权弹窗），无需授权时不会报错"""
        try:
            self.native.handle_modal()
        except Exception:
            pass
