# resume-tailor

A local, private resume tailoring pipeline. Paste a job description, get a tailored resume as `.docx` and `.pdf`. No cloud APIs, no data leaving your machine.

## How it works

Two scripts, two steps:

`resume_tailor.py` — two-pass LLM pipeline using a local Ollama model. Pass 1 extracts signals from the JD (role, core pillars, required skills, key verbs). Pass 2 rewrites each resume entry individually as structured JSON, validated for hallucinated tools before accepting.

`resume_render.py` — parses the tailored markdown, fills it into your `.docx` template preserving your fonts, colors, and styles, then exports to PDF via LibreOffice.

## Project structure

```
resume-tailor/
├── base/
│   ├── base_resume.md        # your base resume in structured markdown
│   ├── resume_template.docx  # your formatting template
│   └── tailored.md           # intermediate output (gitignored)
├── jd/                       # job description text files
├── finalresume/              # rendered .docx and .pdf outputs (gitignored)
├── runbook/
│   └── runbook.md            # copy-paste commands
├── resume_tailor.py
├── resume_render.py
├── requirements.txt
└── .gitignore
```

## Requirements

Python 3.11+ and [Ollama](https://ollama.com) running locally.

```bash
pip install -r requirements.txt
```

For PDF export, LibreOffice must be installed and `soffice` in PATH:

```bash
# macOS
brew install --cask libreoffice
sudo ln -s /Applications/LibreOffice.app/Contents/MacOS/soffice /usr/local/bin/soffice

# Ubuntu/Debian
sudo apt install libreoffice
```

Pull a model:

```bash
ollama pull qwen3:8b
```

## Usage

### Step 1 — Tailor

```bash
python resume_tailor.py \
    --jd jd/<jdfile>.txt \
    --resume base/base_resume.md \
    --output base/tailored.md
```

Check `base/tailored.md` before rendering. If the output looks off, re-run — model output varies slightly each run.

### Step 2 — Render

```bash
python resume_render.py \
    --input base/tailored.md \
    --template base/resume_template.docx \
    --format both \
    --output finalresume/<company>_resume
```

Output: `finalresume/<company>_resume.docx` and `finalresume/<company>_resume.pdf`.

### Shell function (zsh)

Add to `~/.zshrc` for a one-liner:

```zsh
tailor() {
    local jd=$1
    local company=$(basename "$jd" .txt)
    python ~/path/to/resume-tailor/resume_tailor.py \
        --jd ~/path/to/resume-tailor/jd/"$jd" \
        --resume ~/path/to/resume-tailor/base/base_resume.md \
        --output /tmp/tailored.md && \
    python ~/path/to/resume-tailor/resume_render.py \
        --input /tmp/tailored.md \
        --template ~/path/to/resume-tailor/base/resume_template.docx \
        --format both \
        --output ~/path/to/resume-tailor/finalresume/"${company}_resume"
}
```

Then: `tailor stripe_jd.txt`

## Base resume format

`base_resume.md` must follow this structure for the parser to work:

```markdown
# Your Name
email | linkedin.com/in/you | github.com/you | phone | city

## Summary

One paragraph summary.

## Skills

**Category:** tool1, tool2, tool3

## Experience

### Job Title · Company
*Start – End · Location*

- Bullet point one
- Bullet point two

## Projects / Open Source Engineering

### Project Name
*Date*

- What you built and why it matters

## Education

### Degree · University
*Year*

- Certifications, GPA
```

Key rules: `# Name` at top, contact line with `|` separators, `##` for sections, `###` for entries, `*italic*` for date/meta, `- ` for bullets. URLs and emails in the contact line are auto-detected and rendered as clickable links in the output.

## Options

```
resume_tailor.py
  --jd PATH          job description file (or - for stdin)
  --resume PATH      base resume markdown (default: base/base_resume.md)
  --model NAME       Ollama model (default: qwen3:8b)
  --output PATH      save tailored markdown to file
  --section NAME     rewrite only one section: experience, skills, summary, projects, education
  --dry-run          run pass 1 only, print JD signals and exit

resume_render.py
  --input PATH       tailored markdown (or - for stdin)
  --template PATH    .docx template file
  --format           docx | pdf | both (default: docx)
  --output PATH      output file stem (no extension)
```

## Troubleshooting

Ollama already running error on `ollama serve`: it's already up, ignore it.

Step 1 hangs or times out: `pkill ollama && ollama serve`, then retry.

`could not connect to Ollama`: Ollama isn't running. Run `ollama serve` in a separate terminal.

`Warning: could not parse any structure`: the model output didn't follow the expected markdown format. Check `base/tailored.md` — look for missing `# Name`, `##` section headers, or code fences wrapping the output. The script strips code fences automatically but the name/contact line must be present.

LibreOffice not found on macOS: `soffice` isn't in PATH. Run the symlink command above.