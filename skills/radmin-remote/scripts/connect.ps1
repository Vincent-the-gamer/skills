<#
.SYNOPSIS
  Launch Radmin Viewer 3 and fill its authentication dialog automatically.

.DESCRIPTION
  Radmin Viewer has no /user or /password command-line switch; credentials must go
  through the popup auth dialog. This script finds the dialog by process + window
  class '#32770' (NOT by title -- on a Chinese-localized install the title comes
  back as mojibake from GetWindowText), then fills and submits it with
  GetDlgItem + SendMessage.

  NOTE: this file is deliberately ASCII-only. Windows PowerShell 5.1 decodes .ps1
  as ANSI (GBK on Chinese Windows) unless a BOM is present, and GBK re-decoding of
  non-ASCII text silently corrupts string literals and breaks parsing. Keep it ASCII.
  Also: a line starting with "+" does NOT continue the previous expression in
  PowerShell -- continuation needs the operator at the END of the line.

.PARAMETER Address
  Target IP or DNS name. Required.

.PARAMETER User
  Remote login. Required.

.PARAMETER Password
  Remote password. Plain string or SecureString. Prompts interactively when omitted
  (recommended -- keeps it out of shell history).

.PARAMETER Port
  Radmin Server port, default 4899.

.PARAMETER Mode
  Connection mode, default FullControl. See references/commands.md for the rest.

.PARAMETER TimeoutSec
  Seconds to wait for the auth dialog, default 10.

.EXAMPLE
  .\connect.ps1 -Address 172.28.1.26 -User admin

.EXAMPLE
  .\connect.ps1 -Address 172.28.1.26 -User admin -Mode ViewOnly -Verbose
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)] [string] $Address,
  [Parameter(Mandatory)] [string] $User,
  [securestring] $Password,
  [int] $Port = 4899,
  [ValidateSet('FullControl','ViewOnly','Telnet','FileTransfer','Shutdown','Chat','VoiceChat','Message')]
  [string] $Mode = 'FullControl',
  [int] $TimeoutSec = 10
)

$ErrorActionPreference = 'Stop'
$RadminExe = 'C:\Program Files (x86)\Radmin Viewer 3\Radmin.exe'

# Viewer mode switches. Full Control has no switch. See references/commands.md
$ModeSwitch = @{
  ViewOnly     = '/noinput'
  Telnet       = '/telnet'
  FileTransfer = '/file'
  Shutdown     = '/shutdown'
  Chat         = '/chat'
  VoiceChat    = '/voice'
  Message      = '/message'
}

if (-not (Test-Path $RadminExe)) { throw "Radmin Viewer not found: $RadminExe" }
if (-not $Password) { $Password = Read-Host -AsPlainText 'Radmin password' }

# --- 1. Reachability -------------------------------------------------------
Write-Verbose "Probing ${Address}:${Port} ..."
$probe = Test-NetConnection -ComputerName $Address -Port $Port -WarningAction SilentlyContinue
if (-not $probe.TcpTestSucceeded) {
  throw "${Address}:${Port} unreachable. Check that Radmin Server is installed and running"
}
Write-Verbose "Reachable via $($probe.SourceAddress.IPAddress)"

# --- 2. Launch Viewer ------------------------------------------------------
$before = @(Get-Process Radmin -ErrorAction SilentlyContinue).Id
$argList = @("/connect:${Address}:${Port}")
if ($ModeSwitch.ContainsKey($Mode)) { $argList += $ModeSwitch[$Mode] }
Write-Verbose "Starting: $RadminExe $($argList -join ' ')"
Start-Process -FilePath $RadminExe -ArgumentList $argList

# --- 3. Locate the auth dialog --------------------------------------------
# Find by process + visible + window class '#32770'. Title matching fails on
# localized installs.
Add-Type -TypeDefinition @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class Win {
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumWindowsProc cb, IntPtr l);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern IntPtr GetDlgItem(IntPtr dlg, int id);
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, string l);
  [DllImport("user32.dll")]
  public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  delegate bool EnumWindowsProc(IntPtr h, IntPtr l);

  public static IntPtr FindAuthDialog(uint pid) {
    IntPtr found = IntPtr.Zero;
    EnumWindows(delegate(IntPtr h, IntPtr l) {
      uint p; GetWindowThreadProcessId(h, out p);
      if (p != pid || !IsWindowVisible(h)) return true;
      var c = new StringBuilder(64); GetClassName(h, c, 64);
      if (c.ToString() == "#32770") { found = h; return false; }
      return true;
    }, IntPtr.Zero);
    return found;
  }
}
'@

$dlg = [IntPtr]::Zero
$deadline = (Get-Date).AddSeconds($TimeoutSec)
while ((Get-Date) -lt $deadline) {
  foreach ($p in @(Get-Process Radmin -ErrorAction SilentlyContinue)) {
    $h = [Win]::FindAuthDialog([uint32]$p.Id)
    if ($h -ne [IntPtr]::Zero) { $dlg = $h; break }
  }
  if ($dlg -ne [IntPtr]::Zero) { break }
  Start-Sleep -Milliseconds 400
}

if ($dlg -eq [IntPtr]::Zero) {
  throw ("No auth dialog within ${TimeoutSec}s. Usual causes: an unrecognized switch " +
         "on the command line (Viewer fails silently and keeps its main window hidden), " +
         "or a previous connection still holding the process.")
}
Write-Verbose ('Auth dialog: 0x' + $dlg.ToString('X'))

# --- 4. Fill credentials and submit ---------------------------------------
# Control IDs: 2047 username, 2048 password, 120 OK, 2 Cancel
$WM_SETTEXT = 0x000C
$BM_CLICK   = 0x00F5
$ID_USER = 2047; $ID_PASS = 2048; $ID_OK = 120

$userBox = [Win]::GetDlgItem($dlg, $ID_USER)
$passBox = [Win]::GetDlgItem($dlg, $ID_PASS)
$okBtn   = [Win]::GetDlgItem($dlg, $ID_OK)
if ($userBox -eq [IntPtr]::Zero -or $passBox -eq [IntPtr]::Zero -or $okBtn -eq [IntPtr]::Zero) {
  throw "Dialog controls incomplete (user/pass/OK). Control IDs may not match this Radmin version."
}

[void][Win]::SetForegroundWindow($dlg)
$plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
           [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
[Win]::SendMessage($userBox, $WM_SETTEXT, [IntPtr]::Zero, $User) | Out-Null
[Win]::SendMessage($passBox, $WM_SETTEXT, [IntPtr]::Zero, $plain) | Out-Null
$plain = $null
Start-Sleep -Milliseconds 300
[void][Win]::SendMessage($okBtn, $BM_CLICK, [IntPtr]::Zero, [IntPtr]::Zero)
Write-Verbose 'Credentials submitted'

# --- 5. Verify -------------------------------------------------------------
# Judge by TCP Established. The window title is localized, so it is not the criterion.
Start-Sleep -Seconds 5
$conn = Get-NetTCPConnection -RemoteAddress $Address -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq 'Established' -and $_.OwningProcess -ne 0 }

if (-not $conn) {
  Write-Warning ("Authentication appears rejected (no Established connection -- usually a bad " +
                 "password, or the account lacks $Mode permission on the server). The Radmin " +
                 "process is left open so you can retry by hand.")
  [pscustomobject]@{ Connected = $false; Address = $Address; Mode = $Mode; Pid = $null }
  return
}

$title = (Get-Process -Id $conn[0].OwningProcess -ErrorAction SilentlyContinue).MainWindowTitle
Write-Verbose "Connected. Window: $title"
[pscustomobject]@{
  Connected = $true
  Address   = $Address
  Port      = $Port
  Mode      = $Mode
  Pid       = $conn[0].OwningProcess
  Window    = $title
}
