#!/usr/bin/env python3
"""
resume_render.py - Fill a .docx resume template with tailored markdown content.

Reads a markdown resume (from resume_tailor.py or manually written) and
renders it into a .docx template, preserving the template's fonts, colors,
and styles. Can also export to PDF via LibreOffice.

Usage:
    python resume_render.py --input tailored.md --template my_resume.docx
    python resume_render.py --input tailored.md --template my_resume.docx --format pdf
    python resume_render.py --input tailored.md --template my_resume.docx --output stripe_resume.docx
    cat tailored.md | python resume_render.py --input - --template my_resume.docx --format pdf

Pipeline usage (combine with resume_tailor.py):
    python resume_tailor.py --jd stripe_jd.txt --no-stream | \\
        python resume_render.py --input - --template my_resume.docx --format pdf --output stripe.pdf

Dependencies:
    pip install python-docx lxml --break-system-packages
    LibreOffice (for PDF export): sudo apt install libreoffice
"""

import argparse
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from copy import deepcopy

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from lxml import etree
except ImportError as e:
    print(f"Error: missing dependency — {e}", file=sys.stderr)
    print("Fix: pip install python-docx lxml --break-system-packages", file=sys.stderr)
    sys.exit(1)

HYPERLINK_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"

# ---------------------------------------------------------------------------
# Link registry
# ---------------------------------------------------------------------------

def parse_link_registry(text: str) -> dict:
    """
    Parse the <!-- links ... --> block from the markdown.
    Returns dict of {display_text_lower: url}.
    """
    registry = {}
    m = re.search(r"<!--\s*links(.*?)-->", text, re.DOTALL)
    if not m:
        return registry
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        label, url = line.split("|", 1)
        registry[label.strip().lower()] = url.strip()
    return registry


def strip_link_registry(text: str) -> str:
    """Remove the <!-- links ... --> block from markdown text."""
    return re.sub(r"<!--\s*links.*?-->", "", text, flags=re.DOTALL).strip()


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

def parse_markdown_resume(text: str) -> dict:
    """
    Parse a markdown resume into structured sections.
    Returns:
        {
            "name": str,
            "subtitle": str,
            "contact": str,          # raw markdown, may contain [text](url)
            "sections": [
                {"title": str, "entries": [
                    {"header": str, "meta": str, "bullets": [str], "plain": [str]}
                ]}
            ]
        }
    """
    # Strip link registry before parsing
    text = strip_link_registry(text)

    lines = text.splitlines()
    result = {"name": "", "subtitle": "", "contact": "", "sections": []}
    current_section = None
    current_entry = None
    i = 0

    def flush_entry():
        if current_entry and current_section is not None:
            result["sections"][current_section]["entries"].append(current_entry)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # H1 = name
        if stripped.startswith("# ") and not result["name"]:
            result["name"] = stripped[2:].strip()
            i += 1
            continue

        # lines right after name: subtitle then contact
        if result["name"] and not result["contact"] and not stripped.startswith("#"):
            if stripped:
                if not result["subtitle"] and "|" not in stripped and "@" not in stripped \
                        and "github" not in stripped.lower() and "linkedin" not in stripped.lower() \
                        and "[" not in stripped:
                    result["subtitle"] = re.sub(r"[*_]", "", stripped)
                    i += 1
                    continue
                elif "|" in stripped or "@" in stripped or "github" in stripped.lower() \
                        or "linkedin" in stripped.lower() or "[" in stripped:
                    result["contact"] = stripped  # keep raw markdown links intact
                    i += 1
                    continue

        # H2 = section heading
        if stripped.startswith("## "):
            flush_entry()
            current_entry = None
            result["sections"].append({"title": stripped[3:].strip(), "entries": []})
            current_section = len(result["sections"]) - 1
            i += 1
            continue

        # H3 = job/project title
        if stripped.startswith("### "):
            flush_entry()
            current_entry = {"header": stripped[4:].strip(), "meta": "", "bullets": [], "plain": []}
            i += 1
            continue

        # italic line = meta
        if current_entry is not None and re.match(r"^\*[^*].+[^*]\*$", stripped):
            current_entry["meta"] = stripped.strip("*").strip()
            i += 1
            continue

        # bullet
        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = stripped[2:].strip()
            if current_entry is not None:
                current_entry["bullets"].append(bullet_text)
            elif current_section is not None:
                if not result["sections"][current_section]["entries"]:
                    result["sections"][current_section]["entries"].append(
                        {"header": "", "meta": "", "bullets": [], "plain": []}
                    )
                result["sections"][current_section]["entries"][-1]["bullets"].append(bullet_text)
            i += 1
            continue

        # plain non-empty line
        if stripped and current_section is not None and not stripped.startswith("#"):
            if current_entry is not None:
                current_entry["plain"].append(stripped)
            else:
                if not result["sections"][current_section]["entries"]:
                    result["sections"][current_section]["entries"].append(
                        {"header": "", "meta": "", "bullets": [], "plain": []}
                    )
                result["sections"][current_section]["entries"][-1]["plain"].append(stripped)

        i += 1

    flush_entry()
    return result


# ---------------------------------------------------------------------------
# XML / run helpers
# ---------------------------------------------------------------------------

def _clone_pPr(src_para):
    pPr = src_para._p.find(qn("w:pPr"))
    return deepcopy(pPr) if pPr is not None else None


def _get_first_rPr_xml(para) -> str:
    for r in para._p.findall(qn("w:r")):
        rPr = r.find(qn("w:rPr"))
        if rPr is not None:
            return etree.tostring(rPr, encoding="unicode")
    return etree.tostring(OxmlElement("w:rPr"), encoding="unicode")


def _make_run(text: str, ref_rPr_xml: str, bold=None, italic=None, color=None) -> etree._Element:
    rPr = deepcopy(etree.fromstring(ref_rPr_xml))

    for tag in ("w:b", "w:bCs"):
        el = rPr.find(qn(tag))
        if bold is True and el is None:
            rPr.append(OxmlElement(tag))
        elif bold is False and el is not None:
            rPr.remove(el)

    for tag in ("w:i", "w:iCs"):
        el = rPr.find(qn(tag))
        if italic is True and el is None:
            rPr.append(OxmlElement(tag))
        elif italic is False and el is not None:
            rPr.remove(el)

    if color:
        c = rPr.find(qn("w:color"))
        if c is None:
            c = OxmlElement("w:color")
            rPr.append(c)
        c.set(qn("w:val"), color)

    r = OxmlElement("w:r")
    r.append(rPr)
    t = OxmlElement("w:t")
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    r.append(t)
    return r


def _make_hyperlink(doc: Document, text: str, url: str, ref_rPr_xml: str,
                    color="729FCF", bold=False) -> etree._Element:
    """Build a <w:hyperlink> element, registering the URL as a relationship."""
    rId = doc.part.relate_to(url, HYPERLINK_REL, is_external=True)

    rPr = deepcopy(etree.fromstring(ref_rPr_xml))

    # Remove bold unless requested
    for tag in ("w:b", "w:bCs"):
        el = rPr.find(qn(tag))
        if not bold and el is not None:
            rPr.remove(el)

    # Set colour
    c = rPr.find(qn("w:color"))
    if c is None:
        c = OxmlElement("w:color")
        rPr.append(c)
    c.set(qn("w:val"), color)

    # Suppress underline (matches template style)
    u = rPr.find(qn("w:u"))
    if u is None:
        u = OxmlElement("w:u")
        rPr.append(u)
    u.set(qn("w:val"), "none")

    r = OxmlElement("w:r")
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)

    hl = OxmlElement("w:hyperlink")
    hl.set(qn("r:id"), rId)
    hl.append(r)
    return hl


# ---------------------------------------------------------------------------
# Inline markdown → runs  (handles [text](url) and **bold**)
# ---------------------------------------------------------------------------

INLINE_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*")

def _emit_inline(p_el, doc: Document, text: str, ref_rPr_xml: str,
                 bold=None, italic=None):
    """
    Append runs to p_el, handling [text](url) as hyperlinks and **bold**.
    bold=None means auto-detect ** markers; bold=True/False forces it.
    """
    pos = 0
    for m in INLINE_RE.finditer(text):
        # plain text before this match
        if m.start() > pos:
            chunk = text[pos:m.start()]
            r = _make_run(chunk, ref_rPr_xml, bold=bold, italic=italic)
            p_el.append(r)

        if m.group(1) is not None:
            # [text](url) — hyperlink
            hl = _make_hyperlink(doc, m.group(1), m.group(2), ref_rPr_xml)
            p_el.append(hl)
        else:
            # **bold**
            b = True if bold is None else bold
            r = _make_run(m.group(3), ref_rPr_xml, bold=b, italic=italic)
            p_el.append(r)

        pos = m.end()

    # trailing plain text
    if pos < len(text):
        r = _make_run(text[pos:], ref_rPr_xml, bold=bold, italic=italic)
        p_el.append(r)


def _clear_document_body(doc: Document):
    body = doc.element.body
    for child in list(body):
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag in ("p", "tbl", "sdt"):
            body.remove(child)


# ---------------------------------------------------------------------------
# Paragraph builders
# ---------------------------------------------------------------------------

TEMPLATE_PARA_ROLES = {
    "name":           0,
    "subtitle":       1,
    "contact":        2,
    "section_header": 3,
    "body_text":      4,
    "job_header":     11,
    "bullet":         12,
    "italic_desc":    26,
    "project_header": 27,
}


def _add_name(doc, ref, text):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    p.append(_make_run(text, rPr_xml, bold=True))
    doc.element.body.append(p)


def _add_subtitle(doc, ref, text):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    p.append(_make_run(text, rPr_xml, bold=False))
    doc.element.body.append(p)


def _add_contact(doc, ref, raw_text):
    """
    Contact line: [text](url) → hyperlink in blue, plain text in grey.
    Separators (·) rendered in blue to match template.
    """
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)

    # Split on · keeping separators
    segments = re.split(r"(\s*·\s*)", raw_text)
    for seg in segments:
        seg_stripped = seg.strip()
        link_m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", seg_stripped)
        if link_m:
            hl = _make_hyperlink(doc, link_m.group(1), link_m.group(2), rPr_xml,
                                 color="729FCF", bold=True)
            p.append(hl)
        elif "·" in seg:
            r = _make_run(seg, rPr_xml, bold=True, color="729FCF")
            p.append(r)
        elif seg_stripped:
            r = _make_run(seg, rPr_xml, bold=False, color="555555")
            p.append(r)

    doc.element.body.append(p)


def _add_section_header(doc, ref, title):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    p.append(_make_run(title.upper(), rPr_xml, bold=True))
    doc.element.body.append(p)


def _add_job_header(doc, ref, header, meta):
    """Title · Company · context [TAB] italic grey date"""
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)

    parts = [x.strip() for x in header.split("·")]
    for idx, part in enumerate(parts):
        if idx == 0:
            p.append(_make_run(part, rPr_xml, bold=True))
        elif idx == 1:
            p.append(_make_run("  ·  ", rPr_xml, bold=False, color="555555"))
            p.append(_make_run(part, rPr_xml, bold=True))
        else:
            p.append(_make_run("  ·  ", rPr_xml, bold=False, color="555555"))
            p.append(_make_run(part, rPr_xml, bold=False, color="555555"))

    if meta:
        tab_r = OxmlElement("w:r")
        tab_r.append(deepcopy(etree.fromstring(rPr_xml)))
        tab_r.append(OxmlElement("w:tab"))
        p.append(tab_r)
        p.append(_make_run(meta, rPr_xml, bold=False, italic=True, color="888888"))

    doc.element.body.append(p)


def _add_project_header(doc, ref, header, meta):
    """
    Project header: [name](url) — *stack*
    The header from markdown is like:
      [log-explainer](https://github.com/...) — Python · Ollama · GitHub Actions · GHCR
    Render: hyperlink name in blue, dash + stack in grey italic.
    """
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)

    # Try to split on " — "
    if " — " in header:
        link_part, stack_part = header.split(" — ", 1)
    else:
        link_part = header
        stack_part = ""

    # Emit link part (may be [text](url) or plain text)
    link_m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", link_part.strip())
    if link_m:
        hl = _make_hyperlink(doc, link_m.group(1), link_m.group(2), rPr_xml,
                             color="729FCF", bold=True)
        p.append(hl)
    else:
        p.append(_make_run(link_part.strip(), rPr_xml, bold=True))

    # Emit " — stack" in grey italic
    if stack_part:
        p.append(_make_run("  —  ", rPr_xml, bold=False, color="888888"))
        p.append(_make_run(stack_part.strip(), rPr_xml, bold=False, italic=True, color="888888"))

    doc.element.body.append(p)


def _add_plain(doc, ref, text):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    _emit_inline(p, doc, text, rPr_xml)
    doc.element.body.append(p)


def _add_italic_desc(doc, ref, text):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    p.append(_make_run(text, rPr_xml, bold=False, italic=True))
    doc.element.body.append(p)


def _add_bullet(doc, ref, text):
    p = OxmlElement("w:p")
    pPr = _clone_pPr(ref)
    if pPr is not None: p.append(pPr)
    rPr_xml = _get_first_rPr_xml(ref)
    _emit_inline(p, doc, text, rPr_xml)
    doc.element.body.append(p)


# ---------------------------------------------------------------------------
# Detect whether a ### header is a project header (has [link] or — stack)
# ---------------------------------------------------------------------------

def _is_project_header(header: str) -> bool:
    return header.startswith("[") or " — " in header


# ---------------------------------------------------------------------------
# Main renderer
# ---------------------------------------------------------------------------

def render_to_docx(parsed: dict, template_path: str, output_path: str):
    doc = Document(template_path)
    refs = {role: doc.paragraphs[idx] for role, idx in TEMPLATE_PARA_ROLES.items()}

    _clear_document_body(doc)

    if parsed["name"]:
        _add_name(doc, refs["name"], parsed["name"])

    if parsed.get("subtitle"):
        _add_subtitle(doc, refs["subtitle"], parsed["subtitle"])

    if parsed["contact"]:
        _add_contact(doc, refs["contact"], parsed["contact"])

    for section in parsed["sections"]:
        _add_section_header(doc, refs["section_header"], section["title"])

        for entry in section["entries"]:
            if entry["header"]:
                if _is_project_header(entry["header"]):
                    _add_project_header(doc, refs["project_header"], entry["header"], entry["meta"])
                else:
                    _add_job_header(doc, refs["job_header"], entry["header"], entry["meta"])
            elif entry["meta"]:
                _add_italic_desc(doc, refs["italic_desc"], entry["meta"])

            for plain in entry["plain"]:
                if re.match(r"^\*[^*].+[^*]\*$", plain.strip()):
                    _add_italic_desc(doc, refs["italic_desc"], plain.strip().strip("*").strip())
                else:
                    _add_plain(doc, refs["body_text"], plain)

            for bullet in entry["bullets"]:
                _add_bullet(doc, refs["bullet"], bullet)

    # Word requires body to end with a paragraph
    last = doc.element.body[-1]
    if last.tag.split("}")[-1] != "p":
        doc.element.body.append(OxmlElement("w:p"))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"Saved DOCX: {output_path}", file=sys.stderr)


def convert_to_pdf(docx_path: str, output_path: str):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print("Error: LibreOffice not found. Install with: sudo apt install libreoffice", file=sys.stderr)
        sys.exit(1)

    out_dir = str(Path(output_path).parent.resolve())
    cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", out_dir, docx_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"LibreOffice error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    auto_name = Path(docx_path).stem + ".pdf"
    auto_path = Path(out_dir) / auto_name
    if str(auto_path) != output_path:
        auto_path.rename(output_path)

    print(f"Saved PDF:  {output_path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Render a markdown resume into a .docx template (and optionally PDF).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python resume_render.py --input tailored.md --template my_resume.docx
          python resume_render.py --input tailored.md --template my_resume.docx --format pdf
          python resume_render.py --input tailored.md --template my_resume.docx --format both
        """)
    )
    parser.add_argument("--input", required=True, metavar="PATH_OR_DASH")
    parser.add_argument("--template", required=True, metavar="PATH")
    parser.add_argument("--output", default=None, metavar="PATH")
    parser.add_argument("--format", default="docx", choices=["docx", "pdf", "both"])
    args = parser.parse_args()

    if args.input == "-":
        md_text = sys.stdin.read().strip()
    else:
        p = Path(args.input)
        if not p.exists():
            print(f"Error: input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        md_text = p.read_text().strip()

    if not md_text:
        print("Error: input markdown is empty", file=sys.stderr)
        sys.exit(1)

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"Error: template not found: {args.template}", file=sys.stderr)
        sys.exit(1)

    stem = args.output.replace(".docx", "").replace(".pdf", "") if args.output else template_path.stem + "_tailored"
    docx_out = stem + ".docx"
    pdf_out  = stem + ".pdf"

    Path(docx_out).parent.mkdir(parents=True, exist_ok=True)

    parsed = parse_markdown_resume(md_text)

    if not parsed["name"] and not parsed["sections"]:
        print("Warning: could not parse any structure from the markdown.", file=sys.stderr)

    if args.format in ("docx", "both"):
        render_to_docx(parsed, str(template_path), docx_out)

    if args.format == "pdf":
        tmp_docx = stem + "_tmp.docx"
        render_to_docx(parsed, str(template_path), tmp_docx)
        convert_to_pdf(tmp_docx, pdf_out)
        Path(tmp_docx).unlink(missing_ok=True)

    if args.format == "both":
        convert_to_pdf(docx_out, pdf_out)


if __name__ == "__main__":
    main()