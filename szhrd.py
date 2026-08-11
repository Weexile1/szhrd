# -*- coding: utf-8 -*-
"""数字华容道 - 3x3 / 4x4 / 5x5"""

import random
import tkinter as tk
from tkinter import messagebox


# 颜色
BG = "#1a2332"
PANEL = "#243447"
TILE = "#3d7ea6"
TILE_HOVER = "#4a9bc7"
EMPTY = "#15202b"
TEXT = "#e8f1f8"
ACCENT = "#f0a500"
BTN = "#2e5a7e"
BTN_HOVER = "#3a7aab"


class NumberPuzzle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("数字华容道")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.size = 3
        self.board = []
        self.empty = (0, 0)
        self.moves = 0
        self.won = False
        self.tile_btns = []
        self.cell = 72

        self._build_menu()
        self._center_window(420, 280)
        self.root.mainloop()

    def _center_window(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------- 主菜单 ----------
    def _build_menu(self):
        self._clear()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True, fill="both", padx=30, pady=24)

        tk.Label(
            frame, text="数字华容道", font=("Microsoft YaHei UI", 28, "bold"),
            fg=ACCENT, bg=BG,
        ).pack(pady=(10, 6))

        tk.Label(
            frame, text="选择难度，用方向键或 WASD 移动方块",
            font=("Microsoft YaHei UI", 11), fg=TEXT, bg=BG,
        ).pack(pady=(0, 20))

        for n, label in ((3, "3 × 3  入门"), (4, "4 × 4  进阶"), (5, "5 × 5  挑战")):
            b = tk.Button(
                frame, text=label, font=("Microsoft YaHei UI", 14),
                fg=TEXT, bg=BTN, activeforeground=TEXT, activebackground=BTN_HOVER,
                relief="flat", cursor="hand2", width=18, pady=8,
                command=lambda s=n: self._start_game(s),
            )
            b.pack(pady=6)
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=BTN))

        self._center_window(420, 380)

    # ---------- 开始游戏 ----------
    def _start_game(self, size):
        self.size = size
        self.moves = 0
        self.won = False
        self.cell = {3: 90, 4: 78, 5: 66}[size]
        self._init_board()
        self._shuffle(size * size * 30)
        self._build_game_ui()

    def _init_board(self):
        n = self.size
        self.board = [[r * n + c + 1 for c in range(n)] for r in range(n)]
        self.board[n - 1][n - 1] = 0
        self.empty = (n - 1, n - 1)

    def _shuffle(self, steps):
        """从已解状态做合法随机移动，保证可解"""
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        last = None
        for _ in range(steps):
            er, ec = self.empty
            candidates = []
            for dr, dc in dirs:
                nr, nc = er + dr, ec + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if last is None or (nr, nc) != last:
                        candidates.append((nr, nc))
            if not candidates:
                continue
            nr, nc = random.choice(candidates)
            self.board[er][ec], self.board[nr][nc] = self.board[nr][nc], 0
            last = self.empty
            self.empty = (nr, nc)

    # ---------- 游戏界面 ----------
    def _build_game_ui(self):
        self._clear()
        n = self.size
        pad = 20
        board_px = n * self.cell + (n + 1) * 6
        win_w = max(board_px + pad * 2, 360)
        win_h = board_px + 140

        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=pad, pady=(16, 8))

        self.info_label = tk.Label(
            top, text=self._info_text(), font=("Microsoft YaHei UI", 12),
            fg=TEXT, bg=BG,
        )
        self.info_label.pack(side="left")

        tk.Button(
            top, text="重新开始", font=("Microsoft YaHei UI", 10),
            fg=TEXT, bg=BTN, activeforeground=TEXT, activebackground=BTN_HOVER,
            relief="flat", cursor="hand2", padx=10, pady=2,
            command=lambda: self._start_game(self.size),
        ).pack(side="right", padx=(6, 0))

        tk.Button(
            top, text="返回菜单", font=("Microsoft YaHei UI", 10),
            fg=TEXT, bg=BTN, activeforeground=TEXT, activebackground=BTN_HOVER,
            relief="flat", cursor="hand2", padx=10, pady=2,
            command=self._build_menu,
        ).pack(side="right")

        board_frame = tk.Frame(self.root, bg=PANEL, padx=6, pady=6)
        board_frame.pack(padx=pad, pady=8)

        self.tile_btns = []
        for r in range(n):
            row = []
            for c in range(n):
                btn = tk.Button(
                    board_frame,
                    font=("Microsoft YaHei UI", max(16, self.cell // 4), "bold"),
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda rr=r, cc=c: self._click(rr, cc),
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                board_frame.grid_rowconfigure(r, minsize=self.cell)
                board_frame.grid_columnconfigure(c, minsize=self.cell)
                row.append(btn)
            self.tile_btns.append(row)

        tip = tk.Label(
            self.root,
            text="方向键 / WASD 移动  ·  点击与缺口相邻的方块也可移动",
            font=("Microsoft YaHei UI", 9), fg="#8aa0b4", bg=BG,
        )
        tip.pack(pady=(4, 12))

        self.root.bind("<KeyPress>", self._on_key)
        self.root.focus_set()
        self._draw()
        self._center_window(win_w, win_h)

    def _info_text(self):
        return f"{self.size}×{self.size} 模式    步数：{self.moves}"

    def _draw(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                btn = self.tile_btns[r][c]
                if val == 0:
                    btn.configure(
                        text="", bg=EMPTY, activebackground=EMPTY,
                        state="disabled", disabledforeground=EMPTY,
                    )
                else:
                    btn.configure(
                        text=str(val), bg=TILE, fg=TEXT,
                        activebackground=TILE_HOVER, activeforeground=TEXT,
                        state="normal",
                    )
        self.info_label.configure(text=self._info_text())

    # ---------- 操作 ----------
    def _neighbors_of_empty(self):
        er, ec = self.empty
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = er + dr, ec + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                yield nr, nc

    def _move_tile(self, r, c):
        if self.won:
            return
        if (r, c) not in self._neighbors_of_empty():
            return
        er, ec = self.empty
        self.board[er][ec] = self.board[r][c]
        self.board[r][c] = 0
        self.empty = (r, c)
        self.moves += 1
        self._draw()
        if self._is_solved():
            self.won = True
            self.root.after(80, self._show_win)

    def _click(self, r, c):
        self._move_tile(r, c)

    def _on_key(self, event):
        if self.won:
            return
        key = event.keysym.lower()
        # 按键表示“把缺口往哪个方向推”，等价于对面的方块滑入缺口
        mapping = {
            "up": (1, 0), "w": (1, 0),
            "down": (-1, 0), "s": (-1, 0),
            "left": (0, 1), "a": (0, 1),
            "right": (0, -1), "d": (0, -1),
        }
        if key not in mapping:
            return
        dr, dc = mapping[key]
        er, ec = self.empty
        tr, tc = er + dr, ec + dc
        if 0 <= tr < self.size and 0 <= tc < self.size:
            self._move_tile(tr, tc)

    def _is_solved(self):
        n = self.size
        expect = 1
        for r in range(n):
            for c in range(n):
                if r == n - 1 and c == n - 1:
                    return self.board[r][c] == 0
                if self.board[r][c] != expect:
                    return False
                expect += 1
        return True

    def _show_win(self):
        again = messagebox.askyesno(
            "通关！",
            f"恭喜！你用了 {self.moves} 步完成 {self.size}×{self.size} 华容道。\n\n再来一局？",
        )
        if again:
            self._start_game(self.size)
        else:
            self._build_menu()


if __name__ == "__main__":
    NumberPuzzle()
