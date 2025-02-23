# proJay

<div align="center">

[![PyPI version](https://badge.fury.io/py/proJay.svg)](https://badge.fury.io/py/proJay)
[![CI](https://github.com/FeelTheFonk/proJay/workflows/CI/badge.svg)](https://github.com/FeelTheFonk/proJay/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# ![TheMatrixReloadedNeoGIF](https://github.com/user-attachments/assets/4df80063-238e-4ce2-9468-13a55bb323f8)

A lightning-fast Python project generator with perfect GitHub workflows. Zero config, instant setup.

</div>

## 🕶 Features

- **Ultra-Minimal**: Single file, zero dependencies
- **Instant Setup**: One command to rule them all
- **Perfect Structure**: Production-ready in seconds
- **GitHub Power**: CI/CD, Release automation, Branch protection
- **PyPI Ready**: Configured for instant publishing
- **Cross-Platform**: Windows & Unix support with dedicated scripts

## 💊 Quick Start

```bash
python -m go your_project_name

# or

python -m go your_project_name --init-git
```

## 🔴 Generated Structure

```
your_project/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.yml     # Bug report template
│   ├── workflows/
│   │   ├── ci.yml            # Multi-OS CI pipeline
│   │   └── release.yml       # Automated PyPI releases
│   ├── dependabot.yml        # Daily updates
│   ├── pull_request_template.md  # PR template
│   └── settings.yml          # Branch protection
├── main.py                   # Entry point
├── setup.py                  # PyPI configuration
├── requirements.txt          # Dependencies
├── go.ps1/go.sh             # Setup scripts
├── LICENSE                   # MIT License
├── README.md                # Documentation
└── .gitignore               # Clean workspace
```

## 🌐 Scripts & Automation

- **Setup Scripts**
  - Windows: `go.ps1`
  - Unix: `go.sh`
  - Automatic venv creation
  - Dependencies installation
  - Environment activation

- **CI Pipeline**
  - Multi-OS testing (Windows, Linux, MacOS)
  - Python 3.8 to 3.13 support
  - Dependencies verification
  - Quality checks
  - Clean build verification

- **DependaBot**
  - Daily pip updates
  - GitHub Actions updates
  - Automated PRs with labels
  - Review assignments
  - Grouped updates

- **Release Pipeline**
  - Version validation
  - Package size checks
  - PyPI publishing
  - GitHub release creation
  - Release notes generation

## 📂 Project Usage

```bash
# Generate project
python proJay.py my_project --init-git

# Setup environment
cd my_project
# On Windows
.\go.ps1
# On Unix
./go.sh

# Add remote & push
git remote add origin https://github.com/username/my_project
git push -u origin main

# Create release
git tag v0.1.0
git push origin v0.1.0
```

## ⚡ Development

1. Clone your generated project
2. Run the setup script (`go.ps1` or `go.sh`)
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start coding in `main.py`

## 🔄 Continuous Integration

Automatic checks on every push:
- Cross-platform compatibility
- Python version compatibility
- Code quality
- Build verification
- Size limits

## 🚀 Release Process

1. Update version in `setup.py`
2. Create and push tag
3. Automatic:
   - Package building
   - Version validation
   - Size verification
   - PyPI publishing
   - GitHub release

---
🔵 46 6F 6C 6C 6F 77 20 74 68 65 20 77 68 69 74 65 20 72 61 62 62 69 74 🐇
---

<div align="center">
🕶
</div>