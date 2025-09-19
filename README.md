# Arcane Scribe

Local, FOSS desktop app to query RPG rulebooks with RAG.

## Dev Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Commands
- Index PDFs: `python -m arcane_scribe.index /path/to/pdfs`
- Ask: `python -m arcane_scribe.ask "How does grapple work?"`

## License
TBD
