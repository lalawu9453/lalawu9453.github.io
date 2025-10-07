# AnyThreads

[English Version](README.en.md)

一個以 Hugo 為核心、具備 AI 輔助能力的自動化部落格內容引擎。

---

## 專案簡介

![](./branner.jpg)

本專案旨在打造一個高度自動化、SEO 友善且具備獨特使用者體驗的豪華部落格。它不僅是一個內容發布平台，更是一個能透過 AI 輔助與自動化流程，持續擴展內容、提升網站權重與流量的「內容引擎」。

### 主要功能

- **高效內容管理**: 使用 Hugo 進行極速靜態網站生成。
- **AI 輔助標籤**: 內建 Python 腳本，可自動掃描文章並透過 AI 建議、增強、及管理標籤。
- **客製化 UI/UX**: 包含獨特的環境音效控制列，並對字體、顏色、版面進行了第一階段優化，提升閱讀體驗。
- **版本化開發環境**: 使用 `uv` 進行 Python 環境與依賴管理，確保開發環境的一致性。

## 技術棧 (Technology Stack)

- **靜態網站生成**: Hugo
- **腳本與自動化**: Python 3
- **Python 環境管理**: uv
- **主題**: loficode (經過客製化修改)

## 本地開發指南 (Getting Started)

請依照以下步驟在你的本地端電腦上設定並運行此專案。

### 1. 環境準備

請確保你的電腦已安裝以下軟體：
- [Git](https://git-scm.com/)
- [Hugo (extended version)](https://gohugo.io/installation/)
- [uv (Python package installer)](https://github.com/astral-sh/uv)

### 2. 專案初始化

```bash
# 1. 複製專案到本地
git clone <repository-url>
cd ai-reporter

# 2. 初始化並拉取 Hugo 主題 (Submodule)
git submodule update --init --recursive

# 3. 同步 Python 開發環境
# (uv 會自動偵測 uv.lock 並安裝所有必要的 Python 函式庫)
uv sync
```

### 3. 運行本地伺服器

完成初始化後，執行以下指令來啟動 Hugo 的本地開發伺服器：

```bash
# -D 參數會同時建立草稿 (draft) 頁面
hugo server -D
```

伺服器啟動後，你可以在瀏覽器中打開 `http://localhost:1313/` 來查看網站。

## 使用方式

### AI 標籤處理器

本專案包含一個用於管理文章標籤的 Python 腳本。你可以透過以下指令運行它：

```bash
# 腳本會自動掃描文章、提出建議並更新檔案
uv run python scripts/tag_processor.py
```

## 授權 (License)

本專案採用 MIT 授權。
