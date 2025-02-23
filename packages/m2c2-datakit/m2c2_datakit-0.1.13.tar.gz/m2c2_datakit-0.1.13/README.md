# m2c2_datakit

🚀 **A set of R, Python, and NPM packages for scoring M2C2kit Data!** 🚀

---

Developers: 
- [Dr. Nelson Roque](https://www.linkedin.com/in/nelsonroque/) | ORCID: https://orcid.org/0000-0003-1184-202X
- [Dr. Scott Yabiku](https://www.linkedin.com/in/scottyabiku) | ORCID: https://orcid.org/0000-0003-1184-202X

---

## Changelog

[Source: https://github.com/nelsonroque/m2c2kit-data](https://github.com/nelsonroque/m2c2kit-data)

See [CHANGELOG.md](CHANGELOG.md)

--- 

## Features

### Current Features

  1) Load a JSON file of a query export from MongoDB
  2) Load a folder of JSON files, one folder per participant, with subfolders for sessions, from Metricwire
  3) Interoperable Data exports (csv, tsv, pkl)

### Feature Roadmap
  1) In General: Feature and Data parity from R, Python, and NPM scoring tools (same data + different tool = same scores)
  2) CLI in Python for simplifying scoring with one-liners (e.g., m2data --score --summarise --file data.json)
  3) Load a folder of JSON files, one folder per participant, with subfolders for sessions, from REDCAP (Coming Soon)
  4) Load a file export, containing columns for each trial, for each task, from Qualtrics (Coming Soon)

--- 

## **🚀 Getting Started**

### **Installation for Scoring Developers**
  - Python
  - [Visual Studio Code](https://code.visualstudio.com/) with Jupyter Notebook Extension or [Jupyter Lab](https://jupyter.org/install) (or [Anaconda](https://www.anaconda.com/))
  - `uv venv`

```{}
# 1. Create the virtual environment
uv venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\Activate    # Windows (PowerShell)

# 3. Install dependencies
uv pip install -e .

# 4. Run formatting, linting, and type checking
make install

```

### **Installation for End Users**
  - `pip install m2c2_datakit`
  - `pip3 install m2c2_datakit`

---

## **💡 Contributions Welcome!**

📌 Have ideas? Found a bug? Want to improve the package?  [Open an issue!](https://github.com/nelsonroque/tidypollute/issues).

📜 **[Code of Conduct](https://docs.github.com/en/site-policy/github-terms/github-community-code-of-conduct) - Please be respectful and follow community guidelines.**

---

## Acknowledgements
The development of `m2c2kit-data` (tentative name) was made possible with support from NIA (XXXXXXXXXXXXX).

---

🌎 **More Resources:**  
📌 [M2C2 Official Website](https://m2c2.io)
📌 [M2C2kit Official Documentation Website](https://m2c2-project.github.io/m2c2kit-docs/)
📌 [Pushing to PyPI](https://docs.astral.sh/uv/guides/publish/#publishing-your-package)
  - https://docs.astral.sh/uv/guides/integration/github/#setting-up-python
[What is JSON?](https://www.w3schools.com/whatis/whatis_json.asp)

---

🚀 Let's go study some brains!