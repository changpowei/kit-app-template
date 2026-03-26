# USD Explorer 應用程式筆記

> 記錄日期：2026-03-09
> 模板：`omni.usd_explorer`
> 產出檔案：`source/apps/my_company.my_usd_explorer.kit`

---

## 一、USD Explorer 是什麼？

### 官方定義

> A reference application for reviewing and constructing large facilities such as factories, warehouses and more.

**USD Explorer 是一個專門用來瀏覽、審閱和建構大型場景的應用程式模板。** 它的目標場景是工廠、倉庫等大型設施的數位孿生。

### 與 Kit Base Editor 的比較

| 比較項目 | Kit Base Editor | USD Explorer |
|---------|----------------|--------------|
| **定位** | 通用 3D 編輯器基礎 | 大型場景瀏覽 / 審閱 / 建構 |
| **目標使用者** | 開發者 / 技術人員 | 專案審閱者 / 設施規劃者 |
| **介面風格** | 全功能（類似 DCC 工具） | 精簡化（隱藏進階選項） |
| **協作功能** | ❌ 無 | ✅ 內建 Live Session |
| **Setup Extension** | ❌ 無 | ✅ 自動產生一個 |
| **導航工具** | 基本攝影機操作 | Waypoint、Markup、Measure 等 |
| **設定量** | 約 125 行 | 約 684 行（大量預設調校） |
| **適用場景** | 自定義開發的起點 | 數位孿生場景審閱 |

---

## 二、建立流程

```bash
# 1. 建立 USD Explorer 應用程式
./repo.sh template new
#    → 選擇 Application
#    → 選擇模板：omni_usd_explorer（USD Explorer）
#    → 輸入 .kit 檔名：my_company.my_usd_explorer
#    → 輸入顯示名稱：My USD Explorer
#    → 輸入版本：0.1.0

# 此模板會自動要求建立 Setup Extension：
#    → 輸入 extension 名稱：my_company.my_usd_explorer_setup_extension
#    → 輸入 extension 顯示名稱：My USD Explorer Setup Extension
#    → 輸入版本：0.1.0

# 2. 建置
./repo.sh build

# 3. 啟動
./repo.sh launch
```

### 產出結構

```
source/
├── apps/
│   └── my_company.my_usd_explorer.kit          ← App 定義檔
└── extensions/
    └── my_company.my_usd_explorer_setup_extension/  ← Setup Extension
        ├── config/extension.toml               ← Extension 設定
        ├── data/                               ← 圖示、內建材質等
        ├── layouts/                            ← UI 佈局設定
        │   ├── default.json
        │   ├── viewport_only.json
        │   ├── comment_layout.json
        │   └── markup_editor.json
        └── my_company/my_usd_explorer_setup_extension/
            ├── setup.py                        ← Extension 啟動邏輯
            ├── navigation.py                   ← 導航功能
            ├── menu_helper.py                  ← 選單管理
            ├── menubar_helper.py               ← 選單列管理
            ├── stage_template.py               ← Stage 模板
            ├── ui_state_manager.py             ← UI 狀態管理
            └── tests/                          ← 測試
```

---

## 三、Setup Extension 的角色

USD Explorer 模板與 Kit Base Editor 的最大差異之一就是**自動產生了一個 Setup Extension**。

### 為什麼需要？

`.kit` 檔只能做「宣告式」的設定（哪些 extension 要載入、設定值是什麼）。但有些初始化邏輯需要**程式碼**來執行，例如：

- 設定 UI 佈局
- 初始化導航系統
- 建立預設 Stage 模板
- 管理選單狀態

### 載入順序

```toml
"my_company.my_usd_explorer_setup_extension" = { order = 10000 }
```

`order = 10000` 確保它**最後載入**，在所有其他 extension 都準備好之後才執行初始化。

---

## 四、核心 Extensions 分析

### 場景瀏覽與導航

| Extension | 用途 |
|-----------|------|
| `omni.kit.tool.camera_playlist` | 攝影機路徑播放清單 |
| `omni.kit.waypoint.playlist` | Waypoint（路標點）導航 |
| `omni.kit.viewport.menubar.waypoint` | Viewport 中的 Waypoint 選單 |
| `omni.kit.viewport.menubar.nav_bar_toggle` | 導航列開關 |
| `omni.kit.timeline.minibar` | 時間軸迷你控制列 |

### 審閱與標記

| Extension | 用途 |
|-----------|------|
| `omni.kit.tool.markup` | 標記工具（在場景中加註記） |
| `omni.kit.viewport.menubar.markup` | Viewport 中的標記選單 |
| `omni.kit.tool.measure` | 測量工具（量距離、面積等） |

### 即時協作（Live Session）

| Extension | 用途 |
|-----------|------|
| `omni.kit.collaboration.channel_manager` | 協作頻道管理 |
| `omni.kit.collaboration.presence_layer` | 顯示其他協作者的位置 |
| `omni.kit.collaboration.selection_outline` | 顯示其他人選取的物件 |
| `omni.kit.collaboration.viewport.camera` | 同步 / 跟隨其他人的攝影機 |
| `omni.kit.widget.live` | Live Session 狀態顯示 |
| `omni.timeline.live_session` | 時間軸的 Live Session 支援 |

### 資產匯入與管理

| Extension | 用途 |
|-----------|------|
| `omni.kit.browser.asset` | NVIDIA 資產瀏覽器 |
| `omni.kit.browser.sample` | 範例場景瀏覽器 |
| `omni.kit.tool.asset_importer` | 資產匯入工具 |
| `omni.kit.converter.cad` | CAD 檔案轉換器 |
| `omni.scene.optimizer.bundle` | 場景優化工具 |

### 渲染

| Extension | 用途 |
|-----------|------|
| `omni.hydra.pxr` | Pixar Hydra 渲染 |
| `omni.kit.viewport.rtx` | RTX 渲染 bundle |
| `omni.rtx.settings.core` | 渲染設定 |
| `omni.light_rigs` | 預設燈光配置 |

---

## 五、關鍵設定解析

### 介面精簡化

USD Explorer 刻意隱藏了許多進階功能，讓介面更適合「瀏覽者」而非「開發者」：

```toml
# 隱藏的功能
[settings.app.primCreation]
enableMenuAudio = false        # 隱藏音訊建立
enableMenuCamera = false       # 隱藏攝影機建立
hideShapes = true              # 隱藏 Create→Shape 選單

[settings.app.viewport.show]
audio = false                  # 不顯示音訊物件
camera = false                 # 不顯示攝影機物件
lights = false                 # 不顯示燈光物件

# 排除的 extension
[settings.app.extensions]
excluded = [
    "omni.kit.viewport.menubar.render",    # 隱藏渲染器切換
    "omni.kit.viewport.menubar.settings",  # 隱藏 viewport 設定
]
```

### 攝影機與導航

```toml
[settings.persistent.app.viewport]
camMoveVelocity = 1.5          # 攝影機移動速度
camVelocityMax = 50            # 最大速度
camVelocityMin = 0.01          # 最小速度
pickingMode = "kind:model.ALL" # 選取模式：選整個 model

[settings.persistent.app.viewport.manipulator.camera]
flyAcceleration = 1000.0       # 飛行加速度
flyDampening = 10.0            # 飛行阻尼
lookAcceleration = 2000.0      # 觀看加速度
tumbleAcceleration = 2000.0    # 旋轉加速度
```

### RTX 渲染優化

```toml
[settings.rtx.ecoMode]
enabled = true                 # 省電模式

[settings.rtx.post]
dlss.execMode = 1              # DLSS Balanced（效能與品質平衡）
histogram.enabled = true       # 自動曝光

[settings.rtx.reflections]
maxRoughness = 0.11            # 降低反射品質以提升效能（預設 0.3）

[settings.rtx-transient.hydra]
conservativeMemoryLimits = true     # 記憶體不足時停止載入幾何
maxInstanceCount = 12000000         # 最多 1200 萬個 instance
```

### 預設資產來源

```toml
[settings.exts."omni.kit.browser.asset"]
folders = [
    ".../Assets/ArchVis/Commercial",      # 商業建築資產
    ".../Assets/ArchVis/Industrial",       # 工業建築資產
    ".../Assets/DigitalTwin/Assets/Warehouse",  # 倉庫數位孿生資產
]

[settings.exts."omni.kit.browser.sample"]
folders = [
    ".../Usd_Explorer/Samples/Examples/2023_2",  # 範例場景
]
```

### 支援的 GPU

```toml
[settings.exts."omni.kit.compatibility_checker"]
supportedGpus = [
    "*GeForce RTX ????*",
    "*Quadro RTX ????*",
    "*RTX ?????*",
    "*RTX????*",
    "*TITAN RTX*"            # ← 目前使用的 GPU
]
```

---

## 六、Kit Base Editor vs USD Explorer — 選擇指南

```
需要建立「通用 3D 編輯器」？
  └─ 選 kit_base_editor
  └─ 自由度高，功能模組自己挑選
  └─ 適合：開發者、技術團隊

需要建立「場景瀏覽 / 審閱工具」？
  └─ 選 omni_usd_explorer
  └─ 預設就有導航、標記、測量、協作功能
  └─ 適合：數位孿生、設施規劃、專案審閱

需要建立「機器人模擬環境」？
  └─ 選 Isaac Sim 相關模板（別的 repo）
```

---

## 七、與數位孿生的關聯

USD Explorer 的設計完全對準「大型設施數位孿生」的使用場景：

| 數位孿生需求 | USD Explorer 對應功能 |
|-------------|---------------------|
| 匯入工廠 CAD 圖 | `omni.kit.converter.cad` |
| 瀏覽大型場景 | Waypoint 導航、攝影機播放清單 |
| 多人同時審閱 | Live Session 協作功能 |
| 標記問題區域 | Markup 標記工具 |
| 測量距離尺寸 | Measure 測量工具 |
| 擺放設備資產 | NVIDIA 資產瀏覽器 + 資產匯入 |
| 效能優化 | DLSS、省電模式、記憶體管理 |
| 場景優化 | Scene Optimizer |
