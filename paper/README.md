# Yogacara: arXiv Submission Guide

## Overview

This guide provides instructions for submitting the Yogacara paper to arXiv.

## Required Files

Before submission, ensure you have the following files:

```
yogacara_paper/
├── main.tex           # Main LaTeX document
├── references.bib     # Bibliography file
├── arxiv.sty          # arXiv LaTeX style (optional, included in arXiv template)
├── README.md          # This file
└── [additional source files if needed]
```

## Submission Steps

### 1. Prepare Your Files

#### Option A: Using arXiv Web Interface

1. **Visit arXiv**: Go to [https://arxiv.org/submit](https://arxiv.org/submark)
2. **Start Submission**: Click "Submit" and follow the wizard
3. **Upload Source**: Select "LaTeX" as the format and upload your `.tex` and `.bib` files
4. **arXiv will compile** your submission automatically

#### Option B: Using arXiv API (Command Line)

```bash
# Install arxiv-cli tools
pip install arxiv-cli

# Upload and submit
arxiv submit main.tex references.bib
```

### 2. Author Anonymization (Optional)

For double-blind review, replace author information:

```latex
% In main.tex, change:
\author{
    Author Name\textsuperscript{1} \\
    \textsuperscript{1}Institution Name \\
    email@example.com
}

% To anonymous:
\author{
    Author Name$^1$ \\
    $^1$Anonymous Institution
}
```

### 3. Compile Locally (Recommended)

Before submitting, compile locally to catch errors:

```bash
# Using pdflatex
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or use arxiv-latex (automates the above)
pip install arxiv-latex
latex-tool build main.tex
```

### 4. Common Issues and Solutions

#### Missing References

If you see "Citation undefined" warnings:
```bash
pdflatex main.tex
bibtex main      # This step generates the .bbl file
pdflatex main.tex
pdflatex main.tex
```

#### Package Not Found

arXiv has a limited package set. Common packages are supported:
- `hyperref`, `amsmath`, `booktabs`, `geometry`
- For lstlisting, use `listings` package

If a package is unavailable, either:
1. Remove the package and use alternatives
2. Include the package source in your submission

#### Figure/Table Placement

arXiv may warn about floats. This is usually fine. Use `[!htbp]` for flexible placement.

### 5. arXiv-Specific Considerations

#### File Size Limits
- Source: 10MB limit
- PDF: 10MB limit
- Use `\includegraphics[width=0.8\textwidth]{...}` for large figures

#### Compile Timeout
- If compilation takes >10 minutes, arXiv may timeout
- Simplify complex figures or reduce document complexity

#### License
- Default: arXiv non-exclusive license
- Choose appropriate license during submission

## arXiv Categories

For this paper, recommended categories:

**Primary**: `cs.AI` (Artificial Intelligence)

**Secondary** (optional):
- `cs.CL` (Computation and Language)
- `cs.MA` (Multiagent Systems)

## After Submission

1. **Wait for Processing**: arXiv typically processes in 24-72 hours
2. **Check Compiler Log**: You'll receive an email with compilation results
3. **Make Revisions** if needed using the "Edit" function
4. **Cross-list** to other categories if relevant

## arXiv Checklist

- [ ] `main.tex` compiles without errors
- [ ] `references.bib` is properly formatted
- [ ] All figures are included (PNG, JPG, or PDF format recommended)
- [ ] No broken references or citations
- [ ] Author information is anonymized (if double-blind)
- [ ] PDF renders correctly
- [ ] Abstract is within typical length (150-300 words)

## Support

- arXiv Help: [https://arxiv.org/help](https://arxiv.org/help)
- Submission FAQ: [https://arxiv.org/help/faq](https://arxiv.org/help/faq)
- arXiv Submit: [https://arxiv.org/submit](https://arxiv.org/submit)

## License

This paper is available under the arXiv non-exclusive license.

---

*Last updated: 2024*
