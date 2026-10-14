# changelogic

Parse small Markdown release fragments into stable, scriptable release notes.

```bash
python -m pip install changelogic
```

```python
from changelogic import parse_directory, render

notes = render(parse_directory("changes"), title="v1.4.0")
```

Fragments use a deliberately tiny format such as `added: support signed URLs`. Files are read in filename order, grouped using conventional categories, and retain their source as an HTML comment for release review. Empty or malformed fragments are skipped when reading a directory.
