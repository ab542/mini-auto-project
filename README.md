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

```python
# cases/test_login.py
from base.base_case import BaseCase
from pages.login_page import LoginPage


class TestLogin(BaseCase):
    def test_login_page_loaded(self):
        """验证登录页正常加载"""
        login = LoginPage(self)
        login.goto()
        self.assert_element_exists("#phone-input", "手机号输入框未加载")

    def test_login_success(self):
        """验证登录成功"""
        login = LoginPage(self)
        login.goto()
        login.input_phone("13800138000")
        login.send_verify_code()
        login.input_verify_code("123456")
        login.submit()
        self.assert_text_in_page("欢迎回来", "未跳转到首页")
```

## 断言示例

> 核心原则：**断言结果，而非过程**。不要断言操作成功，断言操作后页面的预期变化。

### 页面加载

```python
self.assert_element_exists("#login-phone", "手机号输入框未加载")
self.assert_element_exists("#send-code-btn", "验证码按钮未加载")
```

### 操作结果

```python
# 断言金额计算正确
freight = order.get_inner_text("#freight-amount")
self.assertTrue(freight and float(freight) >= 0, f"运费异常: {freight}")
```

### Toast 弹窗（一闪而过的提示）

Toast 展示 1-2 秒就消失，等它出现再查找来不及。用 **Hook 拦截** 在底层就抓住它：

```python
# 1. 操作前开启捕获
self.start_capture_toast()

# 2. 触发操作（点击提交空购物车）
cart.tap("#submit-btn")

# 3. 断言捕获到的 Toast 内容
self.assert_toast("购物车为空", "未弹出空购物车提示")
```

原理：`start_capture_toast()` 通过 `app.hook_wx_method("showToast")` 拦截小程序的 `wx.showToast` 调用，把 title 记下来。后续 `get_captured_toast()` 直接读取已记录的内容，不存在"消失找不到"的问题。也支持连续捕获：

```python
self.start_capture_toast()

# 提交 → 弹出"提交成功"
self.tap("#submit-btn")

# 快速连续断言
self.assert_toast("提交成功")
self.assert_toast("即将刷新列表")  # 如果连续弹了两次 Toast
```

### 状态变化

```python
# 选择优惠券 → 断言金额变化
before = order.get_inner_text("#total-price")
order.tap_text("满100减20")
after = order.get_inner_text("#total-price")
self.assertNotEqual(before, after, "优惠后金额未变化")
```

### 列表数据

```python
# 搜索后断言列表非空
items = goods.get_elements(".goods-item")
self.assertGreater(len(items), 0, "搜索结果为空")

# 断言价格升序
prices = goods.get_all_prices()
self.assertGreaterEqual(len(prices), 2, f"商品数不足: {len(prices)}")
self.assertEqual(prices, sorted(prices), f"排序不正确: {prices}")
```

### 页面跳转

```python
home.tap("#banner-0")
self.page.wait_for(3)
current = self.app.get_current_page()
self.assertIn("goods-detail", current.path, f"跳转失败，当前路径: {current.path}")
```

### 常用断言速查

| 场景 | 推荐断言 |
|------|----------|
| 元素存在 | `assert_element_exists(selector)` |
| 文案出现 | `assert_text_in_page(text)` |
| 数值相等 | `assertEqual(a, b)` |
| 数值不等 | `assertNotEqual(a, b)` |
| 大于/大于等于 | `assertGreater(a, b)` / `assertGreaterEqual(a, b)` |
| 列表非空 | `assertGreater(len(list), 0)` |
| 布尔为真 | `assertTrue(condition)` |
| 字符串包含 | `assertIn(sub, full)` |

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
