# pytex-lib

**pytex-lib** is a Python library that simplifies inserting function outputs into LaTeX documents. The `@write_to_latex` decorator allows you to automatically write function results into a specified LaTeX file at a predefined keyword location. This is particularly useful for dynamically generating LaTeX reports, papers, or documents with computed values. Installation is straightforward via `pip install pytex-lib`, and integration requires minimal setup.

## Example Usage

### Import the Library

```python
from pytex_lib import write_to_latex
```

### Define a Function

Use the `@write_to_latex` decorator to output your function’s result to a LaTeX file:

```python
@write_to_latex
def compute_square(x):
    return f"The square of {x} is {x**2}"
```

### Initial LaTeX Document (`document.tex`)

Before calling the function, your LaTeX document (`document.tex`) might look like this:

```latex
\documentclass{article}
\begin{document}

Here is the computed result:
% RESULT_PLACEHOLDER

\end{document}
```

### Call the Function

Now, execute the function, specifying the LaTeX file and the keyword where the result should be inserted:

```python
file_path = "document.tex"
keyword = "RESULT_PLACEHOLDER"
compute_square(4, file_path=file_path, keyword=keyword)
```

### Updated LaTeX Document (`document.tex`)

After running the function, `document.tex` will be updated as follows:

```latex
\documentclass{article}
\begin{document}

Here is the computed result:
% RESULT_PLACEHOLDER
(The square of 4 is 16)

\end{document}
```

## Installation

```bash
pip install pytex-lib
```
