# Windows 工作日自动换壁纸

这个文件夹可以直接上传到 GitHub，然后在你的 Windows 电脑上使用。

## 文件说明

- `Set-WeekdayWallpaper.ps1`：根据当天是周几（周一到周五）自动切换对应壁纸。
- `Install-WeekdayWallpaperTask.ps1`：一键创建 Windows 计划任务（默认每天 **06:30** 执行一次，且电脑开机时也会执行）。

## 壁纸文件准备

请在本目录新建 `wallpapers` 文件夹，并放入以下 5 张图片（文件名必须一致）：

- `monday.jpg`
- `tuesday.jpg`
- `wednesday.jpg`
- `thursday.jpg`
- `friday.jpg`

> 你给我的五张课表图，就分别重命名为上面这 5 个名字即可。

## 首次安装（Windows）

以管理员身份打开 PowerShell，进入该目录后执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-WeekdayWallpaperTask.ps1
```

## 立即测试

```powershell
.\Set-WeekdayWallpaper.ps1
```

## 自定义每天执行时间（可选）

例如改成每天 07:00：

```powershell
.\Install-WeekdayWallpaperTask.ps1 -DailyTime "07:00"
```

> 无论你设置几点，脚本都会保留“开机时执行”这个触发器。
