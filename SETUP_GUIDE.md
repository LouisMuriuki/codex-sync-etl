# VSCode Setup Guide - Medical Codex ETL Pipeline

Complete step-by-step guide to set up this project in Visual Studio Code.

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed (check with `python3 --version`)
- **Visual Studio Code** installed ([download here](https://code.visualstudio.com/))
- **Git** installed (for cloning, if applicable)
- **Internet connection** (for downloading dependencies and data files)

---

## Step 1: Install Python (if not already installed)

### macOS:
```bash
# Check if Python is installed
python3 --version

# If not installed, install via Homebrew:
brew install python3

# Or download from python.org
```

### Windows:
- Download from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## Step 2: Install Visual Studio Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install following the installer prompts
3. Launch VSCode

---

## Step 3: Install Essential VSCode Extensions

Open VSCode and install these extensions:

1. **Python** (by Microsoft) - Essential for Python development
   - Open Extensions: `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
   - Search "Python" and install the official Microsoft extension

2. **Pylance** (by Microsoft) - Python language server (usually auto-installed with Python extension)

3. **Python Indent** (optional but recommended) - Better indentation handling

**Quick install via command:**
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
```

---

## Step 4: Get the Project

### Option A: Clone from Git Repository
```bash
# Navigate to your desired directory
cd ~/Desktop/Develop/python

# Clone the repository (replace URL with your actual repo URL)
git clone <repository-url> codex-sync-etl

# Navigate into project
cd codex-sync-etl
```

### Option B: Copy/Download Project Files
1. Copy the project folder to your desired location
2. Open VSCode
3. File → Open Folder → Select the `codex-sync-etl` folder

---

## Step 5: Open Project in VSCode

1. Launch VSCode
2. **File → Open Folder** (or `Cmd+O` / `Ctrl+O`)
3. Navigate to and select the `codex-sync-etl` folder
4. Click "Open"

You should now see the project structure in the Explorer sidebar.

---

## Step 6: Create Python Virtual Environment

### In VSCode Terminal:

1. Open integrated terminal: **Terminal → New Terminal** (or `` Ctrl+` `` / `` Cmd+` ``)

2. Create virtual environment:
```bash
python3 -m venv venv
```

3. Activate virtual environment:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt.

---

## Step 7: Configure VSCode Python Interpreter

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: `Python: Select Interpreter`
3. Select the interpreter from your `venv` folder:
   - Should show: `./venv/bin/python` (Mac/Linux) or `./venv/Scripts/python.exe` (Windows)
   - If not visible, click "Enter interpreter path..." and navigate to:
     - Mac/Linux: `./venv/bin/python3`
     - Windows: `./venv/Scripts/python.exe`

**Verify:** Check bottom-right corner of VSCode - should show Python version from venv.

---

## Step 8: Install Project Dependencies

With virtual environment activated, install requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

You should see: `pandas`, `requests`, `numpy`, etc.

---

## Step 9: Configure VSCode Settings (Optional but Recommended)

Create `.vscode/settings.json` in project root:

1. Create `.vscode` folder if it doesn't exist
2. Create `settings.json` file inside `.vscode`
3. Add these settings:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "none",
    "python.analysis.typeCheckingMode": "basic",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "editor.formatOnSave": false,
    "editor.rulers": [88, 120]
}
```

---

## Step 10: Create Input Directory Structure

Ensure input directory exists (should already exist, but verify):

```bash
# Check if input directory exists
ls -la input/

# If missing, create it:
mkdir -p input
mkdir -p output/csv
mkdir -p output/errors
mkdir -p logs
```

---

## Step 11: Test the Setup

Run a simple processor to verify everything works:

```bash
# Make sure venv is activated (you should see (venv) in prompt)
python scripts/icd10cm_processor.py
```

**Expected behavior:**
- Script will attempt to download data if `ICD10CM_URL` env var is set
- Or will look for local file at `input/icd10cm_codes_2024.txt`
- Creates output files in `output/csv/`
- Creates logs in `logs/`

---

## Step 12: Configure Environment Variables (Optional)

For processors that support automatic downloads, set environment variables:

**macOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bashrc for persistence
export ICD10CM_URL="https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2024/icd10cm_codes_2024.txt"
export HCPCS_URL="https://www.cms.gov/files/zip/2024-alpha-numeric-hcpcs-file.zip"

# Or set temporarily for current session:
export ICD10CM_URL="..."
```

**Windows (PowerShell):**
```powershell
$env:ICD10CM_URL="https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2024/icd10cm_codes_2024.txt"
```

**Windows (Command Prompt):**
```cmd
set ICD10CM_URL=https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2024/icd10cm_codes_2024.txt
```

---

## Step 13: Verify Project Structure

Your project should look like this:

```
codex-sync-etl/
├── .vscode/              # VSCode settings (you created this)
│   └── settings.json
├── input/                # Raw data files go here
├── scripts/              # ETL processor scripts
│   ├── icd10cm_processor.py
│   ├── hcpcs_processor.py
│   ├── npi_processor.py
│   └── ...
├── output/
│   ├── csv/             # Clean output files
│   └── errors/          # Invalid rows
├── logs/                # Processing logs
├── utils/               # Shared utilities
├── venv/                # Virtual environment (don't commit)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Step 14: Running Processors

### Run Individual Processors:

```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Run processors
python scripts/icd10cm_processor.py
python scripts/hcpcs_processor.py
python scripts/npi_processor.py
python scripts/icd10who_processor.py
python scripts/loinc_processor.py
python scripts/rxnorm_processor.py
python scripts/snomed_processor.py
```

### Run All Processors (create a script):

Create `run_all.py` in project root:

```python
import subprocess
import sys
from pathlib import Path

scripts = [
    "scripts/icd10cm_processor.py",
    "scripts/hcpcs_processor.py",
    "scripts/npi_processor.py",
    "scripts/icd10who_processor.py",
    "scripts/loinc_processor.py",
    "scripts/rxnorm_processor.py",
    "scripts/snomed_processor.py",
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"Running {script}")
    print('='*60)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"❌ {script} failed with exit code {result.returncode}")
        sys.exit(1)
    print(f"✅ {script} completed successfully")

print("\n🎉 All processors completed!")
```

Run with: `python run_all.py`

---

## Troubleshooting

### Issue: Python interpreter not found
**Solution:**
- Ensure Python 3.9+ is installed: `python3 --version`
- Re-select interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"
- Restart VSCode

### Issue: Module not found errors
**Solution:**
- Ensure venv is activated (check for `(venv)` in terminal)
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify interpreter is set to venv Python

### Issue: Scripts fail with import errors
**Solution:**
- Ensure you're running from project root directory
- Check that `utils/` folder exists and contains `common_functions.py`
- Verify `sys.path` setup in processor scripts (should auto-add project root)

### Issue: File not found errors
**Solution:**
- Ensure input files exist in `input/` directory
- Or set appropriate environment variables for auto-download
- Check file paths in processor scripts match your file names

### Issue: VSCode terminal doesn't activate venv automatically
**Solution:**
- Check `.vscode/settings.json` has `"python.terminal.activateEnvironment": true`
- Manually activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)

### Issue: Download failures
**Solution:**
- Some data sources require registration/licenses (LOINC, RxNorm, SNOMED)
- Download files manually and place in `input/` directory
- Check network connectivity and URL validity

---

## Quick Reference Commands

```bash
# Activate virtual environment
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# Deactivate virtual environment
deactivate

# Install/update dependencies
pip install -r requirements.txt

# Run a processor
python scripts/icd10cm_processor.py

# Check Python version
python3 --version

# List installed packages
pip list

# Check project structure
ls -la                              # Mac/Linux
dir                                 # Windows
```

---

## Next Steps

1. **Add sample data files** to `input/` directory
2. **Run individual processors** to test each codex
3. **Check output files** in `output/csv/` directory
4. **Review logs** in `logs/` directory for processing details
5. **Customize processors** as needed for your use case

---

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [VSCode Python Documentation](https://code.visualstudio.com/docs/languages/python)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- Project README.md for data source information

---

## Summary Checklist

- [ ] Python 3.9+ installed
- [ ] VSCode installed
- [ ] Python extension installed in VSCode
- [ ] Project folder opened in VSCode
- [ ] Virtual environment created (`venv`)
- [ ] Python interpreter set to venv
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Input/output directories exist
- [ ] Test processor runs successfully
- [ ] Environment variables set (if using auto-download)

---

**You're all set!** 🎉

If you encounter any issues not covered here, check the logs in `logs/` directory for detailed error messages.

