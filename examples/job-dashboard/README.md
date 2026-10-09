# Job Dashboard：合成文档快照

[返回中文 README](../../README.md) · [Back to English README](../../README.en.md)

这是匿名合成的文档快照，展示规格、任务与裁决如何记录。团队、用户、任务和路径均为演示数据；文档里的批准、完成状态和测试数字不是本仓库可重新运行的证据。仓库未包含该案例所描述的应用源码、合同文件或测试。

需要运行真实命令并检查失败裁决时，请使用 [Java 独立验收示例](../java-acceptance/README.md)。它提供离线、确定性的 verifier replay，不需要模型或 API 密钥。

## 初始请求

> 为运维人员增加一个 Job Dashboard：能够查看后台任务、按状态筛选，并正确处理加载中、空结果和失败状态。请让前后端并行开发，但最终要由主 Agent 验收。

这个请求看似清楚，实际仍有四个关键空缺：合法状态集合、非法状态行为、前后端共享合同、以及“页面完成”的可观察证据。流程先检查现有 `JobStore` 和测试约定，再冻结以下决定：

- 状态集合固定为 `all`、`queued`、`running`、`failed`；
- 非法状态返回结构化 400 错误；
- API 合同版本固定为 1；
- 实现使用 Python 标准库和原生 JavaScript，不新增依赖；
- 写操作、认证、数据库、实时推送和部署不在本轮范围。

## 权威文档

| 文档 | 本例中的作用 |
| --- | --- |
| [PRD.md](PRD.md) | 冻结目标、范围、功能需求与产品决定 |
| [TECH_DESIGN.md](TECH_DESIGN.md) | 冻结 API、页面状态、文件边界和测试策略 |
| [ACCEPTANCE.md](ACCEPTANCE.md) | 将四项需求映射为四个阻塞验收项 |
| [AGENT_PLAN.md](AGENT_PLAN.md) | 后端和前端并行、主 Agent 串行集成验收 |
| [LOOP.md](LOOP.md) | 保存实现证据、裁决、风险和最终状态 |

## 冻结后执行

```text
TASK-001 backend/jobs_api.py + backend unit tests ─┐
                                                    ├─► TASK-003 main-agent integration and judgment
TASK-002 frontend/index.html + app.js + unit tests ─┘
```

共享合同、既有存储和验收测试均为只读输入。两个实现任务没有写入重叠，因此可并行；主 Agent 等待二者完成后独立检查文件边界、冻结输入哈希和完整测试门槛。

## 文档所描述的最终验收快照

| AC | 结果 | 证据摘要 | 缺口 |
| --- | --- | --- | --- |
| AC-001 列表与筛选 | Pass | 单元与合同测试覆盖 `None`、`all` 和全部合法状态 | 无 |
| AC-002 非法筛选 | Pass | `paused` 返回 400 / `INVALID_STATUS`，存储未变化 | 无 |
| AC-003 页面状态 | Pass | 静态合同测试覆盖筛选、表格、加载、空结果和错误容器；JS 语法检查通过 | 未做真实网络 E2E，非冻结阻塞项 |
| AC-004 只读与集成 | Pass | 冻结输入哈希不变、无文件越权、完整门槛 14/14 通过 | 无 |

快照中记录的主 Agent 裁决：**ACCEPTED**。这不是对当前仓库运行测试所得的结论。

这个例子刻意保留了一个非阻塞风险。独立验收不是把结果包装成完美，而是明确区分“已证明”“未证明”和“是否阻塞发布”。
