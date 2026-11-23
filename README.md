# 苹果风格学习定时器（桌面版）

这是一个使用 Python + Tkinter 实现的简洁桌面学习软件：

- 可设置每日学习目标（分钟）
- 可设置每轮学习时长、休息时长
- 自动在「学习 → 休息」之间循环
- 到时弹窗提醒，达到每日目标会提示完成
- 新增「每日 14:00 灵感学习提醒」：提醒去 GitHub、Dribbble、Behance 学习案例并完善 APP
- 界面为浅色、卡片化、简洁苹果风格

## 运行方式

1. 确认本机有 Python 3（自带 Tkinter）。
2. 在项目目录执行：

```bash
python3 mac_study_timer.py
```

## 灵感学习功能说明

- 默认开启每日 14:00 提醒。
- 到点后会弹窗提醒你学习案例。
- 可点击「打开灵感站点」一键打开以下平台：
  - GitHub（study timer app 相关仓库）
  - Dribbble（Pomodoro / Study UI）
  - Behance（Study Planner UI）

## 可继续扩展

- 增加本地数据持久化（保存历史统计）
- 增加深色模式
- 增加白噪音/番茄钟音效
- 增加 WebView 内嵌灵感面板
