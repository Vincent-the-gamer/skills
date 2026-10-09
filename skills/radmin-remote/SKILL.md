---
name: radmin-remote
description: Use Radmin Viewer 3 on Windows to connect to a remote computer, and drive its authentication dialog programmatically. Use when the user asks to 远程/remote into a host by IP with Radmin, needs full-control or view-only control, needs a non-default mode (file transfer, telnet, text chat, voice chat, send message, shutdown), or asks which command-line switches Radmin supports.
---

# Radmin 远程连接

Radmin Viewer 3 是 **dialog-driven** 的：连接目标可以放命令行，凭据必须走弹出的认证对话框。命令行没有 `/user` 或 `/password`，传了不会报错，只会让主窗口保持隐藏、对话框也不弹——静默失败，比报错更难查。

## 快捷路径

有现成脚本时直接调用，它把下面第 1–4 步全做完了：

```powershell
& "C:\Users\mer\.config\opencode\skills\radmin-remote\scripts\connect.ps1" `
  -Address <IP> -User admin -Password (Read-Host -AsPlainText "密码")
```

脚本参数化的凭据不落盘。用户口述的密码不要写进任何文件。

## 手动流程

### 1. 探测可达性

Radmin Server 默认端口 4899。**完成判据**：`TcpTestSucceeded : True`。

```powershell
Test-NetConnection -ComputerName <IP> -Port 4899 -WarningAction SilentlyContinue |
  Select-Object RemoteAddress, TcpTestSucceeded
```

端口不通就停下并报告——后面每一步都会无声地卡住。这不是防火墙能自己好的情况，先问用户对端是否装了 Radmin Server、端口是否改过。

### 2. 启动 Viewer 并发起连接

```powershell
Start-Process "C:\Program Files (x86)\Radmin Viewer 3\Radmin.exe" `
  -ArgumentList "/connect:<IP>:4899"
```

不带模式开关即为 Full Control（完全控制）。View Only 加 `/noinput`，其余模式见 `references/commands.md`。

等 3–5 秒再进下一步，对话框是异步弹出的。

### 3. 找到认证对话框

**按进程找，不要按标题找。** 本机 Radmin 是中文版，标题 `Radmin 安全对话: <IP>` 里的中文经 `GetWindowText` 取回来是乱码，用 `FindWindow` 按标题匹配会返回 `0x0`——而 `Get-Process` 显示的 `MainWindowTitle` 有时是空的，两种直觉写法都会失败。

判据：Radmin 进程名下**可见**的、窗口类为 `#32770`（Win32 对话框类）的那个窗口。

```powershell
$p = Get-Process Radmin
# 枚举该 PID 的顶层窗口，筛 IsWindowVisible 且 GetClassName -eq '#32770'
```

**完成判据**：拿到一个非零句柄。拿不到就重试第 2 步；重复两次仍无对话框，说明凭据路径或服务端权限有问题，报告给用户而不是继续。

### 4. 填入凭据并提交

对话框内的控件 ID（同一版本下稳定）：

| 控件        | ID   |
| ----------- | ---- |
| 用户名 Edit | 2047 |
| 密码 Edit   | 2048 |
| 确定 Button | 120  |
| 取消 Button | 2    |

用 `GetDlgItem` 取句柄，再 `SendMessage`：

```powershell
$WM_SETTEXT = 0x000C   # 写入文本
$BM_CLICK   = 0x00F5   # 点击
```

`GetDlgItem` 会在对话框子树里递归查找，不必自己枚举子控件。密码框是 `ES_PASSWORD`，但 `WM_SETTEXT` 一样能写进去。

### 5. 验证连接

**完成判据**，两条都要满足：

```powershell
Get-NetTCPConnection -RemoteAddress <IP> -ErrorAction SilentlyContinue |
  Where-Object State -eq 'Established'
```

以及 Radmin 进程名下出现一个可见的、类名非 `#32770` 的窗口（即连接窗口本身）。中文版标题含 `全程控制`，英文版是 `Full Control`——**以 TCP Established 为准**，标题是本地化的，不稳。

窗口没出来、TCP 停在 `TimeWait`：认证被拒。重新走第 2–4 步，先向用户确认账号密码，以及对端 Radmin Server 的权限设置是否给该用户开了 Full Control。

## 常见故障

| 现象                         | 原因                                           |
| ---------------------------- | ---------------------------------------------- |
| 主窗口隐藏、无对话框、无报错 | 命令行传了不存在的 `/user`、`/password` 等开关 |
| TCP 停在 `TimeWait`          | 认证被拒，或该用户无此模式权限                 |
| 对话框句柄找不到             | 按标题匹配了中文窗口名（编码不匹配）           |
| `MainWindowTitle` 为空       | 对话框弹出前后该字段本就不可靠，改用窗口类枚举 |
