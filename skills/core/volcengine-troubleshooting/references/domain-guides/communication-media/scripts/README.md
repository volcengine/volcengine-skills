# Scripts

当前首版没有默认脚本。

## 何时新增

- 一个问题需要多接口联动才能判断。
- 单个 SDK 返回过深、分页过多或很难稳定回归。
- 需要把多个媒体阶段汇总成 `summary` / `findings`。

## 固定约束

- 只读。
- 优先读取 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_SESSION_TOKEN`。
- 明确声明 SDK 来源与调用 Action。
- 不在脚本里发送短信、呼叫、推流、禁流、创建或删除资源。
