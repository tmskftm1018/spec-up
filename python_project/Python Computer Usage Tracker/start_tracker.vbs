Set objShell = CreateObject("WScript.Shell")

Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

command = "cmd /k py """ & scriptPath & "\Python_Computer_Usage_Tracker.py"""

objShell.Run command, 0, False