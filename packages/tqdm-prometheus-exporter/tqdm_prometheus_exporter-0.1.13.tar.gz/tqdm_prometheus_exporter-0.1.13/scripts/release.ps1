$ErrorActionPreference = "Stop"
Clear-Host

uv venv
.venv\Scripts\Activate.ps1

uv sync
.\scripts\run-tests.ps1

foreach ($_ in 0..15) {
    Write-Host ""
}

Write-Host "Check the test results and press any key to continue..."
pause
Clear-Host

uv pip install toml
uv pip install sermver
uv pip install gitpython

uv run python release_tool\bump.py $args