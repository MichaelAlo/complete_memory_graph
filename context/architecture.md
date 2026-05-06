# Architecture

## Current system
Describe the enduring system shape here.

## Major modules
- `src/`: primary codebase root used for graph refreshes.
- `context/`: live operational memory.
- `raw/`: immutable source material.
- `wiki/`: compiled project knowledge.
- `graphify-out/`: structural graph outputs and summaries.

## Invariants
- `/checkpoint` updates semantic memory and structural memory together.
- Structural graph refreshes target `src/` by default.
