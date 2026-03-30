Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "python C:\IA_AUTOMACAO\MOTOR\orquestrador.py", 0
WshShell.Run "python C:\IA_AUTOMACAO\WEB\servidor.py", 0

Set WshShell = Nothing