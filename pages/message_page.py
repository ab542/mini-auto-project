"""消息页 Page Object"""
from base.base_page import BasePage


class MessagePage(BasePage):
    """全部消息页"""

    def goto(self):
        """通过底部 tab 切换到消息页"""
        self.switch_tab("/pages/message/index")
        self.wait_for_page(3)

    def get_message_list(self):
        """获取消息列表所有项

        Returns:
            t-cell 元素列表，列表为空时返回空列表
        """
        return self.page.get_elements("t-cell")

    def tap_first_message(self):
        """点击第一条消息，进入聊天对话页

        Returns:
            True 点击成功，False 列表为空无法点击
        """
        items = self.get_message_list()
        if not items:
            return False
        items[0].tap()
        return True

    def tap_message_by_index(self, index: int):
        """点击第 N 条消息（从 0 开始）

        Args:
            index: 消息索引，0 为第一条

        Returns:
            True 点击成功，False 索引越界
        """
        items = self.get_message_list()
        if index >= len(items):
            return False
        items[index].tap()
        return True

    def get_first_message_name(self) -> str:
        """获取第一条消息的联系人名称

        Returns:
            title 文本内容，列表为空返回空字符串
        """
        items = self.get_message_list()
        if not items:
            return ""
        return items[0].inner_text or ""
