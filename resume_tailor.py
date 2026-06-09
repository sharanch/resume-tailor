#!/usr/bin/env python3
"""
resume_tailor.py - Tailor resume bullet points to a job description using a local Ollama model.

Two-pass approach:
  Pass 1: Extract JD signals (single call, fast)
  Pass 2: Rewrite each resume entry individually via structured JSON output

Usage:
    python resume_tailor.py --jd path/to/jd.txt
    python resume_tailor.py --jd path/to/jd.txt --resume path/to/resume.md
    python resume_tailor.py --jd path/to/jd.txt --model qwen3:14b
    cat jd.txt | python resume_tailor.py --jd -
    python resume_tailor.py --jd path/to/jd.txt --section experience
    python resume_tailor.py --jd path/to/jd.txt --output tailored_resume.md
    python resume_tailor.py --jd path/to/jd.txt --dry-run
"""

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path
import urllib.request
import urllib.error

DEFAULT_RESUME_PATH = Path(__file__).parent / "base/base_resume.md"
DEFAULT_MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ── Prompts ───────────────────────────────────────────────────────────────────

JD_EXTRACT_SYSTEM = "You are a technical recruiter. Extract the essential signals from job descriptions concisely."

JD_EXTRACT_PROMPT = """Extract the following from this job description. Be terse — one line each.

JD:
---
{jd}
---

Output ONLY this structure (no preamble):
ROLE: <job title>
CORE_PILLARS: <top 3-4 things this team cares most about, e.g. "CI/CD automation, Kubernetes reliability, observability">
MUST_HAVE: <5-8 hard requirements, comma-separated>
NICE_TO_HAVE: <3-5 preferred skills, comma-separated>
KEY_VERBS: <5-8 action verbs the JD uses, comma-separated>
DOMAIN: <primary domain>
SCALE: <scale signals or "not specified">
CULTURE: <1-2 words>"""

# Per-entry rewrite — rules from expert prompt, architecture stays per-entry + JSON
REWRITE_SYSTEM = """You are an expert technical resume writer specializing in SRE, DevOps, and Infrastructure Engineering. Return JSON only. No prose. /no_think"""

REWRITE_PROMPT = """You are rewriting resume bullets for a specific job. Strict rules:

JD core signals:
CORE_PILLARS: {core_pillars}
MUST_HAVE: {must_have}
KEY_VERBS: {key_verbs}

Rewrite each bullet to read like a senior engineer wrote it — not like a resume template was applied.
Internalize this structure: strong action → what was achieved → by what means. Do NOT write it out literally as "Accomplished X, as measured by Y, by doing Z" — that phrasing is a guide, not a format.

Rules:
- Use past tense throughout — these are completed work items, not current duties
- Vary the opening verb — do not repeat the same verb across bullets
- Use a KEY_VERB to open a bullet only where it genuinely fits the action; otherwise use the best past-tense verb
- Replace generic terms with MUST_HAVE equivalents only where genuinely equivalent
- Where a bullet mentions a tool or pattern that maps to a CORE_PILLAR, surface that connection naturally
- Use only metrics and numbers present verbatim in the input — do not invent new ones
- Do not merge bullets, split them, or change their count
- Do not invent tools, projects, or company names not in the input
- No buzzwords, no fluff, no filler phrases like "as measured by" or "in order to"

You have {n_bullets} bullets. Return the same count.

Bullets:
{numbered_bullets}

Return JSON only:
{{
  "bullets": ["<rewritten bullet 1>", "<rewritten bullet 2>", ...]
}}"""


# ── Resume entry splitter / reassembler ───────────────────────────────────────

ENTRY_RE = re.compile(r"(^#{1,3} .+)", re.M)
SECTION_PATTERNS = {
    "summary":    re.compile(r"(^#{1,2}\s*(summary|profile|about).*?)(?=^#{1,2}\s|\Z)", re.I | re.M | re.S),
    "skills":     re.compile(r"(^#{1,2}\s*(skills|tech stack|technologies).*?)(?=^#{1,2}\s|\Z)", re.I | re.M | re.S),
    "experience": re.compile(r"(^#{1,2}\s*(experience|work history|employment).*?)(?=^#{1,2}\s|\Z)", re.I | re.M | re.S),
    "projects":   re.compile(r"(^#{1,2}\s*(projects?|open.?source).*?)(?=^#{1,2}\s|\Z)", re.I | re.M | re.S),
    "education":  re.compile(r"(^#{1,2}\s*education.*?)(?=^#{1,2}\s|\Z)", re.I | re.M | re.S),
}


def split_into_entries(text: str) -> list[dict]:
    """
    Split markdown into a list of {heading_line, meta_lines, bullets, plains}.
    Heading levels: ## = section header (pass through), ### = rewritable entry.
    """
    entries = []
    lines = text.splitlines()
    current = None

    def flush():
        if current is not None:
            entries.append(current)

    for line in lines:
        if re.match(r"^#{1,2} ", line):
            flush()
            current = {"heading": line, "level": "section", "meta": [], "bullets": [], "plains": []}
        elif re.match(r"^### ", line):
            flush()
            current = {"heading": line, "level": "entry", "meta": [], "bullets": [], "plains": []}
        elif current is None:
            entries.append({"heading": None, "level": "top", "meta": [], "bullets": [], "plains": [line]})
        elif re.match(r"^\*[^*].+[^*]\*$", line.strip()):
            current["meta"].append(line)
        elif re.match(r"^[-*] ", line.strip()):
            current["bullets"].append(line.strip()[2:])
        elif line.strip():
            current["plains"].append(line)

    flush()
    return entries


def entry_to_text(e: dict) -> str:
    """Reconstruct an entry dict back to markdown."""
    parts = []
    if e["heading"]:
        parts.append(e["heading"])
    parts.extend(e["meta"])
    parts.extend(e["plains"])
    parts.extend(f"- {b}" for b in e["bullets"])
    return "\n".join(parts)


def apply_rewrite(entry: dict, result: dict) -> dict:
    """Merge JSON rewrite result back into an entry dict."""
    updated = dict(entry)
    if result.get("bullets"):
        updated["bullets"] = result["bullets"]
    if result.get("summary") and entry["level"] != "entry":
        updated["plains"] = [result["summary"]]
    return updated


def extract_section(resume: str, section: str) -> tuple[str, str, str]:
    pattern = SECTION_PATTERNS.get(section.lower())
    if not pattern:
        return "", resume, ""
    m = pattern.search(resume)
    if not m:
        return "", resume, ""
    start, end = m.span()
    return resume[:start], resume[start:end], resume[end:]


def get_sections_to_rewrite(resume: str, section_name: str | None) -> tuple[str, str, str]:
    if section_name:
        return extract_section(resume, section_name)
    _, edu, _ = extract_section(resume, "education")
    edu_start = resume.find(edu) if edu else len(resume)
    return "", resume[:edu_start], resume[edu_start:]


# ── Ollama helpers ────────────────────────────────────────────────────────────

def call_ollama(model: str, prompt: str, system: str,
                stream: bool = False, as_json: bool = False) -> str:
    body: dict = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": stream,
        "options": {
            "temperature": 0.2 if as_json else 0.4,
            "top_p": 0.9,
            "num_predict": 1024 if as_json else 2048,  # enough for think + JSON output
            "num_ctx": 4096,
        },
    }
    if as_json:
        body["format"] = "json"

    timeout = 60 if as_json else 180  # fail fast per entry, not hang for 3 min

    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )

    full_response = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if stream:
                for line in resp:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        full_response.append(token)
                        print(token, end="", flush=True)
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
                print()
                return "".join(full_response)
            else:
                data = json.loads(resp.read())
                return data.get("response", "").strip()
    except urllib.error.URLError as e:
        print(f"\nError: could not connect to Ollama at {OLLAMA_URL}", file=sys.stderr)
        print("Is Ollama running? Try: ollama serve", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)


def call_ollama_json(model: str, prompt: str, system: str) -> dict:
    """Call Ollama with JSON mode; returns parsed dict or {} on failure."""
    raw = call_ollama(model, prompt, system, stream=False, as_json=True)
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log(f"Warning: JSON parse failed, keeping original. Raw: {raw[:120]}")
        return {}


def check_ollama_model(model: str) -> bool:
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            base = model.split(":")[0]
            return any(m.startswith(base) for m in models)
    except Exception:
        return False


# ── Rewrite pass ──────────────────────────────────────────────────────────────

def parse_signals(signals: str) -> dict:
    """Extract CORE_PILLARS, MUST_HAVE and KEY_VERBS from pass-1 signal text."""
    out = {"core_pillars": "", "must_have": "", "key_verbs": ""}
    for line in signals.splitlines():
        if line.startswith("CORE_PILLARS:"):
            out["core_pillars"] = line.split(":", 1)[1].strip()
        elif line.startswith("MUST_HAVE:"):
            out["must_have"] = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_VERBS:"):
            out["key_verbs"] = line.split(":", 1)[1].strip()
    return out


# Known tech terms to check for hallucination
TECH_RE = re.compile(
    r"\b(kubernetes|k8s|argocd|loki|prometheus|grafana|terraform|ansible|"
    r"jenkins|boto3|helm|istio|envoy|zabbix|cloudnativepg|pagerduty|"
    r"github actions|gitlab|datadog|splunk|vault|consul)\b",
    re.I
)


def extract_tools(text: str) -> set[str]:
    """Return lowercase tool names found in text."""
    return {m.group(0).lower() for m in TECH_RE.finditer(text)}


def check_hallucination(original_bullets: list[str], new_bullets: list[str],
                        entry_heading: str) -> list[str]:
    """
    Reject any new bullet that introduces a tool not present in the original entry.
    Falls back to the original bullet for that position.
    """
    original_tools = extract_tools(" ".join(original_bullets))
    validated = []
    for orig, new in zip(original_bullets, new_bullets):
        new_tools = extract_tools(new)
        hallucinated = new_tools - original_tools
        if hallucinated:
            log(f"    ⚠ hallucination detected in [{entry_heading[:40]}]: {hallucinated} — kept original bullet")
            validated.append(orig)
        else:
            validated.append(new)
    return validated


def rewrite_entries(model: str, entries: list[dict], signals: str) -> list[dict]:
    """
    For each ### entry, send its bullets as a numbered list and expect the same
    count back. Validates for hallucinated tool names before accepting rewrites.
    Section headers and entries with no bullets pass through unchanged.
    """
    sig = parse_signals(signals)
    results = []

    for e in entries:
        if e["level"] != "entry" or not e["bullets"]:
            results.append(e)
            continue

        numbered = "\n".join(f"{i+1}. {b}" for i, b in enumerate(e["bullets"]))
        prompt = REWRITE_PROMPT.format(
            core_pillars=sig["core_pillars"],
            must_have=sig["must_have"],
            key_verbs=sig["key_verbs"],
            n_bullets=len(e["bullets"]),
            numbered_bullets=numbered,
        )
        result = call_ollama_json(model, prompt, REWRITE_SYSTEM)

        new_bullets = result.get("bullets", [])

        # Validate bullet count
        if not new_bullets or len(new_bullets) != len(e["bullets"]):
            log(f"  ✗ {e['heading'][:60]} (count mismatch {len(new_bullets)} != {len(e['bullets'])}, kept original)")
            results.append(e)
            continue

        # Validate for hallucinated tools, fall back per-bullet
        validated_bullets = check_hallucination(e["bullets"], new_bullets, e["heading"])
        log(f"  ✓ {e['heading'][:60]}")
        updated = dict(e)
        updated["bullets"] = validated_bullets
        results.append(updated)

    return results


# ── I/O ───────────────────────────────────────────────────────────────────────

def read_file_or_stdin(path: str) -> str:
    if path == "-":
        return sys.stdin.read().strip()
    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return p.read_text().strip()


def log(msg: str):
    print(msg, file=sys.stderr)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Two-pass resume tailor: extract JD signals, then rewrite entries via structured JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python resume_tailor.py --jd stripe_jd.txt
          python resume_tailor.py --jd cloudflare_jd.txt --model gemma3:12b
          python resume_tailor.py --jd datadog_jd.txt --section experience --output tailored.md
          cat jd.txt | python resume_tailor.py --jd -
          python resume_tailor.py --jd jd.txt --dry-run
        """)
    )
    parser.add_argument("--jd", required=True, metavar="PATH_OR_DASH")
    parser.add_argument("--resume", default=str(DEFAULT_RESUME_PATH), metavar="PATH")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--section", default=None, choices=list(SECTION_PATTERNS.keys()))
    parser.add_argument("--output", default=None, metavar="PATH")
    parser.add_argument("--no-stream", action="store_true", help="(unused; kept for pipeline compat)")
    parser.add_argument("--dry-run", action="store_true", help="Pass 1 only — print signals and exit")
    args = parser.parse_args()

    resume_text = read_file_or_stdin(args.resume)
    jd_text     = read_file_or_stdin(args.jd)

    if not resume_text: print("Error: resume is empty", file=sys.stderr); sys.exit(1)
    if not jd_text:     print("Error: JD is empty",     file=sys.stderr); sys.exit(1)

    if not check_ollama_model(args.model):
        log(f"Warning: model '{args.model}' not found. Try: ollama pull {args.model}")

    # ── Pass 1: JD signals ────────────────────────────────────────────────────
    log(f"\n[Pass 1] Extracting JD signals  (model: {args.model})")
    log("-" * 60)
    signals = call_ollama(
        model=args.model,
        prompt=JD_EXTRACT_PROMPT.format(jd=jd_text),
        system=JD_EXTRACT_SYSTEM,
        stream=False,
    )
    signals = re.sub(r"<think>.*?</think>", "", signals, flags=re.DOTALL).strip()
    log(signals)
    log("-" * 60)

    if args.dry_run:
        log("\n--dry-run: skipping rewrite pass.")
        return

    # ── Pass 2: per-entry rewrite ─────────────────────────────────────────────
    preamble, section_text, remainder = get_sections_to_rewrite(resume_text, args.section)

    if not section_text.strip():
        log(f"Warning: section '{args.section}' not found. Rewriting full resume.")
        section_text = resume_text
        preamble = remainder = ""

    entries = split_into_entries(section_text)
    rewritable = [e for e in entries if e["level"] == "entry" and (e["bullets"] or e["plains"])]
    log(f"\n[Pass 2] Rewriting {len(rewritable)} entries individually")
    log("-" * 60)

    updated_entries = rewrite_entries(args.model, entries, signals)

    rewritten = "\n".join(entry_to_text(e) for e in updated_entries)
    final = "\n\n".join(p for p in [preamble, rewritten, remainder] if p.strip())

    print(final)

    if args.output:
        Path(args.output).write_text(final)
        log(f"\nSaved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()