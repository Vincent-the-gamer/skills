# Radmin 命令行参考

来源：安装目录自带帮助 `Radmin30.chm`（`ViewerCMD.htm` / `CMD.htm`）。

Viewer 与 Server 是两个不同的 exe，开关集不通用。

## Viewer — `Radmin.exe`

安装路径默认 `C:\Program Files (x86)\Radmin Viewer 3\Radmin.exe`。

### 连接

| 开关 | 作用 |
|---|---|
| `/connect:<address>:<port>` | 直连，不经 phonebook。不带模式开关 = Full Control |
| `/through:<address>:<port>` | 经中间 Radmin Server 中转。须与 `/connect` 同用 |
| `/pbpath"<path>"` | 指定 phonebook 文件启动 |

### 模式（与 `/connect` 同用）

| 开关 | 模式 |
|---|---|
| *(无)* | Full Control 完全控制 |
| `/noinput` | View Only 仅查看 |
| `/telnet` | Telnet 文本终端 |
| `/file` | File Transfer 文件传输 |
| `/shutdown` | Shutdown 关机 |
| `/chat` | Text Chat 文字聊天 |
| `/voice` | Voice Chat 语音聊天 |
| `/message` | Send Message 弹窗消息 |

### 显示与性能（须配合 Full Control 或 `/noinput`）

| 开关 | 作用 |
|---|---|
| `/fullscreen` | 全屏显示，不拉伸 |
| `/fullstretch` | 全屏并拉伸以匹配分辨率差异 |
| `/nofullkbcontrol` | Full Control 下不转发系统热键（如 Alt-Tab） |
| `/monitor"<\\.\DISPLAYn>"` | 多显示器时指定用哪块屏 |
| `/24bpp` `/16bpp` `/8bpp` `/4bpp` `/2bpp` `/1bpp` | 色深，越低越省带宽 |
| `/updates:<n>` | 每秒最大屏幕刷新次数 |

### 其他

| 开关 | 作用 |
|---|---|
| `/sendrequest /requestfile"<req>" /licensefile"<lic>" [/outputfile"<log>"]` | 把激活请求发给 Famatech 激活服务器，保存授权文件 |
| `/?` | 弹窗列出所有开关 |

### 不存在的开关

Viewer **没有** `/user`、`/password`、`/fullscreen:yes` 之类的凭据或布尔开关。凭据只能在认证对话框里填（见 `../SKILL.md`）。传入未识别的开关不会报错，会静默失败。

## Server — `RServer3.exe`

装在被控端，服务名 `Rserver3`。仅管理自身状态，**不含连接目标**。

| 开关 | 作用 |
|---|---|
| `/setup` | 显示设置窗口，不启动服务 |
| `/start` | 启动服务（须已正确安装） |
| `/stop` | 停止服务 |
| `/activate /key:<key> [/outputfile"<log>"]` | 用远程计算机的网络连接激活 |
| `/saverequest /key:<key> /requestfile"<req>" [/outputfile"<log>"]` | 保存离线激活所需的请求文件 |
| `/uselicense /licensefile"<lic>" [/outputfile"<log>"]` | 用授权文件激活 |
| `/?` | 弹窗列出所有开关 |

## 连接模式语义

| 模式 | 能做什么 |
|---|---|
| Full Control | 看远程桌面并用本地键鼠操控 |
| View Only | 只看，键鼠不转发 |
| Telnet | 文本终端，跑系统命令和无界面程序 |
| File Transfer | 双向传文件，支持断点续传 |
| Shutdown | 两下鼠标关掉远程计算机 |
| Text Chat | 与同机所有连接者文字聊天 |
| Voice Chat | 与同机所有连接者麦克风通话 |
| Send Message | 在远程桌面弹出文本消息 |
| Intel AMT | 开关机、改 BIOS、OS 未加载前接管启动流程、从 CD/ISO 启动 |

AMT 模式不能用命令行开关发起，在 Viewer 界面里选。
