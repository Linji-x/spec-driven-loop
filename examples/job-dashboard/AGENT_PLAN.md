# Job Dashboard Agent 计划

Status: Frozen  
Specification approval: `PRD.md`, `TECH_DESIGN.md`, `ACCEPTANCE.md` approved  
Shared contract: `contracts/jobs-api.json` version 1  
Plan owner: Main agent

## 冻结共享输入

| Contract / input | Location | Change rule |
| --- | --- | --- |
| Jobs API v1 | `contracts/jobs-api.json` | 所有实现任务只读 |
| Acceptance gate | `tests/test_acceptance_contract.py` | 所有实现任务只读 |
| Existing store | `backend/job_store.py` | 本轮不得修改 |

## 依赖图

`TASK-001` 与 `TASK-002` 只共同读取冻结合同，因此可以并行。`TASK-003` 必须等待两者完成，由主 Agent 串行集成与验收。

## 所有权映射

| Task | Allowed writes | Forbidden writes | Overlap |
| --- | --- | --- | --- |
| TASK-001 Backend | `backend/jobs_api.py`, `tests/test_jobs_api_unit.py` | 其余路径 | None |
| TASK-002 Frontend | `frontend/index.html`, `frontend/app.js`, `tests/test_frontend_unit.py` | 其余路径 | None |
| TASK-003 Judge | `docs/spec-driven/job-dashboard/LOOP.md` | 冻结规格、合同、验收输入和实现文件 | Main agent only |

## TASK-001 — 后端只读列表

- Objective: 按 Jobs API v1 实现 `get_jobs(status, store)`。
- Related: FR-001, FR-004; AC-001, AC-002, AC-004。
- Required checks: 合法状态、非法状态、版本头、只读行为。
- Completion report: 实际变更文件、定向测试命令/输出、风险；不得自行声称验收通过。

## TASK-002 — 浏览器页面

- Objective: 实现筛选、任务表格和 loading/empty/error 状态。
- Related: FR-002, FR-003, FR-004; AC-003, AC-004。
- Required checks: DOM 合同、请求路径、状态互斥、安全文本渲染、JS 语法。
- Completion report: 实际变更文件、定向检查输出、风险；不得修改共享合同。

## TASK-003 — 主 Agent 集成与裁决

- Objective: 不修改实现，通过独立证据判定 AC-001 至 AC-004。
- Steps:
  1. 检查实际 diff 与所有权；
  2. 重算冻结输入 SHA-256；
  3. 运行所有定向检查和完整门槛；
  4. 逐项填写验收矩阵；
  5. 若失败，只下发与具体 AC 绑定的返工；若需求变化，回到规格审批。
- Output: 仅更新 `LOOP.md`。
