# progress.json 字段说明

`progress.json` 是唯一的进度数据来源。每轮对话结束后更新它，再运行 `scripts/render.py` 生成 `progress.html`。

## 字段

| 字段 | 说明 |
|---|---|
| `version` | 固定为 `1` |
| `project` | 项目名（中文即可） |
| `slug` | 文件夹名：英文或拼音，小写加连字符 |
| `one_liner` | 一句话需求：帮谁在什么场景解决什么问题 |
| `owner` | 用户的称呼 |
| `started` / `updated` | 开始日期 / 最近更新日期，格式 `YYYY-MM-DD` |
| `current_step` | 当前所在步骤：`0` = 建立档案，1–4 = 四步，四步都完成后写 `5` |
| `profile` | 第 0 步的档案摘要（从 `profile.md` 复制）：`identity` 身份标签、`expertise` 比别人懂的领域、`reach` 能触达的人，各写一两句话 |
| `steps[]` | 四个步骤，顺序固定，见下方 |
| `direction` | 第 1 步：四条标准的打分（每条 0–2，未打分写 `null`）和目标用户 |
| `loops[]` | 第 2 步：最小闭环，`status` 为 `todo` / `doing` / `done` |
| `launch` | 第 3 步：发布记录 `posts[]` 和反馈群 `group` |
| `metrics` | 第 4 步：`uv`、`dau`、`retention`（文字，如“次日 30%”）、`interviews_done`、`interviews_target`（默认 10） |
| `iterations[]` | 第 4 步：每周迭代，`week`、`date`、`note` |
| `first_gold` | 终点：`done`（true / false）、`amount`、`date`、`source` |
| `share_asked` | 是否已经邀请过用户分享进度（只问一次），默认 `false` |
| `log[]` | 每轮对话一行：`date`、`text`，新的追加在末尾 |

### steps[] 中每一项

| 字段 | 说明 |
|---|---|
| `id` | 1–4 |
| `name` | 找方向 / 搭架构 / 宣发拉群 / 反馈迭代 |
| `status` | `not-started` / `in-progress` / `done` / `skipped` |
| `note` | 一句话现状或卡点（可空） |
| `checklist[]` | 过关清单：`text` + `done`（true / false）。不要删改清单项，只改 `done` |
| `outputs[]` | 关键产出：`label` + `path`（相对 progress.json 的路径或网址） |

## 初始模板

新项目时复制这一份，填上 `project`、`slug`、`owner` 和日期：

```json
{
  "version": 1,
  "project": "",
  "slug": "",
  "one_liner": "",
  "owner": "",
  "started": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD",
  "current_step": 0,
  "profile": {"identity": "", "expertise": "", "reach": ""},
  "steps": [
    {
      "id": 1, "name": "找方向", "status": "not-started", "note": "",
      "checklist": [
        {"text": "四条标准打分：前三条每条至少 1 分，总分至少 5 分", "done": false},
        {"text": "写出一句话需求", "done": false},
        {"text": "说出 1 个具体的目标用户", "done": false}
      ],
      "outputs": []
    },
    {
      "id": 2, "name": "搭架构", "status": "not-started", "note": "",
      "checklist": [
        {"text": "有交互 UI 图", "done": false},
        {"text": "有可点击的前端 demo，并且自己确认了流程", "done": false},
        {"text": "拆出至少 3 个最小闭环", "done": false},
        {"text": "第一个闭环跑通", "done": false}
      ],
      "outputs": []
    },
    {
      "id": 3, "name": "宣发拉群", "status": "not-started", "note": "",
      "checklist": [
        {"text": "宣发文案定稿", "done": false},
        {"text": "至少在 1 个渠道发布，并记录了链接", "done": false},
        {"text": "反馈群已经建好", "done": false}
      ],
      "outputs": []
    },
    {
      "id": 4, "name": "反馈迭代", "status": "not-started", "note": "",
      "checklist": [
        {"text": "访问统计已经上线（只看汇总数据）", "done": false},
        {"text": "完成 10 个用户访谈", "done": false},
        {"text": "写完第一份周迭代记录", "done": false}
      ],
      "outputs": []
    }
  ],
  "direction": {
    "scores": [
      {"label": "懂这个领域", "score": null},
      {"label": "真需求且自己会一直用", "score": null},
      {"label": "能触达前 100 个用户", "score": null},
      {"label": "结合热点", "score": null}
    ],
    "target_user": ""
  },
  "loops": [],
  "launch": {"posts": [], "group": {"name": "", "members": 0}},
  "metrics": {"uv": null, "dau": null, "retention": "", "interviews_done": 0, "interviews_target": 10},
  "iterations": [],
  "first_gold": {"done": false, "amount": "", "date": "", "source": ""},
  "share_asked": false,
  "log": []
}
```

## 更新规则

- 档案建好后，把三项写进 `profile`，第 1 步的 `status` 改为 `in-progress`，`current_step` 改为 1。
- 一个步骤的清单全部 `done` 后，把它的 `status` 改为 `done`，下一步改为 `in-progress`，`current_step` 加 1。
- 用户要求跳过时，把 `status` 改为 `skipped`，在 `note` 里写原因。
- 每轮都要更新 `updated`，并在 `log` 里追加一行。
- 访谈数、UV 等数字以用户告诉你的为准，不要估算。
