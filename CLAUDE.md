# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Launch dev tool + run all tests
venv\Scripts\python run_tests.py

# Run tests (dev tool must be already running on auto-port 9420)
pytest
pytest cases/test_message.py                     # Single file
pytest -m smoke                                  # Smoke tests only
pytest -k "test_click_first_message_to_chat"     # Single test by name
pytest -n 2                                      # Parallel (requires pytest-xdist)

# Test report: outputs/report.html
```

## Architecture

This is a **WeChat Mini Program UI automation** project using the official [Minium](https://minitest.weixin.qq.com/#/minium/Python/introduction/quick_start) framework + pytest. Tests run against the WeChat Developer Tool (IDE mode), not real devices.

### Fixture chain (conftest.py)

```
mini_config (session) → mini (session) ─┬→ mini_page (function)
                                        └→ mini_app (function)
```

- `mini_config`: reads `config.json`, session-scoped so it's loaded once.
- `mini`: creates the `minium.Minium` instance (connects to dev tool on `auto_port`), yields it, then calls `shutdown()`.
- `mini_page` / `mini_app`: thin function-scoped aliases to `mini.page` and `mini.app`.

### Test class hierarchy

```
minium.MiniTest  (framework base — provides self.app, self.page, self.native)
  └─ BaseCase (base/base_case.py)
       ├─ Toast capture (start_capture_toast / assert_toast)
       ├─ Common assertions (assert_element_exists, assert_text_in_page)
       └─ wait_and_get_text helper
```

Each test class inherits `BaseCase` and calls `self.page` / `self.app` directly. The `mini` / `page` / `app` fixtures from conftest are **not used directly by tests** — `BaseCase` wires its own via minium's framework machinery.

### Page Object pattern

```
BasePage (base/base_page.py)
  ├─ IndexPage (pages/index_page.py)    — bottom tab switching + home page ops
  ├─ MessagePage (pages/message_page.py) — message list + click-to-chat
  └─ ... (new pages added here)
```

BasePage wraps `self.page` (minium.Page) behind convenience methods (`tap`, `input`, `get_inner_text`, etc.) and takes either a `mini` instance or `BaseCase` instance in its constructor. Page objects access `self.app`, `self.page`, `self.native` via properties that delegate to `self.mini`.

### Toast capture mechanism

Toast notifications disappear in 1–2 seconds, too fast for normal element queries. The solution (in `BaseCase`):
1. `start_capture_toast()` calls `self.app.hook_wx_method("showToast", callback)` before the triggering action.
2. The callback records `args["title"]` into `self._toast_messages` at the JS layer — no timing race.
3. `assert_toast("expected text")` checks the captured list.

### Element selector fallback pattern

When a component library (e.g. TDesign) renders complex nested structures, the preferred selector (like a custom element tag) may not work. The convention in this project is multi-strategy fallback with a debug helper:
- Try the specific component selector first (`.message-list t-cell`), fall back to generic tags (`view`).
- If the list is empty, call `debug_page_structure()` to print the actual DOM tree for diagnosis before failing the assertion.

## Code style

**Every method must have a docstring** explaining parameters (Args:) and return value (Returns:). Key steps get inline comments. This is a project requirement, not optional.
