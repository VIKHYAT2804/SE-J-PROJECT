# Lab 6 – Code and Branch Coverage

This folder contains the pizza-order application, separate test suites for line/code coverage and branch coverage, and terminal screenshots of the test runs and coverage reports.

## Install dependencies
```bash
python -m pip install -r requirements.txt
```

## Code coverage
```bash
python -m coverage erase
python -m coverage run -m pytest -v CodeCoverageTest_xxxx_application.py
python -m coverage report -m
```

## Branch coverage
```bash
python -m coverage erase
python -m coverage run --branch -m pytest -v BranchCoverageTest_xxxx_application.py
python -m coverage report -m
```

## Captured results
- Code coverage tests: 4 passed; application line coverage: 100%.
- Branch coverage tests: 9 passed; application branch coverage: 100%.

Screenshots: `code_test.png`, `code_coverage.png`, `branch_test.png`, and `branch_coverage.png`.

Replace `xxxx` in both test filenames if your instructor requires your student identifier in the filenames.
