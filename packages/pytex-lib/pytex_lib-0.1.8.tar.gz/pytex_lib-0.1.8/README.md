# pytex-lib

**pytex-lib** is a Python library that simplifies inserting function outputs into LaTeX documents. The `@write_to_latex` decorator allows you to automatically write function results into a specified LaTeX file at a predefined keyword location. This is particularly useful for dynamically generating LaTeX reports, papers, or documents with computed values. Installation is straightforward via `pip install pytex-lib`, and integration requires minimal setup.

## Example Usage

Import the library:

```python
from pytex_lib import write_to_latex
```

Use the `write_to_latex` decorator to automatically output your function's result to a LaTeX file:

```python
@write_to_latex
def f(x):
    return x**2
```

Call the function with the `file_path` and `keyword` parameters:

```python
file_path = "Path/to/latex/doc"
keyword = "keyword in latex doc"
f(file_path=file_path, keyword=keyword)
```

This will modify your LaTeX document as follows:

```latex
\documentclass{article}
\begin{document}

The answer is 
% keyword in latex doc
(answer from f(x) = x^2)

\end{document}
```

## Installation

```bash
pip install pytex-lib
```
