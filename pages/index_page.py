"""首页 Page Object — 封装底部 tab 切换及首页元素操作"""
from base.base_page import BasePage


class IndexPage(BasePage):
    """小程序首页，同时作为底部 tab 导航的入口"""

    # ========== 底部 tab 切换 ==========

    def goto(self):
        """切换到首页 tab"""
        self.switch_tab("/pages/home/index")
        self.wait_for_page(3)

    def goto_message(self):
        """切换到消息 tab"""
        self.switch_tab("/pages/message/index")
        self.wait_for_page(2)

    def goto_my(self):
        """切换到我的 tab"""
        self.switch_tab("/pages/my/index")
        self.wait_for_page(2)

    def goto_testpage(self):
        """切换到 TEST 页 tab"""
        self.switch_tab("/pages/testpage/index")
        self.wait_for_page(2)

    # ========== 首页元素操作 ==========

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
