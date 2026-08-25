# Job Dashboard 技术设计

Status: Frozen  
Based on: Approved `PRD.md`  
Contract version: Jobs API v1

## 整体方案

- 既有 `backend/job_store.py` 保持只读，不改变存储职责。
- 新建 `backend/jobs_api.py`，暴露 `get_jobs(status, store)`，返回 `(status_code, headers, body)`。
- `status` 为 `None` 或 `all` 时返回全部任务；合法状态只返回对应任务；非法状态返回冻结合同规定的 400 错误。
- 新建 `frontend/index.html` 和 `frontend/app.js`；页面通过 `fetch` 请求 `/api/jobs?status=<value>`，默认 `all`。
- 共享合同保存为 `contracts/jobs-api.json`，实现任务只能读取。

## API v1

成功响应：

```json
{
  "items": [
    {"id": "job-001", "title": "Build report", "status": "running"}
  ]
}
```

- HTTP 200；响应头包含 `X-Contract-Version: 1`。
- 每项只包含 `id`、`title`、`status`。
- 非法状态返回 HTTP 400 与 `{"error":{"code":"INVALID_STATUS"}}`。

## 页面合同

- 筛选控件 ID：`status-filter`。
- 结果表格：`aria-label="Jobs"`。
- 状态容器：`loading-state`、`empty-state`、`error-state`。
- 新请求先显示 loading；成功后只显示结果或 empty；失败时只显示 error。

## 并发、数据与安全

功能完全只读，不引入新数据生命周期。任务标题必须通过 DOM 文本节点渲染，不使用未转义 `innerHTML`。同一筛选重复请求不会改变后端状态。

## 文件边界

| Slice | Write set |
| --- | --- |
| Backend | `backend/jobs_api.py`, `tests/test_jobs_api_unit.py` |
| Frontend | `frontend/index.html`, `frontend/app.js`, `tests/test_frontend_unit.py` |
| Main agent | `LOOP.md` only |

## 验证与回滚

- 定向单元测试：`python -m unittest tests.test_jobs_api_unit -v` 与 `python -m unittest tests.test_frontend_unit -v`。
- 完整门槛：`python -m unittest discover -s tests -v`。
- JavaScript：`node --check frontend/app.js`。
- 回滚：移除新增 API/UI 文件；不得修改现有存储、冻结合同或验收测试。
