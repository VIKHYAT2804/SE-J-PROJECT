# Lab 5: Static Code Analysis — Issue Documentation

Line numbers below refer to the original `school_transport.original.py`. The BEFORE findings are taken from the reports generated in the lab terminal. The AFTER results were checked after editing `school_transport.py`.

| Issue | Tool / type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command constructed from route data | Bandit B602 — High | 23–24 | `subprocess.run(..., shell=True)` interprets a concatenated string as a shell command. | Removed shell execution; the dispatch notice is printed directly. |
| SQL built with an f-string | Bandit B608 — Medium | 8–9 | Rider values are interpolated into SQL text, creating an injection risk. | Replaced interpolation with `?` placeholders and parameter values passed separately to `execute`. |
| `subprocess` import | Bandit B404 — Low | 1 | Bandit flags the subprocess module for review because it can be used unsafely. | Removed the import along with the shell invocation. |
| `assert` used for program validation | Bandit B101 — Low | 38 | Assertions can be disabled when Python runs with optimization. | Replaced the assertion with an explicit conditional that raises `ValueError` when the total is wrong. |
| Bare exception handler | Pylint / Flake8 | 30 | Bare `except:` can hide unrelated database or programming errors. | Removed the broad exception path; the aggregate query explicitly returns zero when no total exists. |
| File opened and closed manually | Pylint | 18–21 | A write error could prevent the explicit close from running; no encoding was specified. | Used `with open(..., encoding="utf-8")` so the file closes reliably. |
| Non-snake_case function names | Pylint | 8, 13, 17, 23, 27 | CamelCase names do not follow Python naming conventions. | Renamed functions to `enroll_rider`, `route_roster`, `export_roster`, `dispatch_alert`, and `fee_collected`. |
| Unused `driver` argument | Pylint | 13 | The argument was never used by `routeRoster`. | Removed the parameter and updated call sites. |
| Missing docstrings and long lines | Pylint / Flake8 | Multiple | The original module/functions lacked documentation and some lines exceeded configured limits. | Added module/function docstrings and split long statements over multiple lines. |
| Flake8 spacing and blank-line violations | Flake8 | Multiple | Missing spaces after commas and insufficient blank-line separation reduced consistency. | Applied standard Python spacing and blank-line conventions. |

## Verification summary

- Original Pylint score: **4.00/10**.
- Corrected Pylint score: **10.00/10**.
- Corrected Bandit report: **No issues identified**.
- Corrected Flake8 report: **No output**, indicating no reported violations.
