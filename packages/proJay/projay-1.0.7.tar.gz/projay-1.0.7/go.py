_D='pull_request_template.md'
_C='bug_report.yml'
_B='settings.yml'
_A='dependabot.yml'
import sys,subprocess,pathlib
from pathlib import Path
GITHUB_WORKFLOWS={'ci.yml':'name: CI\n\non: \n  push:\n    branches: [ main ]\n    paths-ignore:\n      - \'*.md\'\n      - \'LICENSE\'\n      - \'.gitignore\'\n  pull_request:\n    branches: [ main ]\n\njobs:\n  test:\n    strategy:\n      matrix:\n        os: [ubuntu-latest, windows-latest, macos-latest]\n        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]\n      fail-fast: false\n\n    runs-on: ${{ matrix.os }}\n    name: Python ${{ matrix.python-version }} on ${{ matrix.os }}\n\n    steps:\n      - uses: actions/checkout@v4\n      \n      - name: Set up Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: ${{ matrix.python-version }}\n          \n      - name: Clean build artifacts\n        run: python -c "import shutil; import os; [shutil.rmtree(p) for p in [\'build\', \'dist\', *[d for d in os.listdir(\'.\') if d.endswith(\'.egg-info\')]] if os.path.exists(p)]"\n          \n      - name: Install dependencies\n        run: |\n          python -m pip install --upgrade pip\n          python -c "import os; os.path.exists(\'requirements.txt\') and __import__(\'subprocess\').run([\'pip\', \'install\', \'-r\', \'requirements.txt\'])"\n          \n      - name: Quality checks\n        run: |\n          python -c "import os, sys; main_exists = os.path.exists(\'main.py\'); sys.exit(0 if not main_exists else 0 if os.path.getsize(\'main.py\') < 1024 and \'def main\' in open(\'main.py\').read() else 1)"\n','release.yml':'name: Release\n\non:\n  push:\n    tags:\n      - \'v*.*.*\'\n\njobs:\n  release:\n    runs-on: ubuntu-latest\n    environment: github-actions\n    permissions:\n      contents: write\n      id-token: write\n\n    steps:\n      - uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n      \n      - name: Validate tag version\n        run: |\n          TAG=${GITHUB_REF#refs/tags/v}\n          grep "version="${TAG}"" setup.py || (echo "Version mismatch between tag and setup.py" && exit 1)\n      \n      - name: Set up Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: "3.12"\n      \n      - name: Install build tools and minifier\n        run: |\n          python -m pip install --upgrade pip\n          pip install build python-minifier\n      \n      - name: Minify Python source code\n        run: |\n          # Exemple : minifier le fichier main.py\n          if [ -f "main.py" ]; then\n            echo "Minification de main.py..."\n            python -m python_minifier main.py > main.min.py && mv main.min.py main.py\n          else\n            echo "main.py non trouvé, minification ignorée."\n          fi\n      \n      - name: Verify clean directory\n        run: |\n          if [ -d "dist" ] || [ -d "build" ] || ls *.egg-info 1> /dev/null 2>&1; then\n            echo "Build directories should not exist"\n            exit 1\n          fi\n      \n      - name: Build package\n        run: python -m build\n      \n      - name: Create GitHub Release\n        uses: softprops/action-gh-release@v2\n        with:\n          files: dist/*\n          generate_release_notes: true\n          draft: false\n          prerelease: false\n      \n      - name: Publish to PyPI\n        uses: pypa/gh-action-pypi-publish@release/v1\n        with:\n          verbose: true\n',_A:'version: 2\nupdates:\n  - package-ecosystem: pip\n    directory: "/"\n    schedule:\n      interval: daily\n    commit-message:\n      prefix: "deps"\n      include: "scope"\n    labels:\n      - "dependencies"\n      - "pip"\n    reviewers:\n      - "$GITHUB_USERNAME"\n    groups:\n      python-packages:\n        patterns: ["*"]\n\n  - package-ecosystem: "github-actions"\n    directory: "/"\n    schedule:\n      interval: "daily"\n    commit-message:\n      prefix: "chore"\n      include: "scope"\n    labels:\n      - "ci"\n      - "dependencies"\n    reviewers:\n      - "$GITHUB_USERNAME"\n    groups:\n      github-actions:\n        patterns: ["*"]\n    ignore:\n      - dependency-name: "actions/*"\n        update-types: ["version-update:semver-patch"]',_B:'repository:\n  name: $PROJECT_NAME\n  description: Generated with proJay\n  private: false\n  has_issues: true\n  has_projects: false\n  has_wiki: false\n  has_downloads: true\n  default_branch: main\n  allow_squash_merge: true\n  allow_merge_commit: false\n  allow_rebase_merge: true\n  delete_branch_on_merge: true\n\nbranches:\n  - name: main\n    protection:\n      required_pull_request_reviews:\n        required_approving_review_count: 1\n        dismiss_stale_reviews: true\n      required_status_checks:\n        strict: true\n        contexts: ["test (ubuntu-latest, 3.12)"]\n      enforce_admins: false\n      restrictions: null',_C:'name: Bug Report\ndescription: Report a bug\nlabels: ["bug"]\nbody:\n  - type: markdown\n    attributes:\n      value: "Report a bug in $PROJECT_NAME"\n  - type: input\n    id: version\n    attributes:\n      label: Version\n      description: Project version\n    validations:\n      required: true\n  - type: dropdown\n    id: python-version\n    attributes:\n      label: Python Version\n      options:\n        - "3.8"\n        - "3.9"\n        - "3.10"\n        - "3.11"\n        - "3.12"\n        - "3.13"\n  - type: textarea\n    id: description\n    attributes:\n      label: Description\n      description: What happened?\n    validations:\n      required: true\n  - type: textarea\n    id: example\n    attributes:\n      label: Example Code\n      description: Minimal example to reproduce\n      render: python',_D:'## Description\n<!-- Describe your changes -->\n\n## Type of change\n- [ ] Bug fix\n- [ ] New feature\n- [ ] Documentation\n- [ ] Other\n\n## Checklist\n- [ ] Code is <1KB\n- [ ] No new dependencies added\n- [ ] Tests pass\n- [ ] Documentation updated\n- [ ] Commit messages follow convention\n\n## Test Results\n```python\n# Add test output here\n```'}
def main():
	O='venv';N='go.sh';I='git';G=True;F=sys.argv[1:];D=F[0]if F else input('Enter the project name: ').strip();P='--init-git'in F if F else input('Initialize a Git repository? (y/N): ').lower().startswith('y');C=Path(D);C.mkdir(parents=G,exist_ok=G);J=sys.platform.startswith('win');H='go.ps1'if J else N;Q={'main.py':'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n',H:'.\\venv\\Scripts\\activate; python -m pip install --upgrade pip; if(Test-Path requirements.txt){pip install -r requirements.txt}else{Write-Host "requirements.txt not found. No dependencies installed."}; python .\\main.py'if J else'#!/bin/bash\nsource venv/bin/activate\npip install --upgrade pip\nif [ -f requirements.txt ]; then\n    pip install -r requirements.txt\nelse\n    echo "requirements.txt not found. No dependencies installed."\nfi\npython main.py\n','.gitignore':'# Python\n__pycache__/\n*.py[cod]\n*$py.class\n\n# Distribution / packaging\ndist/\nbuild/\n*.egg-info/\n\n# Virtual environments\nvenv/\nenv/\n.env/\n.venv/\n\n# IDE\n.idea/\n.vscode/\n*.swp\n*.swo\n\n# OS\n.DS_Store\nThumbs.db','setup.py':f'''from setuptools import setup
setup(
    name="{D}",
    version="0.1.0",
    py_modules=["{D}"],
    description="Generated with proJay",
    long_description=open(\'README.md\').read(),
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
)''','README.md':f"""# {D}

## Quick Start
1. Clone this repository
2. Run `{H}` to setup environment and dependencies
3. Execute `python main.py`

## Development
1. Activate virtual environment:
   - Windows: `venv\\Scripts\\activate`
   - Unix: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
""",'requirements.txt':'','LICENSE':'MIT License\n\nCopyright (c) 2024\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.'}
	for(A,B)in Q.items():
		K=C/A;K.write_text(B)
		if A==N:K.chmod(493)
	E=C/'.github';L=E/'workflows';M=E/'ISSUE_TEMPLATE'
	for R in[L,M]:R.mkdir(parents=G,exist_ok=G)
	for(A,B)in GITHUB_WORKFLOWS.items():
		B=B.replace('$PROJECT_NAME',D);B=B.replace('$GITHUB_USERNAME','OWNER')
		if A==_A:(E/A).write_text(B)
		elif A==_B:(E/A).write_text(B)
		elif A==_C:(M/A).write_text(B)
		elif A==_D:(E/A).write_text(B)
		else:(L/A).write_text(B)
	subprocess.run([sys.executable,'-m',O,O],cwd=C)
	if P:subprocess.run([I,'init'],cwd=C);subprocess.run([I,'add','.'],cwd=C);subprocess.run([I,'commit','-m','🚀 Initial commit'],cwd=C)
	print(f"""
✨ Project '{D}' created successfully!

Next steps:
1. Add your dependencies to 'requirements.txt'
2. Run '{H}' to setup the environment
3. Start coding in main.py

To publish to PyPI:
1. Update version in setup.py
2. git tag v0.1.0
3. git push origin v0.1.0
""");input('Press Enter to exit...')
if __name__=='__main__':main()