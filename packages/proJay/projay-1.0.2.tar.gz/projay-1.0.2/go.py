import sys, subprocess, pathlib
from pathlib import Path

GITHUB_WORKFLOWS = {
    "ci.yml": """name: CI

on: 
  push:
    branches: [ main ]
    paths-ignore:
      - '*.md'
      - 'LICENSE'
      - '.gitignore'
  pull_request:
    branches: [ main ]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
      fail-fast: false

    runs-on: ${{ matrix.os }}
    name: Python ${{ matrix.python-version }} on ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Clean build artifacts
        run: python -c "import shutil; import os; [shutil.rmtree(p) for p in ['build', 'dist', *[d for d in os.listdir('.') if d.endswith('.egg-info')]] if os.path.exists(p)]"
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -c "import os; os.path.exists('requirements.txt') and __import__('subprocess').run(['pip', 'install', '-r', 'requirements.txt'])"
          
      - name: Quality checks
        run: |
          python -c "import os, sys; main_exists = os.path.exists('main.py'); sys.exit(0 if not main_exists else 0 if os.path.getsize('main.py') < 1024 and 'def main' in open('main.py').read() else 1)"
""",

    "release.yml": """name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    environment: github-actions
    permissions:
      contents: write
      id-token: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Validate tag version
        run: |
          TAG=${GITHUB_REF#refs/tags/v}
          grep "version=\\"$TAG\\"" setup.py || (echo "Version mismatch between tag and setup.py" && exit 1)
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build
      
      - name: Verify clean directory
        run: |
          if [ -d "dist" ] || [ -d "build" ] || [ -d "*.egg-info" ]; then
            echo "Build directories should not exist"
            exit 1
          fi
      
      - name: Build package
        run: python -m build
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/*
          generate_release_notes: true
          draft: false
          prerelease: false
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          verbose: true""",

    "dependabot.yml": """version: 2
updates:
  - package-ecosystem: pip
    directory: "/"
    schedule:
      interval: daily
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "pip"
    reviewers:
      - "$GITHUB_USERNAME"
    groups:
      python-packages:
        patterns: ["*"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    commit-message:
      prefix: "chore"
      include: "scope"
    labels:
      - "ci"
      - "dependencies"
    reviewers:
      - "$GITHUB_USERNAME"
    groups:
      github-actions:
        patterns: ["*"]
    ignore:
      - dependency-name: "actions/*"
        update-types: ["version-update:semver-patch"]""",

    "settings.yml": """repository:
  name: $PROJECT_NAME
  description: Generated with proJay
  private: false
  has_issues: true
  has_projects: false
  has_wiki: false
  has_downloads: true
  default_branch: main
  allow_squash_merge: true
  allow_merge_commit: false
  allow_rebase_merge: true
  delete_branch_on_merge: true

branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
      required_status_checks:
        strict: true
        contexts: ["test (ubuntu-latest, 3.12)"]
      enforce_admins: false
      restrictions: null""",

    "bug_report.yml": """name: Bug Report
description: Report a bug
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: "Report a bug in $PROJECT_NAME"
  - type: input
    id: version
    attributes:
      label: Version
      description: Project version
    validations:
      required: true
  - type: dropdown
    id: python-version
    attributes:
      label: Python Version
      options:
        - "3.8"
        - "3.9"
        - "3.10"
        - "3.11"
        - "3.12"
        - "3.13"
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: example
    attributes:
      label: Example Code
      description: Minimal example to reproduce
      render: python""",

    "pull_request_template.md": """## Description
<!-- Describe your changes -->

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Other

## Checklist
- [ ] Code is <1KB
- [ ] No new dependencies added
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Commit messages follow convention

## Test Results
```python
# Add test output here
```""",
}

def main():
    # Get project name and git init preference
    args = sys.argv[1:]
    project_name = args[0] if args else input("Enter the project name: ").strip()
    init_git = '--init-git' in args if args else input("Initialize a Git repository? (y/N): ").lower().startswith('y')

    # Create project directory
    project_path = Path(project_name)
    project_path.mkdir(parents=True, exist_ok=True)

    # Determine OS and script name
    is_windows = sys.platform.startswith('win')
    script_name = 'go.ps1' if is_windows else 'go.sh'

    # Define core files
    files = {
        "main.py": '''def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''',
        script_name: (
            r'.\venv\Scripts\activate; python -m pip install --upgrade pip; '
            r'if(Test-Path requirements.txt){pip install -r requirements.txt}else{Write-Host "requirements.txt not found. No dependencies installed."}; '
            r'python .\main.py' if is_windows else
            '#!/bin/bash\nsource venv/bin/activate\npip install --upgrade pip\n'
            'if [ -f requirements.txt ]; then\n    pip install -r requirements.txt\nelse\n    echo "requirements.txt not found. No dependencies installed."\nfi\n'
            'python main.py\n'
        ),
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
env/
.env/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db""",
        "setup.py": f'''from setuptools import setup
setup(
    name="{project_name}",
    version="0.1.0",
    py_modules=["{project_name}"],
    description="Generated with proJay",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",        
    author="",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)''',
        "README.md": f"""# {project_name}

## Quick Start
1. Clone this repository
2. Run `{script_name}` to setup environment and dependencies
3. Execute `python main.py`

## Development
1. Activate virtual environment:
   - Windows: `venv\\Scripts\\activate`
   - Unix: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
""",
        "requirements.txt": "",
        "LICENSE": '''MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''
    }

    # Create project files
    for filename, content in files.items():
        file_path = project_path / filename
        file_path.write_text(content)
        if filename == 'go.sh':
            file_path.chmod(0o755)

    # Create GitHub structure
    github_dir = project_path / ".github"
    workflows_dir = github_dir / "workflows"
    issue_template_dir = github_dir / "ISSUE_TEMPLATE"
    
    # Create all necessary directories
    for dir_path in [workflows_dir, issue_template_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Write GitHub files
    for filename, content in GITHUB_WORKFLOWS.items():
        # Replace placeholders
        content = content.replace("$PROJECT_NAME", project_name)
        content = content.replace("$GITHUB_USERNAME", "OWNER")

        if filename == "dependabot.yml":
            (github_dir / filename).write_text(content)
        elif filename == "settings.yml":
            (github_dir / filename).write_text(content)
        elif filename == "bug_report.yml":
            (issue_template_dir / filename).write_text(content)
        elif filename == "pull_request_template.md":
            (github_dir / filename).write_text(content)
        else:
            (workflows_dir / filename).write_text(content)

    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=project_path)

    # Initialize git if requested
    if init_git:
        subprocess.run(["git", "init"], cwd=project_path)
        subprocess.run(["git", "add", "."], cwd=project_path)
        subprocess.run(["git", "commit", "-m", "🚀 Initial commit"], cwd=project_path)

    print(f"""
✨ Project '{project_name}' created successfully!

Next steps:
1. Add your dependencies to 'requirements.txt'
2. Run '{script_name}' to setup the environment
3. Start coding in main.py

To publish to PyPI:
1. Update version in setup.py
2. git tag v0.1.0
3. git push origin v0.1.0
""")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()