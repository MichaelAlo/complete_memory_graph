# /lint

Run the repository lint workflow.

## Instructions
1. Read repository build files and infer the canonical lint command.
2. Prefer repo-specific commands over defaults.
3. Run the narrowest useful fast-feedback validation.
4. Report:
   - commands run
   - pass/fail
   - important warnings or errors
   - impacted files

## Fallback order
- `npm run lint`
- `pnpm lint`
- `yarn lint`
- `ruff check .`
- `eslint .`
- `make lint`
