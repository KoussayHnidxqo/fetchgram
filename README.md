# fetchgram

Scrape article metadata into tidy CSV files

Small but I use it weekly.

## Highlights

- Per-domain delay to stay polite
- Concurrent fetching with a worker pool
- Simple on-disk cache so reruns are fast
- Exports tidy CSV ready for pandas
- Retries with exponential backoff

## Installation

```bash
pip install -r requirements.txt
```

## Examples

```bash
python crawler.py https://example.com/blog --pages 5 --out data.csv
```

## Project structure

```text
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── usage.md
├── examples/
│   └── quickstart.md
├── tests/
│   └── test_smoke.py
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── SECURITY.md
├── crawler.py
└── requirements.txt
```

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

## Notes

- mostly stable, edge cases remain

## License

MIT. Do whatever you want.
