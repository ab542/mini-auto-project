"""消息模块测试用例"""
from base.base_case import BaseCase
from pages.index_page import IndexPage
from pages.message_page import MessagePage


class TestMessage(BaseCase):
    """消息模块"""

    def test_click_first_message_to_chat(self):
        """验证点击第一条消息能进入聊天对话页"""
        # 1. 切换到消息 tab
        index = IndexPage(self)
        index.goto_message()

        # 2. 操作消息列表
        msg = MessagePage(self)
        message_list = msg.get_message_list()

        # 列表为空时打印页面结构，方便定位问题
        if not message_list:
            msg.debug_page_structure()

        self.assertTrue(
            len(message_list) > 0,
            "消息列表为空，无法测试点击跳转——查看上方 DEBUG 输出确认元素渲染结构"
        )

        # 记录第一条消息的联系人名称
        first_name = msg.get_first_message_name()

        # 3. 点击第一条消息
        result = msg.tap_first_message()
        self.assertTrue(result, "点击消息列表失败")
        self.page.wait_for(3)

        # 4. 断言进入了聊天页（页面包含刚才点击的联系人名称）
        self.assert_text_in_page(
            first_name,
            f"未跳转到聊天页，期望联系人'{first_name}'未出现在页面"
        )
