# Job Dashboard 验收合同

Status: Frozen  
Based on: Approved `PRD.md` and `TECH_DESIGN.md`  
Release blockers: AC-001 through AC-004

## Definition of Done

冻结合同未修改；新增实现有明确且不重叠的文件所有权；完整 `unittest` 门槛通过；主 Agent 独立检查实际 diff、文件清单和测试输出。

## AC-001 — 列表与筛选

- Related FRs: FR-001, FR-004
- Blocking: Yes
- Action: 分别传入 `None`、`all`、`queued`、`running` 和 `failed`。
- Expected: 返回 200、合同版本头和正确集合；筛选集合只含目标状态。
- Required evidence: 后端单元测试与冻结合同测试输出。

## AC-002 — 非法筛选

- Related FRs: FR-001, FR-004
- Blocking: Yes
- Action: 传入 `paused`。
- Expected: 返回 400 和 `INVALID_STATUS`；调用前后存储快照相同。
- Required evidence: 自动化测试输出和只读断言。

## AC-003 — 页面呈现与状态

- Related FRs: FR-002, FR-003, FR-004
- Blocking: Yes
- Action: 检查初始加载、状态切换、空响应和失败响应。
- Expected: 页面存在冻结的控件、表格和状态容器；每个状态互斥；任务文本安全呈现；请求路径符合 API v1。
- Required evidence: 前端静态合同测试、单元测试和 JavaScript 语法检查。

## AC-004 — 集成、冻结和所有权

- Related FRs: FR-001 through FR-004
- Blocking: Yes
- Action: 主 Agent 检查冻结输入哈希、实际变更文件和完整门槛。
- Expected: 冻结输入未变化；每个实现文件归属一个任务；所有测试通过。
- Required evidence: SHA-256 清单、`git diff --name-only`、完整测试输出。

## 验收矩阵模板

| AC | Evidence owner | Pass condition |
| --- | --- | --- |
| AC-001 | Main agent | 合法集合和版本合同全部通过 |
| AC-002 | Main agent | 错误合同与只读断言通过 |
| AC-003 | Main agent | 页面状态与 JS 检查通过 |
| AC-004 | Main agent | 哈希、所有权和完整门槛通过 |
