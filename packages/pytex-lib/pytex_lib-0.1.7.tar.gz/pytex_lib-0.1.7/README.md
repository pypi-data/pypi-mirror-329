# pytex-lib

Allows you to output your python functions directly to a LaTeX file.

# TODO

- [ ] Figure out out how to core file allows you to import it easier

# Example Usage

Import with
```python
from pytex_lib import write_to_latex
```

Then you can use the `write_to_latex` decorator to output your functions to a LaTeX file.

```python
@write_to_latex
def f(x):
    return x**2
```

You call the function with the `directory` and the `keyword` like this

```python
file_path = "Path/to/latex/doc"
keyword = "keyword in latex doc"
f(file_path=file_path, keyword=keyword)
```

Then your latex doc should look like this

```latex
\documentclass{article}
\begin{document}

The answer is 
% keyword in latex doc
(answer form f(x) = x^2)

\end{document}
```

# Installation

```bash
pip install pytex-lib
```





