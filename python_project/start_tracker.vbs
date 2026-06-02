Set objShell = CreateObject("WScript.Shell")

' 현재 vbs 파일이 있는 폴더 기준으로 경로 잡기
Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' python 실행 (환경 변수 기준으로 자동 탐색)
command = "python """ & scriptPath & "\usage_tracker.py"""

' 숨김 실행 (0 = 안 보임)
objShell.Run command, 0, False