# DEPI Data Engineering Assignments

A lightweight, reusable environment for data engineering coursework.
Works online (Google Colab, GitHub Codespaces) or locally with minimal setup.

---

## Recommended Online Setup (Zero-Install)

| Option | How to open |
|--------|------------|
| **Google Colab** | Upload any `.ipynb` notebook to [colab.research.google.com](https://colab.research.google.com) |
| **GitHub Codespaces** | Click **Code → Codespaces → Create codespace on this branch** |
| **Binder** | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Ali-Hegazy-Ai/depi_assignments/HEAD) |

All three options install dependencies automatically on first launch.
Your work is saved in your Google Drive (Colab) or the Codespace (VS Code).

---

## Local Setup (One-Time)

```bash
# 1. Clone the repo
git clone https://github.com/Ali-Hegazy-Ai/depi_assignments.git
cd depi_assignments

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Launch Jupyter Notebook
jupyter notebook
```

### Docker (optional – keeps everything self-contained)

```bash
cd docker
docker compose up --build          # first run installs dependencies
docker compose up                  # subsequent runs use the cached image
```

Open `http://localhost:8888` in your browser.

---

## Folder Structure

```
depi_assignments/
├── requirements.txt            # Python dependencies (pip install -r requirements.txt)
├── .gitignore
│
├── templates/                  # Reusable starting points
│   ├── notebook_template.ipynb # Jupyter notebook template
│   ├── etl_script_template.py  # Stand-alone ETL script template
│   └── report_template.py      # Plain-text report generator
│
├── utils/                      # Shared utility modules
│   ├── extractor.py            # Extract from CSV, JSON, API, HTML, SQLite
│   ├── transformer.py          # Clean, transform, derive columns
│   └── loader.py               # Save to CSV, JSON, SQLite; print summaries
│
├── assignments/                # One sub-folder per assignment
│   └── assignment_01/
│       ├── README.md           # Task description & submission checklist
│       ├── solution.ipynb      # Worked example notebook
│       └── data/               # Assignment-specific raw data (git-ignored)
│
├── data/                       # Shared data store (contents git-ignored)
│   ├── raw/                    # Original source files
│   ├── processed/              # Intermediate cleaned files
│   └── output/                 # Final results
│
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Core language |
| **pandas** | Data wrangling |
| **requests** | HTTP / API calls |
| **beautifulsoup4** | HTML parsing |
| **SQLAlchemy** | SQL support |
| **Jupyter Notebook** | Interactive notebooks |
| **Docker** *(optional)* | Reproducible environment |

---

## ETL Pipeline at a Glance

```
Source  →  Extract  →  Clean  →  Transform  →  Validate  →  Load
(CSV / API / SQL / HTML)                                  (CSV / SQLite)
```

All steps have ready-made helpers in the `utils/` package.

### Quick example (Python script)

```python
from utils.extractor   import from_api
from utils.transformer import normalize_columns, drop_duplicates_and_nulls
from utils.loader      import to_csv

df = from_api('https://jsonplaceholder.typicode.com/posts')
df = normalize_columns(df)
df = drop_duplicates_and_nulls(df)
to_csv(df, 'data/output/posts.csv')
```

### Quick example (notebook)

Copy `templates/notebook_template.ipynb` into your assignment folder and
fill in the **TODO** cells.

---

## Starting a New Assignment

```bash
# Copy the template notebook into a new assignment folder
cp -r templates/notebook_template.ipynb assignments/assignment_02/solution.ipynb
```

Then open `solution.ipynb` and follow the numbered sections:
0. Setup → 1. Extract → 2. Explore → 3. Clean & Transform → 4. Validate → 5. Load → 6. Findings

---

## Assignment 01 – Worked Example

See [`assignments/assignment_01/`](assignments/assignment_01/) for a complete
end-to-end example that:

1. Fetches 100 posts from the JSONPlaceholder REST API
2. Cleans column names and strips whitespace
3. Derives a `body_length` column
4. Validates required columns and uniqueness
5. Saves the result to `data/output/assignment_01_posts.csv`

---

## Optimisation Tips

* **Low bandwidth:** all libraries install once into your virtual environment
  or Docker image layer — subsequent runs need no downloads.
* **Google Colab:** mount your Google Drive (`drive.mount('/content/drive')`)
  so notebooks and output files persist between sessions.
* **Reuse across assignments:** the `utils/` package is shared by every
  assignment notebook — update helpers once and all notebooks benefit.
