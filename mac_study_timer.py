import tkinter as tk
from tkinter import ttk, messagebox
import time


class StudyTimerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Daily Study Timer")
        self.root.geometry("560x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F7")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        self.daily_goal_minutes = 120
        self.study_minutes = 50
        self.break_minutes = 10

        self.running = False
        self.on_break = False
        self.remaining_seconds = 0
        self.total_study_done = 0
        self.timer_job = None
        self.day_stamp = time.strftime("%Y-%m-%d")

        self._build_ui()
        self._refresh_labels()

    def _configure_styles(self):
        self.style.configure("Card.TFrame", background="#FFFFFF")
        self.style.configure("Title.TLabel", font=("SF Pro Display", 24, "bold"), background="#F5F5F7", foreground="#111111")
        self.style.configure("SubTitle.TLabel", font=("SF Pro Text", 11), background="#F5F5F7", foreground="#6E6E73")
        self.style.configure("CardTitle.TLabel", font=("SF Pro Text", 12, "bold"), background="#FFFFFF", foreground="#1D1D1F")
        self.style.configure("CardValue.TLabel", font=("SF Pro Display", 30, "bold"), background="#FFFFFF", foreground="#0071E3")
        self.style.configure("Body.TLabel", font=("SF Pro Text", 11), background="#FFFFFF", foreground="#3A3A3C")
        self.style.configure("Primary.TButton", font=("SF Pro Text", 11, "bold"), foreground="#FFFFFF", background="#0071E3", borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", "#005BBB")])
        self.style.configure("Secondary.TButton", font=("SF Pro Text", 10), foreground="#1D1D1F", background="#E8E8ED", borderwidth=0)
        self.style.map("Secondary.TButton", background=[("active", "#D8D8DE")])

    def _build_ui(self):
        header = ttk.Frame(self.root, style="Card.TFrame")
        header.place(x=20, y=20, width=520, height=90)

        ttk.Label(self.root, text="学习节奏助手", style="Title.TLabel").place(x=28, y=30)
        ttk.Label(self.root, text="苹果风格 · 每日目标 + 学习/休息循环", style="SubTitle.TLabel").place(x=30, y=70)

        self.timer_card = ttk.Frame(self.root, style="Card.TFrame")
        self.timer_card.place(x=20, y=120, width=520, height=210)

        ttk.Label(self.timer_card, text="当前倒计时", style="CardTitle.TLabel").place(x=22, y=18)
        self.timer_text = ttk.Label(self.timer_card, text="00:00", style="CardValue.TLabel")
        self.timer_text.place(x=20, y=52)

        self.phase_text = ttk.Label(self.timer_card, text="未开始", style="Body.TLabel")
        self.phase_text.place(x=24, y=110)

        self.progress_text = ttk.Label(self.timer_card, text="今日已学习：0 分钟 / 120 分钟", style="Body.TLabel")
        self.progress_text.place(x=24, y=136)

        ttk.Button(self.timer_card, text="开始学习", style="Primary.TButton", command=self.start_session).place(x=24, y=164, width=110, height=34)
        ttk.Button(self.timer_card, text="暂停", style="Secondary.TButton", command=self.pause_session).place(x=144, y=164, width=90, height=34)
        ttk.Button(self.timer_card, text="重置", style="Secondary.TButton", command=self.reset_session).place(x=242, y=164, width=90, height=34)

        settings_card = ttk.Frame(self.root, style="Card.TFrame")
        settings_card.place(x=20, y=344, width=520, height=250)

        ttk.Label(settings_card, text="参数设置", style="CardTitle.TLabel").place(x=22, y=16)

        ttk.Label(settings_card, text="每日学习目标（分钟）", style="Body.TLabel").place(x=24, y=56)
        self.goal_var = tk.StringVar(value=str(self.daily_goal_minutes))
        ttk.Entry(settings_card, textvariable=self.goal_var).place(x=240, y=56, width=250, height=30)

        ttk.Label(settings_card, text="单次学习时长（分钟）", style="Body.TLabel").place(x=24, y=100)
        self.study_var = tk.StringVar(value=str(self.study_minutes))
        ttk.Entry(settings_card, textvariable=self.study_var).place(x=240, y=100, width=250, height=30)

        ttk.Label(settings_card, text="休息时长（分钟）", style="Body.TLabel").place(x=24, y=144)
        self.break_var = tk.StringVar(value=str(self.break_minutes))
        ttk.Entry(settings_card, textvariable=self.break_var).place(x=240, y=144, width=250, height=30)

        ttk.Button(settings_card, text="保存设置", style="Primary.TButton", command=self.save_settings).place(x=24, y=196, width=110, height=34)

    def save_settings(self):
        try:
            goal = int(self.goal_var.get())
            study = int(self.study_var.get())
            brk = int(self.break_var.get())
            if goal <= 0 or study <= 0 or brk <= 0:
                raise ValueError
            self.daily_goal_minutes = goal
            self.study_minutes = study
            self.break_minutes = brk
            if not self.running:
                self.remaining_seconds = self.study_minutes * 60
            self._refresh_labels()
            messagebox.showinfo("已保存", "设置已更新。")
        except ValueError:
            messagebox.showerror("输入错误", "请输入大于 0 的整数分钟值。")

    def start_session(self):
        self._sync_new_day()
        if not self.running:
            if self.remaining_seconds <= 0:
                self.remaining_seconds = (self.break_minutes if self.on_break else self.study_minutes) * 60
            self.running = True
            self._tick()

    def pause_session(self):
        self.running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def reset_session(self):
        self.pause_session()
        self.on_break = False
        self.remaining_seconds = self.study_minutes * 60
        self.phase_text.config(text="未开始")
        self._refresh_labels()

    def _tick(self):
        if not self.running:
            return

        self._sync_new_day()

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if not self.on_break:
                self.total_study_done += 1
            self._refresh_labels()
            self.timer_job = self.root.after(1000, self._tick)
            return

        self.on_break = not self.on_break
        self.remaining_seconds = (self.break_minutes if self.on_break else self.study_minutes) * 60

        if self.on_break:
            messagebox.showinfo("学习结束", "本轮学习完成，开始休息。")
        else:
            messagebox.showinfo("休息结束", "休息结束，开始下一轮学习。")

        if (self.total_study_done // 60) >= self.daily_goal_minutes:
            messagebox.showinfo("目标达成", "🎉 今日学习目标已完成！")

        self._refresh_labels()
        self.timer_job = self.root.after(1000, self._tick)

    def _sync_new_day(self):
        current_day = time.strftime("%Y-%m-%d")
        if current_day != self.day_stamp:
            self.day_stamp = current_day
            self.total_study_done = 0

    def _refresh_labels(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_text.config(text=f"{mins:02d}:{secs:02d}")
        phase = "休息中" if self.on_break else "学习中"
        if not self.running and self.remaining_seconds == 0:
            phase = "未开始"
        self.phase_text.config(text=f"当前阶段：{phase}")
        self.progress_text.config(
            text=f"今日已学习：{self.total_study_done // 60} 分钟 / {self.daily_goal_minutes} 分钟"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTimerApp(root)
    app.remaining_seconds = app.study_minutes * 60
    app._refresh_labels()
    root.mainloop()
