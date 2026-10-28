# Lab 5: Static Code Analysis — Reflection

*The supplied three-page handout lists the lab objectives and deliverables but does not show the exact reflection-question prompts. These answers cover four relevant reflection topics; replace the headings with your instructor's exact wording if the questions were supplied separately.*

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps detect likely defects, unsafe coding patterns, and style violations early, improving maintainability and making code reviews more effective. It complements runtime testing; it does not prove the program is correct in every situation.

## 2. What problems did the tools identify?

Bandit identified a high-severity shell execution concern, a medium-severity SQL construction concern, a subprocess-module review warning, and use of `assert`. Pylint reported missing docstrings, non-snake_case names, long lines, an unused parameter, a broad exception handler, and file-handling improvements. Flake8 reported long lines, missing whitespace, blank-line spacing, and the bare exception.

## 3. Which fixes were most important?

The highest-priority changes removed shell interpretation of route data and replaced SQL string interpolation with parameterized queries. The program now uses an explicit fee-total check instead of `assert`, and a context manager with UTF-8 encoding for roster export. Removing the bare exception prevents unrelated errors from being hidden. Naming, documentation, and formatting changes improve readability and consistency.

## 4. What are the limitations of static analysis?

Static-analysis tools can flag patterns that require human judgment and may not detect every runtime defect. Their findings should be reviewed in context, and behavior should still be checked by running the program and performing suitable tests. Using Pylint, Bandit, and Flake8 together provides complementary checks for code quality, common security risks, and formatting.
