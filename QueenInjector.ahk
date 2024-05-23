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

; Hotkey to start/stop the script
F11::
scriptRunning := !scriptRunning
if (scriptRunning) {
    SetTimer, InjectQueens, %injectionDelay%
    ; Immediately run the injection routine for the first time
    Gosub, InjectQueens
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

; Prevent any action when ALT is pressed if the script is not running
$Alt::
if (scriptRunning) {
    ; Move mouse to position x900 y500
    MouseMove, 900, 500
    Sleep, 100 ; Short delay to ensure the mouse move is registered

    Send, {tab}{4}{v}{F1}
    Sleep, 50
    Send, {Click}{F3}
    Sleep, 50
    Send, {Click}{F4}
    Sleep, 50
    Send, {Click}{F5}
    Sleep, 50
    Send, {Click}{F6}
    Sleep, 50
}
return

; Function to check if window is active
WinActive(title) {
    WinGet, active_id, ID, A
    WinGetTitle, active_title, ahk_id %active_id%
    return InStr(active_title, title)
}
