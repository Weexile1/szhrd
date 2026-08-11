 szhrd
数字华容道：3×3 / 4×4 / 5×5 滑动拼图，支持网页在线玩与 Python 桌面版
 玩法说明

棋盘为 `n × n`，含 `n² − 1` 个数字方块与 **1 个空缺**。

- 数字范围：`1` ～ `n² − 1`
- 仅可与空缺相邻的方块上下左右滑动
- 开局从已解状态经合法随机移动打乱，保证可解
- **通关条件**：数字自上而下、自左而右按 `1 → 最大数` 排列，空缺位于右下角

| 模式 | 规模 | 方块数 |
|------|------|--------|
| 入门 | 3×3 | 8 |
| 进阶 | 4×4 | 15 |
| 挑战 | 5×5 | 24 |

 操作

| 方式 | 说明 |
|------|------|
| 方向键 / WASD | 移动方块（空缺相对移动） |
| 鼠标 / 触屏点击 | 点击与空缺相邻的方块 |

---

 网页版（在线玩）

入口文件：[`index.html`](./index.html)

适合部署到 **GitHub Pages**，打开即可游玩，无需安装。

本地预览

```bash
# 进入本仓库目录后
python -m http.server 8000
```

浏览器访问：<http://localhost:8000>

也可直接用浏览器打开 `index.html`。

部署 GitHub Pages

1. 将本仓库推送到 GitHub（公开仓库）
2. 仓库 **Settings → Pages**
3. Source 选择 `Deploy from a branch`
4. Branch 选 `main`，文件夹选 `/ (root)`
5. 保存后访问：

```text
https://<你的用户名>.github.io/<仓库名>/
```

> 请确保 `index.html` 位于仓库根目录。

---

## 桌面版（Python）

入口文件：[`szhrd.py`](./szhrd.py)

基于标准库 **tkinter**，无需第三方依赖。

### 环境要求

- Python 3.8+
- tkinter（Windows / macOS 官方安装包通常已包含；部分 Linux 需自行安装，如 `sudo apt install python3-tk`）

### 运行

```bash
python szhrd.py
```

---

## 项目结构

```text
.
├── index.html   # 网页版（GitHub Pages 入口）
├── szhrd.py     # Python 桌面版
└── README.md
```

---

## 技术说明

- **可解性**：打乱时不采用任意置换，而是从完成态执行若干次合法滑动，避免无解局面
- **网页版**：纯前端（HTML / CSS / JavaScript），无后端、无构建步骤
- **桌面版**：tkinter GUI，交互与网页版规则一致

---

## License

MIT
