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
    ; Move mouse to position x900 y500
    MouseMove, 900, 500
    Sleep, 100 ; Short delay to ensure the mouse move is registered

    ; Select all Queens
    Send, {6}
    Sleep, 100 ; Short delay to ensure command is registered

    ; Issue the inject command sequence
    Send, {F1}{Click}
    Sleep, 100
    Send, {F3}{Click}
    Sleep, 100
    Send, {F4}{Click}
    Sleep, 100
    Send, {F5}{Click}
    Sleep, 100
}
return

; Single injection routine for manual Alt keypress
SingleInjectQueens:
if WinActive(gameTitle) {
    ; Move mouse to position x900 y500
    MouseMove, 900, 500
    Sleep, 100 ; Short delay to ensure the mouse move is registered

    ; Select all Queens
    Send, {6}
    Sleep, 100 ; Short delay to ensure command is registered

    ; Issue the inject command sequence
    Send, {F1}{Click}
    Sleep, 100
    Send, {F3}{Click}
    Sleep, 100
    Send, {F4}{Click}
    Sleep, 100
    Send, {F5}{Click}
    Sleep, 100
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

; Function to check if window is active
WinActive(title) {
    WinGet, active_id, ID, A
    WinGetTitle, active_title, ahk_id %active_id%
    return InStr(active_title, title)
}
