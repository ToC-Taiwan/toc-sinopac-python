# DEBUG

## Launch json and Tasks json

```bash
mkdir -p .vscode
echo '{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "SJ_LOG_PATH": "${workspaceFolder}/logs/shioaji.log",
                "SJ_CONTRACTS_PATH": "${workspaceFolder}/data",
                "PYTHONPATH": "${workspaceFolder}/src/pb"
            },
            "envFile": "${workspaceFolder}/.env",
            "python": "${command:python.interpreterPath}",
            "pythonArgs": [
                "-BO"
            ],
            "preLaunchTask": "Check venv",
            "internalConsoleOptions": "neverOpen"
        }
    ]
}
' > .vscode/launch.json

echo '{
    "version": "2.0.0",
    "cwd": "${workspaceFolder}",
    "type": "shell",
    "presentation": {
        "close": true
    },
    "tasks": [
        {
            "label": "Check venv",
            "command": "",
            "args": [
                "source",
                "venv/bin/activate;",
            ],
        },
    ]
}
' > .vscode/tasks.json
```
