#NoEnv
SendMode Input
SetTitleMatchMode, 2
SetTitleMatchMode, slow

; Set the title of the game window here
gameTitle := "StarCraft II"

; Delay between each injection cycle (in milliseconds)
injectionDelay := 32000 ; 32 seconds

; Flag to control the script
scriptRunning := false
autoInjectionStarted := false

; Conversion factor from centimeters to pixels (approximately)
cmToPx := 38

; Hotkey to start/stop the script
F11::
scriptRunning := !scriptRunning
if (scriptRunning) {
    autoInjectionStarted := false ; Reset the flag when script starts
} else {
    SetTimer, InjectQueens, Off
}
return

; Injection routine
InjectQueens:
if WinActive(gameTitle) {
    MouseGetPos, startX, startY
    MouseMove, 1280, 540
    Send,{tab}{4}{v}{Backspace}
    sleep -1
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    ControlSend, , {v}, StarCraft II,
    Send , {Click}{Backspace}
    MouseMove, startX, startY
}
return

; Single injection routine for manual Alt keypress
SingleInjectQueens:
if WinActive(gameTitle) {
    MouseGetPos, startX, startY
    Send,{6}{v}{Backspace}
    Click, 1280, 540
    ControlSend, , {v}{Click, 1280, 540}{Backspace}, StarCraft II,
    ControlSend, , {v}{Click, 1280, 540}{Backspace}, StarCraft II,
    ControlSend, , {v}{Click, 1280, 540}{Backspace}, StarCraft II,
    ControlSend, , {v}{Click, 1280, 540}{Backspace}, StarCraft II,
    MouseMove, startX, startY
}
return

; ALT key press handler
$Alt::
if (scriptRunning) {
    ; Run single injection routine
    Gosub, SingleInjectQueens

    ; Start the automatic injection after the first manual injection
    if (!autoInjectionStarted) {
        autoInjectionStarted := true
        SetTimer, InjectQueens, %injectionDelay%
    }
}
return

CapsLock::
    ControlSend, , {5}{s}{d}, StarCraft II,
return

; Function to check if window is active
WinActive(title) {
    WinGet, active_id, ID, A
    WinGetTitle, active_title, ahk_id %active_id%
    return InStr(active_title, title)
}
