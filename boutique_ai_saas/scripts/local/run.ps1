$ErrorActionPreference = 'Stop'

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location -Path "..\\.."

Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver

