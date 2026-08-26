---
id: generated-artifact-manual-edit-drift
type: recurring-finding
status: open
occurrences: 1
first_seen: 2026-08-26
last_seen: 2026-08-26
links:
  - openspec/changes/ant-grasshopper-storybook/reviews/propose-r1.md
---

# 產出物被手改而未回寫產生器

由腳本或模板產生的檔案被直接手動修改，修改未回寫到產生器；下一次重新產生時這些修改會無聲倒退。

規劃變更時若只讀產出物的現值、把它當成「現況」，就會寫出「維持現況不變」這種在重新產生後不成立的敘述。判斷產出物是否與其產生器同步，要看產生器本身，並用 `git show --stat` 確認當初的手改 commit 涵蓋哪些檔案。

## Occurrences

- 2026-08-26 — `ant-grasshopper-storybook`（cash-propose，round 1，F-1，Critical）：commit `4114ad5` 的四項 UI 調整只手改 `index.html`，未回寫 `generate_audio.py` 的 HTML 模板。提案原本寫「速度控制維持現況不變」，但本變更會由模板重新產生 `index.html`，照該敘述實作會讓速度按鈕退回三顆、預設退回 0.75、冒出已被移除的中文播放按鈕，直接違反同一提案自己寫下的兩條 SHALL。
