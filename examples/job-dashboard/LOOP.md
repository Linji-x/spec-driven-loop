# Job Dashboard 交付循环

Current state: accepted  
Current loop: LOOP-001  
Frozen specification: PRD, technical design, acceptance contract, Jobs API v1  
Blocking issue: None  
Next action: Deliver accepted result

## LOOP-001

- Objective: 完成 FR-001 至 FR-004，并为 AC-001 至 AC-004 生成独立验收证据。
- Assignments: TASK-001 后端；TASK-002 前端；TASK-003 主 Agent 集成与裁决。
- Files changed: `backend/jobs_api.py`, `frontend/index.html`, `frontend/app.js`, two unit-test files, this loop record.
- Checks executed: 两组定向 `unittest`、完整 `unittest discover`、`node --check`、冻结输入哈希、文件所有权和跨模块合同检查。
- Agent reports: 后端 5/5 定向测试通过；前端 5/5 定向测试通过。报告仅作为证据输入。
- Main-agent rerun: 完整门槛 `Ran 14 tests` / `OK`；JavaScript 语法退出码 0；冻结输入哈希未变化；无越权文件。
- Unresolved risk: 未执行真实浏览器网络 E2E。冻结合同只要求静态合同测试和主 Agent 文件检查，因此不阻塞本轮。
- Main-agent judgment: ACCEPTED
- Next state: accepted

## 主 Agent 验收矩阵

| Acceptance ID | Result | Evidence | Defect / caveat |
| --- | --- | --- | --- |
| AC-001 | Pass | 冻结验收与后端测试覆盖 `None`、`all` 和三个合法状态；完整门槛通过 | None |
| AC-002 | Pass | `paused` 返回 400 / `INVALID_STATUS`，调用前后存储相同 | None |
| AC-003 | Pass | 静态合同测试验证筛选、Jobs 表格、三类状态、请求路径与文本渲染；JS 检查通过 | 未做真实网络 E2E，非阻塞 |
| AC-004 | Pass | 冻结输入哈希不变；变更文件符合所有权；14/14 完整门槛通过 | None |

## Evidence notes

- 哈希值属于一次合成测试运行，不应被复制为其他项目的验收证据。
- 真正项目应在此记录完整命令、退出码、关键输出与证据文件路径。
- 如果实现任务改变了合同语义，结果必须是 `REQUIRES_SPEC_CHANGE`，而不是继续修补代码。
