# 工作日美术教育晨报

这是一个面向中国一线美术教师的日更自动化项目。

## 目标

- 每个工作日生成一份“美术教育教学最新资讯晨报”
- 优先覆盖近 7 天的政策、教研、展览、AI 教育和论文动态
- 输出可直接给教师阅读和转发的中文摘要

## 当前结构

- `automation.toml`：Codex 自动化定义
- `scripts/run_daily_report.py`：本地 / CI 统一入口，调用 Codex 生成日报
- `.github/workflows/daily-report.yml`：GitHub Actions 定时任务
- `outputs/`：生成结果输出目录

## 两种运行方式

### 1. Codex Cloud

适合你希望把“检索 + 生成 + 汇总”都交给 Codex 云端执行的场景。

你可以直接把 `automation.toml` 作为自动化定义使用。

### 2. GitHub Actions

适合你希望每天固定时间自动跑，并把结果留在仓库、再通过 GitHub 手机通知接收的场景。

推荐做法：

- 让 Action 生成 `outputs/latest.md`
- 再把日报写回仓库，或者写到一个专用 Issue 评论里
- GitHub 手机端收到通知后即可查看

## 需要配置的环境变量

- `OPENAI_API_KEY`：Codex CLI 登录用
- `REPORT_ISSUE_NUMBER`：可选。设置后，Workflow 会把日报摘要写到该 Issue 评论里，便于手机推送

## 下一步

如果你要我继续，我可以把这套内容直接整理成一个可推送的 GitHub 仓库，并补上：

- 仓库初始化
- 首次提交
- 远程地址配置
- GitHub Actions 推送回写

