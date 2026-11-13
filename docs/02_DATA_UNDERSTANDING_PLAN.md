# Phase 2 – Data Understanding Plan

**Goal:** Thoroughly understand the structure, quality, and content of the three ranking files before any cleaning or modelling.

## Checklist

- [ ] Confirm exact file names and formats present in `data/raw/`
- [ ] Load each file and record:
  - Shape (rows × columns)
  - Column names & dtypes
  - Missing value counts & percentages
  - Duplicate rows
  - Basic statistics for numeric columns (Sales, YOY, Units, etc.)
  - Unique values / cardinality for categorical columns (Segment, Location, Franchising, State, etc.)
- [ ] Identify obvious data-quality issues (inconsistent units, currency symbols, percentage signs, mixed types, outliers)
- [ ] Document business meaning of each column
- [ ] Note relationships / possible joins between the three tables (Restaurant name is the natural key)
- [ ] Produce a short Data Quality Report (Markdown or HTML) saved in `docs/` and key summary tables in `reports/`

## Deliverable of this phase
`docs/02_DATA_QUALITY_REPORT.md` + any profiling notebooks/scripts.

