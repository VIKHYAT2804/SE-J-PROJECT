# Lab 5 — Static Code Analysis: School Transport Register

This folder contains the assigned school transport Python program and the Lab 5 static-analysis deliverables.

## Files

- `school_transport.original.py` — unchanged baseline program.
- `school_transport.py` — corrected program.
- `issues.md` — issue table and fix approaches.
- `reflection.md` — reflection answers.
- `pylint_report_before.txt`, `pylint_report_after.txt` — Pylint output before and after changes.
- `bandit_report_before.txt`, `bandit_report_after.txt` — Bandit output before and after changes.
- `flake8_report_before.txt`, `flake8_report_after.txt` — Flake8 output before and after changes.

## Re-run analysis

Activate your Python virtual environment and run:

```bash
python school_transport.py
pylint school_transport.py
bandit -r school_transport.py
flake8 school_transport.py
```

## Verified results

- Pylint: **10.00/10** on the corrected program.
- Bandit: **No issues identified** on the corrected program.
- Flake8: no findings printed for the corrected program.

The baseline reports are for the original program. The final reports reflect runs performed in the lab terminal.
