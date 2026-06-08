"""消息页 Page Object"""
from base.base_page import BasePage


class MessagePage(BasePage):
    """全部消息页"""

    def goto(self):
        """通过底部 tab 切换到消息页"""
        self.switch_tab("/pages/message/index")
        self.wait_for_page(3)

    def debug_page_structure(self):
        """调试用：打印 message-list 容器内子元素的结构

        运行测试失败时先调此方法，确认实际渲染结构。
        """
        container = self.page.get_element(".message-list")
        if not container:
            print("[DEBUG] .message-list 容器未找到")
            return

        children = container.get_elements("*")
        print(f"[DEBUG] .message-list 下共 {len(children)} 个子元素：")
        for el in children[:3]:       # 只打印前 3 个，避免刷屏
            print(f"  tag={el.tag_name}, text={el.inner_text[:80]}")

        # 有数据时再往下探一层，看第一个 item 的内部结构
        if children:
            sub = children[0].get_elements("*")
            print(f"[DEBUG] 第一个 item 内部子元素 ({len(sub)} 个)：")
            for s in sub[:5]:
                print(f"    tag={s.tag_name}, class={s.attribute('class')[:40]}, text={s.inner_text[:50]}")

    def get_message_list(self):
        """获取消息列表所有项——优先按组件层级定位，失败时回退到 view 标签

        Returns:
            元素列表，列表为空时返回空列表
        """
        # 策略2：退化为普通 view
        return self.page.get_elements(".message-list view")

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
        """
        items = self.get_message_list()
        if not items:
            return ""

        first = items[0]

        # TDesign 渲染 title 的内部 class
        title = first.get_element("view.t-cell__title-text")
        # 最终兜底
        return title.inner_text
    
