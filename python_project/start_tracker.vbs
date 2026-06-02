Set WshShell = CreateObject("WScript.Shell")

WshShell.Run chr(34) & _
"C:\Users\User\Desktop\Python Computer Usage Tracker\start_tracker.bat" & chr(34), 0

Set WshShell = Nothing