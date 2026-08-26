# Cash Propose Review — Round 1

## Reviewer Findings

彙整自兩位平行 reviewer（Reviewer A — Adherence、Reviewer B — Quality），依 `location + summary` 去重後套用 confidence filter。

### Critical

**F-1**（Reviewer A）
- `severity`: Critical
- `confidence`: 100
- `layer`: design
- `location`: `design.md` → `## Context` 第 3 點與 `## Implementation Contract` → Behavior；`proposal.md` → `## Non-Goals` 第 5 點
- `summary`: design 宣稱「規格與實作的落差只有中文音檔」，但 commit `4114ad5` 的三項 UI 調整全部只手改在 `index.html`、從未回寫 `generate_audio.py` 的 HTML 模板；本變更會由模板重新產生 `index.html`，「維持現況不變」的敘述會直接導致這些調整被復原。
- `recommendation`: 改寫 design Context 說明模板落後的四個項目，把 proposal Non-Goals 的措辭從「不調整」改為「不改變使用者可見結果，但需回寫模板」，並在 tasks 中明列模板要回寫的目標值與驗證。
- 主 agent 已獨立驗證：`git show --stat 4114ad5` 顯示 `1 file changed`（只有 `index.html`）；`generate_audio.py` 模板現值為 `慢2倍`/`慢1倍`/`正常` 三顆、`let playbackRate = 0.75;`、中文播放按鈕未註解、`.zh-text` 無 `margin-left`。

### Warning

**F-2**（Reviewer A `confidence` 75 與 Reviewer B `confidence` 90 各自獨立提出，合併取 90）
- `severity`: Warning
- `confidence`: 90
- `layer`: design
- `location`: `proposal.md` → `## Impact`；`tasks.md` → 第 4 節；`design.md` → Acceptance criteria；`specs/practice-webpage/spec.md`
- `summary`: 沒有任何 spec requirement 或 task 涵蓋網頁的 `<title>`、`<h1>` 與副標，重新產生後的 `index.html` 仍會是《Three Little Pigs》與 `Ryan - pig 2`。
- `recommendation`: 在 `practice-webpage` delta 加入標題需求，並在 tasks 與驗收清單中涵蓋；副標的去留需求方拍板。

### Suggestion

以下皆為 `confidence` 落在 [50, 80) 而由 confidence filter 自 Warning 降級為 Suggestion，或 reviewer 原本即歸為 Suggestion。全部為非阻塞。

**F-3**（Reviewer A，原 Warning `confidence` 75 → 降級）
- `layer`: design ／ `location`: `specs/audio-generation/spec.md` ADDED 需求 vs `design.md` `## Decisions` 與 `tasks.md`
- `summary`: spec 規定「空行 SHALL 一律結束一個句子」，但 design 的分句 Decision 完全沒提這條規則，tasks 也沒有交付或驗證它；這是影響句數的獨立變因。
- `recommendation`: design 補上段落邊界強制斷句，tasks 補一項「段落結尾標點後接小寫開頭」的驗證實例。

**F-4**（Reviewer B，原 Warning `confidence` 70 → 降級）
- `layer`: design ／ `location`: `design.md` `## Failure modes` 與音檔命名 Decision；`tasks.md` 舊檔刪除
- `summary`: 沒有任何 artifact 定義誰在何時清掉過時音檔，而頁面內流水號的設計理由恰恰預設未來會改單頁內容造成句數變動，會留下永久孤兒檔且無任何檢查會發現。
- `recommendation`: spec 加一條「產生後清除不屬於本次結果的音檔」，驗收改為「`audio/` 恰等於本次產生集合」而非寫死 50。

**F-5**（Reviewer B，原 Warning `confidence` 60 → 降級）
- `layer`: design ／ `location`: `design.md` 分句 Decision；`specs/audio-generation/spec.md`；`tasks.md` 1.1
- `summary`: 分句規則依賴引號字元，但沒有規定 `story.md` 用直引號還是彎引號，而 task 要求「原樣謄打繪本」；謄打成 `he cried. “And` 會讓關鍵句界失效，fail-fast 雖會擋下但錯誤訊息指不到真正原因。
- `recommendation`: 明訂一律 ASCII 直引號，並在 tasks 1.1 加彎引號檢查。

**F-6**（Reviewer A `confidence` 50 與 Reviewer B `confidence` 60 合併）
- `layer`: design ／ `location`: `tasks.md` 2.1 與 2.2 的驗證欄
- `summary`: tasks 在驗證欄裡引入了 `--dry-run` 這個 CLI 旗標，但它不存在於 design 的 Implementation Contract 也不存在於任何 spec；它與 `story.json` 的用途重疊，且「是否寫出 `story.json`」語意未定義。
- `recommendation`: 刪掉 `--dry-run`，改以檢視 `story.json` 驗證分句結果。

**F-7**（Reviewer A `confidence` 50 與 Reviewer B `confidence` 55 合併）
- `layer`: text ／ `location`: `tasks.md` 3.2 與 4.6 的驗證欄
- `summary`: 兩條驗證命令無法驗證其宣稱要驗證的事 —— `grep -c 'zh_' generate_audio.py` 會被 `zh_count` 這類區域變數誤觸而假陽性；`grep -c 'play-btn zh'` 只回傳數字，看不出是否在註解裡。
- `recommendation`: 分別改為 `grep -n 'zh-TW\|ZH_VOICE\|zh_.*\.mp3'` 與 DevTools 的 `querySelectorAll('.play-btn.zh').length`。

**F-8**（Reviewer B，`confidence` 55）
- `layer`: design ／ `location`: `design.md` `## Failure modes`；`tasks.md` 舊檔刪除與產生步驟的順序
- `summary`: Failure modes 未涵蓋 50 次循序 TTS 請求中途失敗的狀態，也沒說重跑是否安全；且刪除舊檔的任務排在實際產生之前，兩者之間 repo 處於 `index.html` 指向已刪除音檔的狀態。
- `recommendation`: 補「非原子但重跑 idempotent」的說明，並把舊檔刪除移到產生成功之後。

**F-9**（Reviewer B，`confidence` 55）
- `layer`: design ／ `location`: `specs/page-navigation/spec.md`「頁碼 tab 列」；`design.md` tab 切換 Decision
- `summary`: tab 列只規定「在畫面最上方」，沒規定 sticky，也沒規定切頁後的捲動位置；p.12 有 7 張 28px 大字卡片在手機上必然超過一個 viewport，唸到底部想換頁得先捲回頂端。
- `recommendation`: 補 sticky 與切頁後捲回該頁頂端兩項需求與對應驗收。

**F-10**（Reviewer B，`confidence` 50）
- `layer`: design ／ `location`: `design.md` `## Implementation Contract` → Interface（`PAGES` 與 `TIMINGS`）
- `summary`: `PAGES` 以「頁 + 頁內序號」定位、`TIMINGS` 以「全域句子索引」定位，兩套索引空間並存有靜默錯位風險 —— 流水計數器錯一格就會讓 karaoke 對到別句的時間軸，而既有的長度比對只在兩句字數不同時才擋得下來。
- `recommendation`: 把 word boundary 併進 `PAGES` 的句子物件，讓全域計數器消失。

## Rating

- post-filter cumulative blocking set Critical count: 1
- post-filter cumulative blocking set Warning count: 1
- 非阻塞 triaged finding count: 8
- `critical_gap`: true
- `round_type`: full
- 理由：本輪為未 seeded 執行的第一輪，所有通過 confidence filter 的 Critical 與 Warning 皆為阻塞。F-1 經主 agent 以 `git show --stat 4114ad5` 獨立驗證屬實，且會直接違反本變更自己寫下的兩條 SHALL（預設速度 0.5、不顯示中文播放按鈕），屬 Critical。F-2 由兩位 reviewer 獨立提出，為明確的範圍缺口。阻塞集合非空，故本輪不通過。

## Fix Actions

修正涵蓋全部 10 項 finding（含非阻塞者），採用 fix propagation：每個被觸及的概念都跨全部 artifact 同步。

- **F-1**：改寫 `design.md` `## Context` 第 3 點，逐項列出模板與 `index.html` 的五處差異並附 `git show --stat` 佐證；新增 Decision「`index.html` 一律由 `generate_audio.py` 模板產生，手改需回寫模板」；`proposal.md` Non-Goals 第 5 點改為「不改變使用者可見結果，但需回寫模板」並在 Proposed Solution 補一條；`specs/practice-webpage/spec.md` 新增 ADDED 需求「產出的網頁與模板一致」含四項回寫的 Example 表；`tasks.md` 新增任務 4.1 明列目標值與 `grep` 驗證。修改檔案：`design.md`、`proposal.md`、`specs/practice-webpage/spec.md`、`tasks.md`。
- **F-2**：`specs/practice-webpage/spec.md` 新增 ADDED 需求「網頁標題反映目前的繪本」；`design.md` Behavior 與 Acceptance criteria 補標題項；`tasks.md` 4.1 與 5.3 涵蓋。副標去留已向使用者確認：**刪除副標**，只留主標 `The Ant and The Grasshopper`。修改檔案：`specs/practice-webpage/spec.md`、`design.md`、`tasks.md`、`proposal.md`。
- **F-3**：`design.md` 分句 Decision 補「段落（空行）邊界一律強制斷句，標點規則只在段落內套用」並說明它是獨立變因；`tasks.md` 2.1 補一項「段落結尾標點後接小寫開頭」的驗證實例。修改檔案：`design.md`、`tasks.md`。
- **F-4**：`design.md` 音檔命名 Decision 補孤兒檔代價與清除規則；`specs/audio-generation/spec.md` 於 `Generate English audio files` 加 Scenario「清除不屬於本次產生結果的音檔」與 Example；`design.md` Acceptance criteria 改為「`audio/` 恰等於本次產生集合」；`tasks.md` 3.1 補清除行為與假檔驗證、5.2 改為集合相等。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`tasks.md`。
- **F-5**：`design.md` 分句 Decision 明訂 ASCII 直引號並說明彎引號的失敗模式；`specs/audio-generation/spec.md` 於 `Single source of truth for lines and translations` 加入引號字元約束；`tasks.md` 1.1 加 `grep -n '[“”‘’]' story.md` 驗證；`design.md` Risks 補一條。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`tasks.md`。
- **F-6**：移除 `tasks.md` 中所有 `--dry-run` 提及，2.1 改以檢視 `story.json` 驗證；`design.md` 的 `story.json` Decision 補「不另外新增只解析不產音的 CLI 旗標」。修改檔案：`tasks.md`、`design.md`。
- **F-7**：`tasks.md` 3.2 改為 `grep -n 'zh-TW\|ZH_VOICE\|zh_.*\.mp3'` 並註明不可用 `grep -c 'zh_'` 的原因；4.7 改為 DevTools 的 `querySelectorAll('.play-btn.zh').length` 為 0。修改檔案：`tasks.md`。
- **F-8**：`design.md` `## Failure modes` 新增非原子與重跑 idempotent 段落；`specs/audio-generation/spec.md` 加 Scenario「產生流程失敗後重跑」；`tasks.md` 重排 —— 舊檔刪除自第 3 節移出，成為第 5 節的 5.2，明確排在 5.1 產生成功之後，5.1 並註明失敗時的復原方式。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`tasks.md`。
- **F-9**：`specs/page-navigation/spec.md`「頁碼 tab 列」補 sticky 需求與 Scenario、「只有被選中頁的句子可見」補捲動位置重設需求與 Scenario；`design.md` tab Decision 與 Behavior 補這兩點；`tasks.md` 4.3 與 4.4 補對應驗收。修改檔案：`specs/page-navigation/spec.md`、`design.md`、`tasks.md`。
- **F-10**：`design.md` 新增 Decision「word boundary 併入 `PAGES`，不保留獨立的全域 `TIMINGS`」並改寫 Interface 為單一 `PAGES` 變數；`specs/word-karaoke/spec.md` 於 `Capture word boundary timing` 改為 `timings` 掛在句子物件上、加 Scenario「不存在獨立的全域時間資料陣列」、`Canonical tokenization and alignment` 的比對對象改為該句 `timings`；`tasks.md` 4.6 補 `grep -c 'const TIMINGS' index.html` 為 0 與高亮正確性抽查。修改檔案：`design.md`、`specs/word-karaoke/spec.md`、`tasks.md`。

修正後處置：
- 因 fix actions 修改了 proposal、design、tasks 與 spec artifacts，已重跑 `cash validate ant-grasshopper-storybook` → Validation passed。
- 已重跑 pre-round mechanical self-check：註解 lint、spec delta 標題身分比對、每個 requirement 至少一個 scenario、requirement 與 design 標題對 tasks 的交叉引用、數量宣稱一致性 —— 全數通過。此次自檢未新增發現。
- 本輪 fix actions 未修改 `openspec/changes/` 以外的任何檔案，故不執行 `cash touched` 記錄。
- 本輪無 `未修復：裁判面保護` 記錄。

## Decision

next_round
