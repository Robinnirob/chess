# Chess for Nicolas

## Getting started

* Install python 3.11
    * Add python in PATH
* In a powershell as administrator

```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

* In a powershell with the user profile  (pyenv installation)

```
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

* In a powershell as administrator
```
Set-ExecutionPolicy -ExecutionPolicy Undefined
```

## Dev

* Execute the following actions :

```
poetry self add poetry-pyinstaller-plugin
python -m ensurepip --upgrade
echo "Add pip3 directory path in PATH (as explained in the comments)"
pip3 install poetry
poetry install
python main.py
```

## Create .exe File

```
poetry build
```
