# /lint

Run the repository lint workflow.

## Instructions
1. Run `ruff check .` from the repository root.
2. If mypy is needed (type errors suspected), also run `mypy src/`.
3. Report:
   - commands run
   - pass/fail
   - important warnings or errors
   - impacted files

## Commands (in order)

```bash
ruff check .
```

For type checking:
```bash
mypy src/
```

## Fallback order
- `ruff check .`
- `ruff check src/`
- `flake8 src/`
- `mypy src/`
