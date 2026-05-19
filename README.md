# 小程序自动化测试 (Minium + pytest)

基于微信官方 [Minium](https://minitest.weixin.qq.com/#/minium/Python/introduction/quick_start) 框架 + pytest 的小程序 UI 自动化测试项目。

## 环境要求

| 依赖 | 版本 |
|------|------|
| Python | >= 3.8 |
| 微信开发者工具 | [稳定版下载](https://developers.weixin.qq.com/miniprogram/dev/devtools/stable.html) |
| 微信公共库 | >= 2.7.3 |

## 快速开始

### 1. 创建虚拟环境并安装依赖

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. 配置 config.json

```json
{
  "project_path": "你的小程序项目路径（包含 app.json）",
  "dev_tool_path": "微信开发者工具 cli.bat 路径",
  "platform": "ide",
  "auto_port": 9420,
  "debug_mode": "debug"
}
```

### 3. 开启开发者工具安全模式

微信开发者工具 → 设置 → 安全设置 → **服务端口：打开**

### 4. 运行测试

**方式一：一键运行（自动拉起开发者工具）**

```bash
venv\Scripts\python run_tests.py
```

**方式二：手动启动开发者工具后运行**

```bash
# 终端 1：启动开发者工具自动化端口
"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" auto --project "项目路径" --auto-port 9420

# 终端 2：运行测试
venv\Scripts\python -m pytest
```

**常用 pytest 命令**

```bash
# 运行所有测试
pytest

# 运行指定文件
pytest cases/test_demo.py

# 按标记运行（冒烟测试）
pytest -m smoke

# 并发运行（需先装 pytest-xdist）
pytest -n 2

# 查看测试报告
# 报告生成在 outputs/report.html，用浏览器打开即可
```

## 项目结构

```
├── config.json            # 框架配置
├── conftest.py            # pytest fixtures（mini, mini_page, mini_app）
├── pytest.ini             # pytest 配置
├── run_tests.py           # 一键启动脚本
├── requirements.txt       # Python 依赖
├── base/                  # 基类
│   ├── base_page.py       # Page Object 基类
│   └── base_case.py       # 测试用例基类
├── pages/                 # Page Object 页面封装
│   └── index_page.py      # 首页 PO 示例
├── cases/                 # 测试用例
│   └── test_demo.py       # 示例用例
└── outputs/               # 测试报告输出
```

## 编写测试用例

### 方式一：pytest 风格（推荐）

```python
import pytest

@pytest.mark.smoke
def test_index_page_load(mini):
    """验证首页正常加载"""
    mini.app.switch_tab("/pages/index/index")
    mini.page.wait_for(3)
    assert mini.page.get_element("view.container")


@pytest.mark.p0
def test_navigation(mini):
    """验证页面跳转"""
    mini.app.navigate_to("/pages/detail/detail")
    mini.page.wait_for(3)
    assert mini.page.get_element("text", inner_text="详情")
```

### 方式二：Page Object 模式

```python
from base.base_case import BaseCase
from pages.index_page import IndexPage

class TestIndex(BaseCase):
    def test_index_title(self):
        index = IndexPage(self)
        index.goto()
        self.assert_text_in_page("首页")
```

### 方式三：unittest / MiniTest 风格

```python
import minium

class MyTest(minium.MiniTest):
    def test_something(self):
        self.page.wait_for(3)
        self.assertIsNotNone(self.page.get_element("button"))
```

## 元素定位速查

```python
# 文本内容定位
page.get_element("text", inner_text="提交")

# CSS 选择器
page.get_element(".my-class")
page.get_element("#my-id")

# 标签选择器
page.get_element("button")
page.get_element("input")

# 获取元素列表
page.get_elements(".item")

# 等待元素出现
page.wait_for(5).get_element(".loading")
```

## 元素操作

### 点击与触摸

```python
el.tap()                     # 点击元素
el.longpress(duration=500)   # 长按（ms）
el.tap_by_coordinate(x, y)   # 坐标点击
```

### 输入

```python
el.input("文本内容")          # 输入文本
el.input_clear()             # 清空输入框
el.input_confirm()           # 确认输入（回车/完成）
el.trigger("input", {"value": "xxx"})  # 触发 input 事件
```

### 滚动

```python
page.scroll_to(top=200)      # 滚动页面到指定位置
page.scroll_to(bottom=200)   # 滚动到底部附近
el.scroll_to()               # 滚动到元素可见
```

### 元素信息

```python
el.inner_text                # 元素文本内容
el.value                     # 元素值（input 等表单元素）
el.attribute("class")        # 获取属性值
el.tag_name                  # 标签名
el.offset                    # 元素位置 {left, top, width, height}
```

### 元素状态

```python
el.enabled                   # 是否可用
el.visible                   # 是否可见
el.selected                  # 是否选中
```

### 手势操作

```python
el.touchstart()              # 手势开始
el.touchmove()               # 手势移动
el.touchend()                # 手势结束
page.slide(start_x, start_y, end_x, end_y)  # 滑动
```

## 页面操作

| 方法 | 说明 |
|------|------|
| `app.navigate_to(route)` | 保留当前页跳转 |
| `app.redirect_to(route)` | 关闭当前页跳转 |
| `app.switch_tab(route)` | 跳转 TabBar 页面 |
| `app.navigate_back()` | 返回上一页 |
| `app.re_launch(route)` | 重启小程序并跳转 |
| `app.get_current_page()` | 获取当前页面对象 |
| `page.wait_for(seconds)` | 页面等待（秒） |
| `page.set_data(data)` | 直接设置页面 data |
| `page.call_method(method, *args)` | 调用页面方法 |

## 弹窗与原生控件

```python
native.handle_modal(text=None)         # 处理授权弹窗
native.allow_authorize(answer=True)     # 授权弹窗（允许/拒绝）
native.choose_media(count=1)            # 选择媒体文件
native.handle_location(callback_id)     # 处理定位弹窗
```

## Mock & Hook

```python
app.mock_wx_method("getLocation", result={"latitude": 22.5})  # Mock 微信 API
app.restore_wx_method("getLocation")                           # 恢复 Mock
app.hook_wx_method("request", callback_fn)                      # Hook 微信 API
```

## 截图

```python
mini.capture("screenshot.png")         # 截图保存到 outputs
page.screenshot("page.png")            # 页面截图
el.screenshot("element.png")           # 元素截图
```

## 参考资源

- [Minium 官方文档](https://minitest.weixin.qq.com/#/minium/Python/introduction/quick_start)
- [官方 Demo](https://git.weixin.qq.com/minitest/minitest-demo)
- [微信开发者工具下载](https://developers.weixin.qq.com/miniprogram/dev/devtools/stable.html)
