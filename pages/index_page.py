"""首页 Page Object 示例"""
from base.base_page import BasePage


class IndexPage(BasePage):
    """小程序首页"""

    def goto(self):
        """进入首页（通过 switch_tab）并等待页面渲染"""
        self.switch_tab("/pages/home/index")
        self.wait_for_page(3)

    def tap_element_by_text(self, text: str):
        """点击页面上包含指定文本的元素

        Args:
            text: 元素的文本内容
        """
        el = self.get_by_text(text)
        if el:
            el.tap()

    def get_title(self):
        """获取首页标题元素

        Returns:
            标题元素对象，找不到返回 None
        """
        return self.page.get_element("view.title") or self.page.get_element("text.title")
