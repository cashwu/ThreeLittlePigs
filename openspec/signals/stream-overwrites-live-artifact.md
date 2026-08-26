---
id: stream-overwrites-live-artifact
type: recurring-finding
status: open
occurrences: 1
first_seen: 2026-08-26
last_seen: 2026-08-26
links:
  - openspec/changes/ant-grasshopper-storybook/reviews/apply-r1.md
---

# 串流直接覆寫正式產物，失敗時破壞目前可用版本

長時間或外部網路串流若直接以截斷模式開啟正式產物，中途失敗會留下空檔或半成品，使原本可用的 consumer 立即失效。當 contract 要求失敗時維持目前版本可用，應先寫入同檔案系統的 staging，待完整集合成功後再發布正式檔案，並用故障注入驗證正式產物 byte-for-byte 不變。

## Occurrences

- 2026-08-26 — `ant-grasshopper-storybook`（cash-apply，round 1，Warning）：edge-tts 直接串流至正式 MP3，網路中斷會截斷舊 `index.html` 正在引用的音檔；改為 50 句全部 staging 成功後才發布。
