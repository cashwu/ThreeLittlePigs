---
id: fix-propagation-incomplete
type: recurring-finding
status: open
occurrences: 2
first_seen: 2026-08-26
last_seen: 2026-08-26
links:
  - openspec/changes/ant-grasshopper-storybook/reviews/propose-r2.md
  - openspec/changes/ant-grasshopper-storybook/reviews/propose-r3.md
---

# 修正只改了被指出的那一處，未傳播到同一概念的其他出現處

審查修正只套用在 reviewer 指出的位置，同一個概念在其他 artifact 或同一 artifact 其他段落的敘述沒有跟著改，結果是修正本身製造出新的矛盾或漏洞。

這類缺陷的特徵是：修正當下看起來完整，問題出在「宣稱」與「未同步的舊敘述」之間，或出在同一規則在不同 artifact 的措辭範圍不一致（限定詞落差）。防法是對修正觸及的每個識別字、規則、數字，grep 全部 artifact 並在同一次修正中一併同步，而非只改被 flag 的那一行。

## Occurrences

- 2026-08-26 — `ant-grasshopper-storybook`（cash-propose，round 2，V-1，Warning，`fix-introduced`）：為消除雙索引風險而新增的 Decision 宣稱「跨頁流水計數器完全消失」，但同一份 `design.md` 的 tab Decision 仍要求維持 `en-words-<globalIdx>` 這個全域流水 DOM id，計數器並未消失，兩個 Decision 互斥。
- 2026-08-26 — `ant-grasshopper-storybook`（cash-propose，round 3，R3-1，Warning，`fix-introduced`）：孤兒檔清除的範圍在 `design.md` 寫「所有不屬於本次結果的**英文**音檔」，而 spec 與 tasks 寫「所有…音檔」。前一輪把人工刪除舊音檔的步驟移除、全權交給腳本之後，這個限定詞落差使 9 個實際存在的中文音檔失去負責者，三處驗收條件都會失敗。
