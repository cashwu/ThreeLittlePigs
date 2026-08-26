---
id: proposal-claim-without-spec-coverage
type: recurring-finding
status: open
occurrences: 1
first_seen: 2026-08-26
last_seen: 2026-08-26
links:
  - openspec/changes/ant-grasshopper-storybook/reviews/propose-r1.md
---

# proposal 宣稱的範圍未被任何 requirement 或 task 涵蓋

proposal 的 Summary 或 Proposed Solution 宣稱了某項改變，但沒有任何 spec requirement 或 task 交付它，導致實作完成後該項改變並未發生。

大範圍的內容替換特別容易漏掉週邊元素：標題、副標、頁面 metadata、範例資料、錯誤訊息中的字串。檢查方式是把 proposal 的每一句宣稱逐一回推到某條 requirement 與某條 task。

## Occurrences

- 2026-08-26 — `ant-grasshopper-storybook`（cash-propose，round 1，F-2，Warning，兩位 reviewer 獨立提出）：proposal 明講內容從《Three Little Pigs》換成《The Ant and The Grasshopper》，Impact 也列出 `index.html` 由腳本重新產生，但四份 spec 與全部 task 都沒有涵蓋 `<title>`、`<h1>` 與副標，重新產生後頁面標題仍會是舊繪本。
