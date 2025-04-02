@echo off

REM Create virtual environment if it doesn't exist
if not exist "env\" (
    python -m venv env
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate the environment
call env\Scripts\activate

REM Install dependencies
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo Dependencies installed from requirements.txt
) else (
    echo requirements.txt not found. Please create one.
)

REM Set default environment variables
set PYTHONPATH=%CD%
set PROJECT_ROOT=%CD%

echo Environment setup complete.