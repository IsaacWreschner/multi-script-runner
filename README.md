# 🖥️ Multi-Tab Script Runner

Multi-Tab Script Runner is a Python + PyQt6 GUI tool that lets you launch grouped scripts via Windows Terminal tabs.

## 📁 Structure

```
.
├── script_runner.py
├── script_wrapper.py
├── scripts.json
└── example-scripts/
    ├── hello-world.ps1
    ├── hello-world.py
    └── echo.bat
```

## ▶️ Run

```bash
pip install PyQt6
python script_runner.py
```

## 🛠 Make an Executable

```bash
pip install pyinstaller
pyinstaller --onefile script_runner.py
```
