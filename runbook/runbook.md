# Resume Tailor Runbook

## Step 1 — Tailor

python resume_tailor.py \
    --jd jd/<jdfile> \
    --resume base/<basefile> \
    --output base/tailored.md

## Step 2 — Render

python resume_render.py \
    --input base/tailored.md \
    --template base/resume_template.docx \
    --format both \
    --output finalresume/<company>_resume

## Notes

- Default model: qwen3:8b (set in resume_tailor.py, override with --model)
- Ollama must be running: ollama serve
- If Step 1 hangs: pkill ollama && ollama serve
- Output lands in finalresume/ as both .docx and .pdf
- Check base/tailored.md before rendering if output looks off