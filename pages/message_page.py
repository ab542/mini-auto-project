"""消息页 Page Object"""
from base.base_page import BasePage


class MessagePage(BasePage):
    """全部消息页"""

    def goto(self):
        """通过底部 tab 切换到消息页"""
        self.switch_tab("/pages/message/index")
        self.wait_for_page(3)

    def debug_page_structure(self):
        """调试用：打印 message-list 容器内的子元素标签及文本

        运行测试失败时先调此方法，确认实际渲染结构。
        """
        container = self.page.get_element(".message-list")
        if not container:
            print("[DEBUG] .message-list 容器未找到")
            return

        children = container.get_elements("*")
        print(f"[DEBUG] .message-list 下共 {len(children)} 个子元素：")
        for el in children[:5]:       # 只打印前 5 个，避免刷屏
            print(f"  tag={el.tag_name}, text={el.inner_text[:50]}")

    def get_message_list(self):
        """获取消息列表所有项——优先按组件层级定位，失败时回退到 view 标签

        Returns:
            元素列表，列表为空时返回空列表
        """
        # 策略1：TDesign t-cell 标签（渲染后通常保留标签名）
        items = self.page.get_elements(".message-list t-cell")
        if items:
            return items

        # 策略2：TDesign 编译后可能退化为 view
        items = self.page.get_elements(".message-list view")
        if items:
            return items

        # 策略3：更宽泛的子元素匹配
        return self.page.get_elements(".message-list > *")

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
            文本内容（title 部分），列表为空返回空字符串
        """
        items = self.get_message_list()
        if not items:
            return ""
        # t-cell 组件的 title 被渲染在内部，取整个元素的 inner_text
        return items[0].inner_text or ""
