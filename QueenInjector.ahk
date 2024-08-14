#NoEnv
SendMode Input
SetTitleMatchMode, 2
SetTitleMatchMode, slow

; Initial delay between each injection cycle (in milliseconds)
injectionDelay := 32000 ; 32 seconds

; Flag to control the script
scriptRunning := false
autoInjectionStarted := false

; Create GUI
Gui, Add, Checkbox, x10 y10 w200 h30 vAutoInject gToggleAutoInject, Auto inject after delay?
Gui, Add, Text, x10 y50 w200 h20, Injection Delay (ms):
Gui, Add, Edit, x220 y50 w100 h20 vInjectionDelay Disabled, %injectionDelay%
Gui, Add, Button, x10 y80 w150 h30 gStartScript, Start
Gui, Add, Button, x170 y80 w150 h30 gStopScript, Stop
Gui, Add, Text, x10 y120 w310 h20 vStatus, Stopped
Gui, Show, x200 y200 h170 w350, StarCraft II Script

; Ensure GUI is always shown
SetTimer, EnsureGUIVisible, 1000
return

EnsureGUIVisible:
if !WinExist("StarCraft II Script") {
    Gui, Show, x200 y200 h170 w350, StarCraft II Script
}
return

; Toggle enable/disable state of the injection delay edit field
ToggleAutoInject:
Gui, Submit, NoHide
if (AutoInject) {
    GuiControl, Enable, InjectionDelay
} else {
    GuiControl, Disable, InjectionDelay
}
return

; GUI Functions
StartScript:
Gui, Submit, NoHide
if (AutoInject) {
    injectionDelay := InjectionDelay
    autoInjectionStarted := false
    SetTimer, InjectQueens, %injectionDelay%
    GuiControl,, Status, Running
} else {
    GuiControl,, Status, Ready (Alt to Inject)
}
scriptRunning := true
return

StopScript:
scriptRunning := false
SetTimer, InjectQueens, Off
autoInjectionStarted := false
GuiControl,, Status, Stopped
return

GuiClose:
ExitApp

; Hotkey to start/stop the script
F11::
scriptRunning := !scriptRunning
if (scriptRunning) {
    autoInjectionStarted := false ; Reset the flag when script starts
    if (AutoInject) {
        SetTimer, InjectQueens, %injectionDelay%
    }
    GuiControl,, Status, Running
} else {
    SetTimer, InjectQueens, Off
    GuiControl,, Status, Stopped
}
return

; Injection routine
InjectQueens:
if WinActive(gameTitle) {
    MouseGetPos, startX, startY
    MouseMove, 1280, 540
    Send , {2}
    sleep 100
    Send , {v}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 26
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    Send , {v}{Click}{Backspace}
    sleep 25
    MouseMove, startX, startY
}
return

; ALT key press handler
$Alt::
if WinActive(gameTitle) {
    MouseGetPos, startX, startY
    MouseMove, 1280, 540
    Send , {2}
    sleep 100
    Send , {Backspace}
    sleep 25
    Send , {v}{v}{Backspace}
    sleep 26
    Send , {v}{v}{Backspace}
    sleep 25
    Send , {v}{v}{Backspace}
    sleep 25
    Send , {v}{v}{Backspace}
    sleep 25
    Send , {v}{v}{Backspace}
    sleep 25
    MouseMove, startX, startY

    if (autoInjectionStarted) {
        return
    }

    if (scriptRunning) {
        autoInjectionStarted := true
        SetTimer, InjectQueens, %injectionDelay%
        GuiControl,, Status, Running
    }
}
return

CapsLock::
    ControlSend, , {5}{s}{d}, StarCraft II
    sleep 10
return

; Function to check if window is active
WinActive(title) {
    WinGet, active_id, ID, A
    WinGetTitle, active_title, ahk_id %active_id%
    return InStr(active_title, title)
}
