# Omniverse Kit 檔案（`.kit`）說明

## 什麼是 `.kit` 檔案？

`.kit` 檔案是 **Omniverse Kit 應用程式的定義檔**，格式為 **TOML**。它等同於應用程式的「組裝清單」，定義了：

- 這個 app 的基本資訊（名稱、版本）
- 要載入哪些 Extensions（模組/插件）
- 各種預設設定值

Kit Runtime 啟動時讀取此檔案，決定要組合哪些模組形成完整的應用程式。

> **核心概念**：Omniverse 的架構是高度模組化的，所有功能都是 Extension，`.kit` 檔就是把這些 Extension 黏在一起的膠水。

---

## 檔案結構解析

以 `my_company.my_editor.kit` 為例：

### `[package]` — 套件元資料

```toml
[package]
title = "My Editor"                # 顯示名稱
version = "0.1.0"                  # 版本號
description = """描述文字"""        # 應用描述
keywords = ["app"]                 # 標籤，UI 可用 "app" 篩選
template_name = "kit_base_editor"  # 產生此檔案的模板名稱
```

---

### `[dependencies]` — 要載入的 Extensions

這是最核心的部分。每一行都是一個 extension，`{}` 代表不指定版本（使用預設版本）。

#### 渲染相關

| Extension | 用途 |
|-----------|------|
| `omni.hydra.rtx` | RTX 渲染器 |
| `omni.hydra.usdrt_delegate` | Fabric Scene Delegate（FabricSceneDelegate 為 True 時必要） |
| `omni.rtx.settings.core` | RTX 渲染設定 |
| `omni.hydra.engine.stats` | HUD 統計資訊（解析度、FPS 等） |

#### Viewport（3D 視窗）

| Extension | 用途 |
|-----------|------|
| `omni.kit.viewport.window` | 核心 Viewport 視窗 |
| `omni.kit.viewport.menubar.camera` | 攝影機選單 |
| `omni.kit.viewport.menubar.display` | 顯示模式選單 |
| `omni.kit.viewport.menubar.lighting` | 燈光選單 |
| `omni.kit.viewport.menubar.render` | 渲染器切換選單 |
| `omni.kit.viewport.menubar.settings` | Viewport 設定選單 |
| `omni.kit.viewport.ready` | 啟動時顯示 RTX 載入資訊 |
| `omni.kit.viewport.scene_camera_model` | 同步攝影機至場景 UI |
| `omni.kit.viewport.legacy_gizmos` | 網格與 Gizmo 繪製 |

#### 操作工具

| Extension | 用途 |
|-----------|------|
| `omni.kit.manipulator.camera` | 攝影機導航（平移、旋轉、縮放視角） |
| `omni.kit.manipulator.prim` | 物件操作（移動、旋轉、縮放物件） |
| `omni.kit.manipulator.selection` | 選取物件 |

#### UI 視窗

| Extension | 用途 |
|-----------|------|
| `omni.kit.mainwindow` | 主視窗框架 |
| `omni.kit.window.console` | 主控台/日誌視窗 |
| `omni.kit.window.content_browser` | 內容瀏覽器 |
| `omni.kit.window.property` | 屬性面板 |
| `omni.kit.window.stage` | Stage 樹狀結構 |
| `omni.kit.window.status_bar` | 狀態列 |
| `omni.kit.window.toolbar` | 工具列 |

#### 選單

| Extension | 用途 |
|-----------|------|
| `omni.kit.menu.file` | File 選單 |
| `omni.kit.menu.edit` | Edit 選單 |
| `omni.kit.menu.create` | Create 選單 |
| `omni.kit.menu.common` | 共用選單元件（`order = 1000` 確保最後載入） |

#### OmniGraph（視覺化程式設計）

| Extension | 用途 |
|-----------|------|
| `omni.graph.core` | Graph Runtime 核心 |
| `omni.graph.action` | Action Graph Runtime |
| `omni.graph.nodes` | Action Graph 節點 |
| `omni.graph.scriptnode` | Script Node 支援 |
| `omni.graph.ui_nodes` | UI 節點 |

#### 其他功能

| Extension | 用途 |
|-----------|------|
| `omni.physx.stageupdate` | PhysX 物理模擬 Runtime |
| `omni.kit.material.library` | 材質建立與指派 |
| `omni.kit.primitive.mesh` | 基本幾何體（cube、sphere 等） |
| `omni.kit.tool.asset_importer` | 資產匯入工具 |
| `omni.kit.tool.collect` | USD Collect 工具 |
| `omni.warp.core` | Warp GPU 計算框架 |
| `omni.uiaudio` | 音訊播放 |
| `omni.anim.curve.core` | 動畫曲線 Runtime |
| `omni.kit.raycast.query` | RTX 光線投射查詢 |

---

### `[settings]` — 全域設定

```toml
[settings]
crashreporter.compressDumpFiles = true           # crash dump 壓縮
renderer.gpuEnumeration.glInterop.enabled = false # 關閉 GL interop（加速啟動）
renderer.asyncInit = true                        # 渲染器非同步初始化（加速啟動）
rtx.ecoMode.enabled = true                      # 省電模式（空閒時降低 GPU 負載）
rtx.hydra.mdlMaterialWarmup = true               # 提前載入 MDL shader
```

---

### `[settings.app]` — 應用程式設定

```toml
[settings.app]
content.emptyStageOnStart = true     # 啟動後建立空 Stage
font.file = "${fonts}/OpenSans-SemiBold.ttf"  # UI 字型
font.size = 16                       # 字型大小
hangDetector.enabled = true          # 啟用卡住偵測
hangDetector.timeout = 120           # 120 秒無回應視為卡住
renderer.skipWhileMinimized = true   # 最小化時停止渲染
window.title = "My Editor"          # 視窗標題
```

---

### `[settings.app.exts]` — Extension 搜尋路徑

```toml
[settings.app.exts]
folders.'++' = [           # '++' 是 append 語法，加入額外搜尋路徑
    "${app}/../exts",      # 本地自定義 extensions 目錄
    "${app}/../extscache/" # 快取的 extensions 目錄
]
```

> `${app}` 變數會被解析為 `.kit` 檔案所在的目錄路徑。

---

### `[[test]]` — 測試設定

```toml
[[test]]
args = [
    "--/app/file/ignoreUnsavedOnExit=true"  # 測試時忽略未儲存變更的提示
]
```

---

### `[template]` — 模板元資料

```toml
[template]
type = "ApplicationTemplate"  # repo template 工具使用的標記
```

---

## 重點整理

- `.kit` 檔案是 TOML 格式的應用程式定義檔
- 透過 `[dependencies]` 組合不同 Extensions 來建構應用功能
- `[settings]` 系列區段控制渲染、UI、效能等行為
- 增減 `[dependencies]` 就能客製化應用程式功能
- `${app}` 和 `${fonts}` 是 Kit 提供的路徑變數，Runtime 時自動解析
