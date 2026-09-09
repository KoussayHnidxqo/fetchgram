# Usage

The README covers the basics. This page collects the
longer examples and the notes that did not fit up front.

## Basic

```bash
python crawler.py https://example.com/blog --pages 5 --out data.csv
```

## Notes

- Simple on-disk cache so reruns are fast
- Concurrent fetching with a worker pool
