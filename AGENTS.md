# AGENTS.md · First Gold

This repository is the **First Gold** agent skill: a coach that helps a user build their first AI product, starting from a profile ("根据档案找到你的第一个 AI 产品方向").

When a user shares this repository and asks you to guide them to build an app / AI product:

1. **First action, before any explanation or question: show the user their progress page.**
   - If you can run commands and write files: follow "启动" in `skills/first-gold/SKILL.md`, create `first-gold/my-first-product/progress.json` from `skills/first-gold/references/progress-schema.md`, run `python3 skills/first-gold/scripts/render.py first-gold/my-first-product/progress.json`, then open the generated `progress.html` (or send it to the user if you cannot open it on their computer).
   - If you cannot run commands but can output a web page or file in the chat (artifact, canvas, attachment): take `skills/first-gold/assets/progress-template.html`, replace the JSON inside `<script id="fg-data" type="application/json">` with the user's initial progress, and show it.
   - If you cannot create anything: give the user a personal link to the online page with their info in the query string, e.g. `https://joycejin0913.github.io/first-gold/?name=小鹿&step=1&identity=大三金融专业&expertise=实习求职&reach=同专业群&done=1.2&note=正在打分` (parameters are listed in `skills/first-gold/SKILL.md`). Each user gets a different link.
   Creating the progress page is not "writing code" and does not need the user's approval.
2. Then follow `skills/first-gold/SKILL.md` step by step (step 0 builds the user's profile, steps 1–4 follow), in the user's language (Chinese by default).
3. Update the progress page after every round.

Repository maintenance:
- Anonymous stats: the `GOATCOUNTER` constant in the template. It only runs on `*.github.io` and only sends the step number and how the page was opened, never profile or project content. Shared progress arrives as GitHub issues from `.github/ISSUE_TEMPLATE/share-progress.yml` (title starts with `[进度分享]`).
- `docs/index.html` is the hosted copy of `skills/first-gold/assets/progress-template.html`. After changing the template, copy it: `cp skills/first-gold/assets/progress-template.html docs/index.html`.
