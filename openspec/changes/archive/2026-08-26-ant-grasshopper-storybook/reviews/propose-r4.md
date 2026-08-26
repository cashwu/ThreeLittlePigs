# Cash Propose Review — Round 4

## Reviewer Findings

本輪為本次執行的第四輪檢查點（full round），由 Reviewer A（Adherence）與 Reviewer B（Quality）並行獨立審查，兩者收到相同 context 且不互相傳遞輸出。findings 依 `location + summary` 去重後套用 confidence filter。

### 累積阻塞集合逐一判定

- **R3-1**（Warning，`fix-introduced`，孤兒檔清除範圍在 design 與其他 artifact 之間不一致）→ **resolved**。兩位檢查點 reviewer 皆判定 resolved，無 unresolved 票。Reviewer A 以 `grep -n '不屬於本次'` 全掃確認四處措辭同義且無一處保留「英文」限定，並確認 `audio/` 實有 18 個舊音檔、全部落入清除範圍、`tasks.md` 5.2 的驗證能在腳本漏掉清除時失敗。Reviewer B 另確認 design 明文否定了 `en_` 前綴這個錯誤實作並直接點名 9 個中文音檔的負責者，且 `audio/` 內無雜項檔案使 `ls audio | wc -l` 為 50 的驗證成立。

**post-filter 累積阻塞集合為空集合。**

### Suggestion

本輪 8 項 findings 的 `confidence` 皆低於 80，經 confidence filter 全數降級或維持為 Suggestion，均為非阻塞。

**Q4-1**（Reviewer B，原 Warning `confidence` 70 → 降級；`disposition`: `fix-introduced`，`introduced_by`: 第 2 輪 V-2）
- `layer`: design ／ `location`: `design.md` Implementation Contract 產出順序與 Failure modes；`tasks.md` 5.1
- `summary`: 產出順序把「清除孤兒檔」排在「寫出 `index.html`」之前，留下具破壞性的失敗窗口 —— 清除已執行但 `index.html` 尚未寫出時，舊的 `index.html` 會指向 18 個已被刪除的音檔，每顆播放鍵全部 404，正是第 1 輪 F-8 要避免的狀況；`tasks.md` 5.1 更把「現有網頁仍可用」寫成失敗後的既定事實，而該不變式在此窗口內不成立。兩步驟之間無資料依賴。
- `recommendation`: 順序改為「產生音檔 → 寫出 `index.html` → 清除孤兒檔」。

**Q4-2**（Reviewer B，原 Warning `confidence` 70 → 降級；`disposition`: `fix-introduced`，`introduced_by`: 第 3 輪 R3-2 與第 2 輪 V-2 疊加）
- `layer`: design ／ `location`: `specs/audio-generation/spec.md` Example「段落規則作為安全網」vs `tasks.md` 2.1
- `summary`: 該 Example 是段落規則唯一的鑑別性案例，但 tasks 2.1 的驗證只要求「每一處段落邊界都產生句界」並明文不得改動 `story.md`。結果是段落規則這條實際存在的程式分支在整份 tasks 中沒有任何驗證能證明它有被實作 —— 一個只實作標點規則、完全省略段落規則的實作會通過 2.1 到 5.3 的每一項驗證。
- `recommendation`: 補一條不觸及 `story.md` 的直接驗證：對分句函式以構造字串單獨呼叫一次。

**Q4-3**（Reviewer B，原 Warning `confidence` 65 → 降級；`disposition`: `new`）
- `layer`: design ／ `location`: `specs/word-karaoke/spec.md` tokenization 規則；`specs/audio-generation/spec.md` 解析需求；`design.md`
- `summary`: tokenization 被規範為等同於 `en_lines.join(' ').split(/\s+/)`，但沒有任何 artifact 要求 `en_lines` 的每個元素為已去除首尾空白的字串。本次分句規則必然會在書上一行中間切開，切點兩側空白會落到某個 fragment 上；只要前導空白被保留，JS 的 `split(/\s+/)` 就會多產生一個空字串 token，token 數與 `timings` 長度差 1，該句靜默退回無高亮 —— 而 Python 的 `str.split()` 會自動去除首尾空白，腳本端的自檢看不到這個不對稱。`tasks.md` 4.6 的抽查點恰好是 p.12 第 5 句而非行中切句產生的第 6 句。
- `recommendation`: 規範顯示行為已去除首尾空白的非空字串，並在 `story.json` 檢視中加入該項檢查。
- 主 agent 已獨立驗證：對 fragment `' "And I'm starving, too!'`，Python `str.split()` 得 4 個 token，node 的 `split(/\s+/)` 得 5 個（首個為空字串）。另以現有 9 句實測 edge-tts 的 `WordBoundary` 對每個空白 token 恰發出一次事件且 `word` 已去除附著標點（`friends!` → `friends`），9 句 token 數與 timing 數全數相符 —— 佐證 Reviewer B 的結論：真正的風險是空 token，而非 design Risks 原先擔心的切詞差異。

**Q4-4**（Reviewer B，`confidence` 55；`disposition`: `new`）
- `layer`: design ／ `location`: `design.md` tab Decision；`specs/page-navigation/spec.md`「頁碼 tab 列」
- `summary`: sticky tab 列沒有被要求具備不透明背景或 stacking 順序。現有模板 body 為 `#fef9ef`、句子卡片為 `#fff` 白卡，無自身背景的 sticky 列會讓白卡直接從 tab 文字底下穿過，12 個 tab 標籤與 28px 英文字重疊而難以辨讀；`tasks.md` 4.3 的「tab 列仍可見」擋不下重疊。
- `recommendation`: 補不透明背景需求與「不與卡片內容重疊」的目視驗收。

**Q4-5**（Reviewer B，`confidence` 50；`disposition`: `new`，與第 3 輪 R3-2 同源）
- `layer`: text ／ `location`: `specs/audio-generation/spec.md` Example「各頁句數」；`specs/page-navigation/spec.md` Example「各頁的句子卡片數」
- `summary`: 第 3 輪 R3-2 已確立「內容衍生、提案階段無法自 repo 查證的事實，不應以規範性斷言寫進會被 archive 的 master spec」，並據此改寫了段落邊界的 Example；但同一類、份量更重的斷言原封不動留著 —— `4, 4, 3, 5, 3, 5, 5, 4, 7, 5, 3, 2` 以 `SHALL` 寫在兩處 Example 中，來源與段落邊界數完全相同。
- `recommendation`: 兩處 Example 改為與內容無關的規範（各頁句數 SHALL 等於該頁翻譯數），具體數列留在不會 archive 的 `design.md` 與 `tasks.md`。

**Q4-6**（Reviewer B，`confidence` 50；`disposition`: `new`）
- `layer`: design ／ `location`: `tasks.md` 1.2；`design.md` `story_zh.json` Decision
- `summary`: 50 句中文翻譯是完成「中文顯示但不發音」需求的必要產出，但沒有任何 artifact 說明它從哪裡來（謄打自繪本中文版、實作者翻譯、或需使用者提供）；也未說明翻譯粒度必須與英文分句 1:1，包含句界落在書上一行中間而被拆開的那幾句 —— 該約束只隱含在「順序對應分句結果」一句中。
- `recommendation`: 1.2 補明翻譯來源與粒度約束。

**R4-1**（Reviewer A，`confidence` 50；`disposition`: `fix-introduced`，`introduced_by`: 第 1 輪 F-1 與 F-2 在同一段落合併時被計為「五項現值」）
- `layer`: text ／ `location`: `design.md` `## Context` 第 3 點與模板回寫 Decision
- `summary`: design 內部計數與事實陳述自相矛盾。同段先寫「`4114ad5` 的三項 UI 調整」隨即列出「差異有四處」（其餘 artifact 一律為四項）；更實質的是把 `<title>`／`<h1>`／副標算進同一組稱為「五項現值」，但經比對模板與 `index.html` 的標題三處**完全相同**，它既不是差異、不會倒退，且「`index.html` 的目前現值」正是要被丟棄的舊值，與「保留現值」語意相反。照字面實作會保留舊標題，違反同一份 design 的 Behavior。
- `recommendation`: 把「模板落差需回寫」與「標題需更新」兩類拆開敘述，並把三項改為四項。

**R4-2**（Reviewer A，`confidence` 50；`disposition`: reviewer 標為 `unresolved-prior`，主 agent 更正為 `new`）
- `layer`: text ／ `location`: `design.md` Failure modes 第 3 點與 karaoke Decision，對照 `specs/word-karaoke/spec.md` 與 `tasks.md` 4.6
- `summary`: fallback 的呈現方式在 design 與 spec／tasks 之間措辭不一致。spec 與 tasks 皆寫「退回保留 `<br>` 換行的文字」，design 只寫「不切 span 的純文字顯示」未提 `<br>`，且把該規則描述為「既有行為保留不變」；而現況 `index.html` 的 fallback 是 `enHtml = line.en`（單一字串、無換行資訊），「保留不變」地套用會把 `en_lines` 併成一行而丟失書上換行，違反 design 自身的 Goal。design Risks 已預期本次內容會有若干句落入 fallback，非純理論情形。
- `recommendation`: Failure modes 改為「保留 `<br>` 換行的純文字」，Decision 段落把「既有行為不變」限定為觸發條件與影響範圍不變、呈現方式改變。
- **disposition 更正紀錄**：Reviewer A 標為 `unresolved-prior`，但主 agent 檢查前三輪紀錄後確認此 finding 未曾出現於任何一輪的阻塞集合，亦不匹配任何先前的阻塞 finding，依規則更正為 `new`。此為 blocking-to-non-blocking 的更正；由於 `confidence` 為 50 本就非阻塞，更正不影響本輪決定。

### Reviewer 明確指出、經查為誤判而不報告的項目

- `Fail-fast on count mismatch` 的「不產生任何音檔、`story.json` 或 `index.html`」與「檢查通過後立即寫出 `story.json`」不矛盾：逐頁檢查排在寫出之前。
- tab 列自身橫向捲動與 body 不出現水平捲軸不矛盾；`position: sticky` 與同元素 `overflow-x: auto` 不互斥。
- `grep -n 'TIMINGS'` 不會被小寫 `timings` 誤觸。
- edge-tts 的 `WordBoundary` 對 `hadn't`、`I'm`、`"Why`、`too!`、`meadow,"` 這類 token 不會造成數量偏差（Reviewer B 以現有 9 句實測，主 agent 複驗）。
- 複雜度稜鏡：三輪新增的孤兒檔清除、sticky tab、切頁捲動重設、產出順序、頁內 DOM id 五項皆有具體代價敘述作為理由且為最小可行作法，無新增相依、無單一實作的抽象、無純轉手 wrapper、無投機性可設定項。
- 一次渲染 50 張卡片配 `display: none`：隱藏頁不影響可見頁的文件流起點、`new Audio(src)` 不在 DOM 中、50 個音檔不會被預載。

## Rating

- post-filter cumulative blocking set Critical count: 0
- post-filter cumulative blocking set Warning count: 0
- 非阻塞 triaged finding count: 8
- `critical_gap`: false
- `round_type`: full
- 理由：唯一的累積阻塞集合成員 R3-1 經兩位檢查點 reviewer 一致判定為 verified resolution 並離開集合，無 unresolved 票。本輪 8 項新 findings 的 `confidence` 皆低於 80，經 confidence filter 全數為 Suggestion，依規則非阻塞。post-filter 累積阻塞集合為空，本輪通過。

## Fix Actions

本輪決定為 `passed`，依規則非阻塞 findings 僅需 triage 記錄；但 Q4-1、Q4-3、R4-2 經主 agent 判定為實質正確且成本低（Q4-3 更經主 agent 以 node 與 Python 獨立實測確認），因此連同其餘 5 項一併修正而非僅記錄。

- **Q4-1**：`design.md` 產出順序改為「解析與分句 → 逐頁句數檢查 → 寫出 `story.json` → 產生音檔 → 寫出 `index.html` → 清除孤兒檔」並說明兩步驟間無資料依賴、反序會留下破壞性窗口；Failure modes 補「任何中斷點上都不會出現 `index.html` 指向已刪除音檔的狀態」；`specs/audio-generation/spec.md` 於 `Single source of truth for lines and translations` 補清除時機、重跑 Scenario 補「目前可用的網頁 SHALL 維持可用」；`tasks.md` 3.1 改為「在 `index.html` 寫出之後刪除」、5.1 復原敘述同步。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`tasks.md`。
- **Q4-2**：`tasks.md` 2.1 補一條不觸及 `story.md` 的直接驗證 —— 以構造字串 `"They ate the seeds.\n\nand slept through the winter."` 單獨呼叫分句函式，確認回傳兩個句子，使段落規則這條程式分支有對應驗證。修改檔案：`tasks.md`。
- **Q4-3**：`design.md` 分句 Decision 補「`en_lines` 每個元素 SHALL 為已去除首尾空白的非空字串」並附 Python 與 JS 切分行為不對稱的實測說明；`specs/audio-generation/spec.md` 解析需求補同一約束並新增 Scenario「行中切句後的顯示行不帶首尾空白」；`specs/word-karaoke/spec.md` tokenization 規則補「SHALL NOT 產生空字串 token」及其後果說明；`tasks.md` 2.1 的 `story.json` 檢視加入「無任何 `en_lines` 元素帶有首尾空白」。修改檔案：`design.md`、`specs/audio-generation/spec.md`、`specs/word-karaoke/spec.md`、`tasks.md`。
- **Q4-4**：`design.md` tab Decision 與 `specs/page-navigation/spec.md`「頁碼 tab 列」補不透明背景需求，sticky Scenario 補「卡片內容 SHALL NOT 自 tab 列下方透出與其重疊」；`tasks.md` 4.3 目視驗收補「tab 標籤不與卡片內容重疊、仍清晰可讀」。修改檔案：`design.md`、`specs/page-navigation/spec.md`、`tasks.md`。
- **Q4-5**：`specs/audio-generation/spec.md` 的 Example 改名為「各頁句數以謄打結果為準」，規範改為「每頁英文句數 SHALL 等於該頁中文翻譯數，具體數值以謄打結果為準」；`specs/page-navigation/spec.md` 的 Example 標題與表頭改為指向 `story.json` 的句子數。具體數列保留於 `design.md` 驗收條件與 `tasks.md`。修改檔案：`specs/audio-generation/spec.md`、`specs/page-navigation/spec.md`。
- **Q4-6**：`tasks.md` 1.2 補明中文翻譯由實作者依 `story.md` 的英文分句結果逐句翻譯、舊的 9 句屬於另一本書不可沿用，並補粒度約束（與英文分句一一對應，含行中切句拆出的那幾句），驗證改為與 `story.json` 各頁英文句數逐頁相符並逐句目視確認語意。修改檔案：`tasks.md`。
- **R4-1**：`design.md` `## Context` 第 3 點把「三項」改為「四項」、把標題三處另立為「不同性質的改動：模板與 `index.html` 兩者相同，不是落差、不會倒退，而是本次要一併改為新繪本的內容」；模板回寫 Decision 改為「把四項現值寫進模板，另把 `<title>` 與 `<h1>` 改為新繪本並刪除副標 —— 這一項不是回寫現值」。修改檔案：`design.md`。
- **R4-2**：`design.md` Failure modes 第 3 點改為「退回保留 `<br>` 換行的純文字顯示」並明言現況的 `enHtml = line.en` 不可原樣沿用；karaoke Decision 把「既有行為保留不變」限定為觸發條件與影響範圍不變、呈現方式改為保留 `<br>`；`tasks.md` 4.6 同步加註不可沿用單一字串寫法。修改檔案：`design.md`、`tasks.md`。

**主 agent 對 Reviewer B 附帶觀察的採納**：Reviewer B 指出 `tasks.md` 3.1 原本的孤兒檔測試假檔 `audio/en_p12_09.mp3` 在「正確實作」與「被否定的 `en_` 前綴實作」下都會被刪除，該測試不具鑑別力。已把假檔改為 `audio/zh_99.mp3`，使單一測試即可同時驗到「比對檔名集合而非 `en_` 前綴」。

修正後處置：
- 因 fix actions 修改了 design、tasks 與三份 spec artifacts，已重跑 `cash validate ant-grasshopper-storybook` → Validation passed；`cash analyze` → 0 Critical/Warning。
- 已重跑 pre-round mechanical self-check：註解 lint、spec delta 標題身分、每個 requirement 至少一個 scenario、requirement 與 design 標題對 tasks 的交叉引用、產出順序措辭一致性、R4-1 的計數殘留掃描、`globalIdx`／`dry-run`／「12 處段落邊界」殘留掃描 —— 全數通過。此次自檢未新增發現。
- 本輪的 fix actions 發生在本次執行最後一輪 reviewer 通過之後，因此這 8 項修正未再經 reviewer 驗證。由於全數為非阻塞 Suggestion 且皆為局部、可由機械自檢與 `cash validate` 覆蓋的措辭與順序調整，主 agent 判定不需為此另起一輪。此事實一併載於完成輸出。
- 本輪 fix actions 未修改 `openspec/changes/` 以外的任何檔案，故不執行 `cash touched` 記錄。
- 本輪無 `未修復：裁判面保護` 記錄。

## Decision

passed
