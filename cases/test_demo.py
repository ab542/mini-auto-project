"""示例测试用例 — PO 模式"""
from base.base_case import BaseCase
from pages.index_page import IndexPage


class DemoTest(BaseCase):
    """演示测试用例"""

    def test_launch_miniprogram(self):
        """验证小程序能正常启动"""
        self.page.wait_for(5)
        self.assertTrue(self.app, "小程序启动失败")

    def test_index_page_loaded(self):
        """验证首页能够加载"""
        index = IndexPage(self)          # 创建首页 PO 对象
        index.goto()                     # 跳转到首页
        self.assert_element_exists("view", "首页未加载")
