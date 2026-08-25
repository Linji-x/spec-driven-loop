# Job Dashboard 产品需求

Status: Frozen  
Owner: Product owner  
Approval: Approved for implementation  
Example type: Anonymized synthetic case

## 产品目标

让运维人员在一个只读页面查看后台任务，并按状态筛选，以便快速发现排队、运行和失败任务。

## 用户与主要流程

- 主要用户：负责检查后台任务健康度的运维人员。
- 进入页面时默认加载全部任务。
- 用户可切换状态筛选；页面更新为对应集合。
- 页面必须明确展示加载中、无结果或请求失败，而不是留白。

## 功能需求

| FR ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| FR-001 | 提供只读任务列表接口，可返回全部任务或按 `queued`、`running`、`failed` 筛选。 | Must | Frozen |
| FR-002 | 提供浏览器页面，展示任务 ID、标题和状态，并允许用户选择状态筛选。 | Must | Frozen |
| FR-003 | 页面明确呈现加载中、空结果和请求失败状态。 | Must | Frozen |
| FR-004 | 后端与前端共同遵守版本 1 的冻结 API 合同。 | Must | Frozen |

## 范围

In scope：只读接口、静态浏览器页面、后端/前端/集成自动化测试。

Out of scope：新建、取消或重试任务；身份认证；持久化数据库；实时推送；生产部署。

## 业务规则

- 状态筛选固定为 `all`、`queued`、`running`、`failed`。
- `all` 与未提供状态含义相同。
- 非法状态返回结构化 400 错误，不改变任何存储数据。
- 任意筛选重复请求均为只读且幂等。

## 成功指标

- FR-001 至 FR-004 均有至少一项自动化验收证据。
- 完整测试门槛通过；冻结合同在实现期间未变化。

## 决策日志

| Decision | Result | Reason |
| --- | --- | --- |
| D-001 状态集合 | 四个固定值 | 防止前后端各自扩展语义 |
| D-002 非法状态 | 结构化 400 | 让调用方可确定处理 |
| D-003 技术依赖 | Python 标准库 + 原生 JS | 与示例仓库约束一致 |
