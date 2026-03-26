# NVIDIA Omniverse 學習筆記

> 記錄日期：2026-03-09
> 環境：Ubuntu 22.04 / NVIDIA TITAN RTX / Kit SDK 110.0.0
> 重點：理解 Omniverse、OpenUSD、kit-app-template 與 kit_base_editor 的定位

---

## 一、Omniverse 是什麼？

**Omniverse 不是一個單一軟體，而是一個開發平台。** 它提供了一整套工具鏈，讓開發者能建造自己的 3D 應用程式。

核心組成：

| 元件 | 角色 |
|------|------|
| **OpenUSD** | 場景描述格式，所有 3D 資料的根基 |
| **Kit SDK** | 應用程式開發框架，用來組裝工具 |
| **RTX 渲染器** | 即時光線追蹤渲染引擎 |
| **PhysX** | 物理模擬引擎 |
| **OmniGraph** | 視覺化程式設計系統 |
| **Nucleus** | 多人協作 / 資料管理伺服器 |

---

## 二、用「蓋房子」理解整體架構

### 比喻對照

| 蓋房子 | Omniverse 對應 | 說明 |
|--------|---------------|------|
| 建築工法、鋼筋水泥、工程標準 | Kit SDK、OpenUSD、RTX | **框架層**：提供所有基礎能力 |
| 你蓋的「設計事務所」 | My Editor（你的 Kit App） | **工具層**：你用框架組裝出來的工具 |
| 事務所裡設計出來的「建築圖 / 模型」 | USD 場景（`.usd` 檔案） | **數據層**：你用工具創造出來的成果 |

### 三層架構圖

```
┌─────────────────────────────────────────────────────┐
│           工作成果（USD 場景 / 虛擬環境）               │  ← 數據層
│   工廠數位孿生、城市模擬、機器人訓練場景...               │
│   這是你最終要交付的東西                                │
└───────────────────────┬─────────────────────────────┘
                        │ 用什麼工具來建構 / 操作 / 檢視？
┌───────────────────────▼─────────────────────────────┐
│           應用程式（Kit App）                          │  ← 工具層
│   USD Composer（官方）/ My Editor（你自己的）           │
│   這是你用來「施工」的工具                               │
└───────────────────────┬─────────────────────────────┘
                        │ 用什麼技術建造這些工具？
┌───────────────────────▼─────────────────────────────┐
│           Kit SDK + OpenUSD + RTX 渲染                │  ← 框架層
│   Extensions、Hydra、PhysX、OmniGraph...              │
│   這是「建材」與「工法」                                │
└─────────────────────────────────────────────────────┘
```

### 軟體世界類比

| Omniverse 概念 | 軟體類比 |
|---------------|---------|
| Kit SDK | Electron 框架 |
| `.kit` 檔案 | `package.json` + 設定檔 |
| Extensions | npm packages / 功能模組 |
| My Editor（你的 App） | 你用 Electron 做的自定義桌面 App |
| USD Composer（官方 App） | VS Code（也是 Electron 做的，但是別人做好的產品） |

**關鍵理解**：「應用程式」是你用來建造 / 編輯 / 檢視虛擬環境的**工具**，不是虛擬環境本身。

---

## 三、為什麼不直接用官方 App？

NVIDIA 官方有做好的 App（例如 USD Composer），直接就能建場景。那為什麼還要自己做 App？

### 原因：不同行業需求差很多

| 應用場景 | 需要的功能 | 不需要的功能 |
|---------|-----------|------------|
| 工廠數位孿生 | 導入 CAD、擺放設備、跑模擬 | 動畫、影視渲染 |
| 影視製作 | 材質、燈光、動畫、渲染 | 物理模擬、感測器 |
| 機器人訓練 | 感測器模擬、物理引擎 | 手動建模、材質編輯 |
| 建築視覺化 | Walkthrough、即時渲染 | 物理、動畫、指令碼 |

**官方 App 是「瑞士刀」**，什麼都有但不一定都需要。
**自定義 App 是「專用工具」**，只留需要的功能，還能加入行業特定的工作流程。

### 具體好處

1. **精簡介面**：終端使用者不會被一堆用不到的按鈕搞混
2. **客製化工作流**：例如一鍵導入特定格式的設備模型、自動佈局功能
3. **可部署給非技術人員**：做成簡單直覺的工具給客戶或現場工程師用
4. **品牌化**：可以變成你公司自己的產品

### 選擇建議

```
目標是「快速出場景」         → 用官方 USD Composer 即可
目標是「建立可重複的工作流程」 → 自己開發 App + Extension
目標是「學習 Omniverse 開發」→ 自己開發（課程走的路線）
```

---

## 四、OpenUSD 的角色

OpenUSD（Universal Scene Description）是 Pixar 開發的場景描述格式，Omniverse 以此為核心。

### 為什麼重要？

```
傳統方式：每個軟體有自己的格式
  Maya (.ma) ← 不能直接給 → Blender (.blend)
  SolidWorks (.sldprt) ← 不能直接給 → Unreal (.uasset)

OpenUSD 方式：統一格式
  任何工具 → 產出 .usd → 任何工具都能讀取/編輯
```

| 特性 | 說明 |
|------|------|
| **層級式（Layer）** | 場景可以分層管理，不同人編輯不同 layer 不衝突 |
| **組合式（Composition）** | 場景由多個 USD 檔案組合而成，可重複引用 |
| **跨軟體** | Maya、Blender、Unreal 都支援 USD |

---

## 五、`kit-app-template` 的定位

### 一句話定義

**`kit-app-template` 是「建立工具的工具」（scaffolding）。** 類似 `create-react-app`，幫你快速產生一個 Kit 應用程式的專案骨架。

### 它產出什麼？

```
kit-app-template（腳手架）
  └─ ./repo.sh template new
       └─ 產出 → my_company.my_editor.kit（你的 App 定義檔）
                  + 專案結構（extensions 目錄、build 設定等）
```

### 建立流程

```bash
# 1. 執行互動式模板建立
./repo.sh template new
#    → 選擇 Application
#    → 選擇模板：kit_base_editor
#    → 輸入名稱：my_company.my_editor
#    → 輸入顯示名稱：My Editor
#    → 輸入版本：0.1.0
#    → 選擇性加入 streaming layers

# 2. 建置（下載 extensions、編譯）
./repo.sh build

# 3. 啟動應用程式
./repo.sh launch
```

---

## 六、`kit_base_editor` 模板

### 定位

`kit_base_editor` 是眾多模板之一，提供了一個**基礎 3D 編輯器**的功能組合，包含約 50 個 Extensions。

### 內建能力

| 功能 | 說明 |
|------|------|
| 3D Viewport | RTX 即時渲染的 3D 視窗 |
| 場景操作 | 移動、旋轉、縮放物件 |
| Stage 樹 | 查看場景的層級結構 |
| Property 面板 | 編輯物件屬性 |
| Content Browser | 瀏覽 / 匯入資產 |
| 物理模擬 | PhysX 物理引擎 |
| 材質管理 | 建立、指派材質 |
| OmniGraph | 視覺化程式設計 |

### 客製化方式

透過修改 `.kit` 檔案中的 `[dependencies]` 來增減功能模組：
- **移除不需要的 extension** → 精簡介面
- **加入自定義 extension** → 加入你開發的功能

---

## 七、`.kit` 檔案結構

`.kit` 檔案是 **TOML 格式的應用程式定義檔**，結構如下：

| 區段 | 用途 |
|------|------|
| `[package]` | App 的名稱、版本、描述 |
| `[dependencies]` | 要載入的 Extensions 清單（最核心） |
| `[settings]` | 全域設定（渲染、效能等） |
| `[settings.app]` | App 專屬設定（字型、視窗標題等） |
| `[settings.app.exts]` | Extension 搜尋路徑 |
| `[[test]]` | 測試用設定 |
| `[template]` | 模板元資料 |

> 詳細的欄位解析請參考 [`docs/kit-file-explained.md`](./kit-file-explained.md)

---

## 八、實際使用流程（End-to-End）

以「建構工廠數位孿生」為例的完整流程：

```
Step 1：建立你的 App
  └─ 用 kit-app-template 建專案
  └─ 選 kit_base_editor 模板
  └─ 調整 .kit 檔，移除不需要的功能

Step 2：開發客製 Extensions
  └─ 寫 Python/C++ 插件
  └─ 例如：一鍵導入 CAD 設備模型
  └─ 例如：自動化產線佈局工具

Step 3：用你的 App 建構 USD 場景
  └─ 導入工廠 3D 模型
  └─ 擺放設備、設定物理屬性
  └─ 配置感測器、光源

Step 4：場景可被多個工具共用
  └─ 你的 App 編輯場景
  └─ 別人的 App 也能開同一個場景
  └─ 透過 Nucleus 多人同時協作

Step 5：場景用於最終目標
  └─ 即時監控（數位孿生）
  └─ AI 訓練（Isaac Sim）
  └─ 高品質渲染輸出
```

---

## 九、啟動時的 Errors / Warnings

### `omni.platforminfo.plugin` — CPU 資訊讀取失敗

```
[Error] failed to find the package that core 0..23 belongs to.
[Error] all CPU packages were empty!
```

- **原因**：CPU topology sysfs 節點不可讀（虛擬化 / 容器環境常見）
- **影響**：**無害**，僅 telemetry 用途

### gRPC protobuf 重複註冊

```
File already exists in database: grpc/health/v1/health.proto
```

- **原因**：多個 extension 重複註冊同一 proto 定義
- **影響**：**無害**，已知問題

### 其他 Warnings

| 訊息 | 說明 |
|------|------|
| `rateLimitFrequency` 120 → 75 | 自動匹配螢幕 75Hz，正常 |
| `cache_indicator` pipapi | Extension 設定不完整但無害 |
| `Unable to detect Cache Server` | 沒裝 Omniverse Cache，可選安裝 |

---

## 十、學習路線

```
1. ✅ 了解 Omniverse 架構與定位（本筆記）
2. ✅ 用 kit-app-template 建立 Kit App（已完成）
3. → 學習撰寫 Extension（自定義功能插件）
4. → 學習 OpenUSD 場景結構（Stage、Prim、Layer）
5. → 透過 App + Extensions 建構數位孿生場景
6. → Nucleus（多人協作 / 資料管理）
7. → Isaac Sim（機器人模擬，如適用）
```
