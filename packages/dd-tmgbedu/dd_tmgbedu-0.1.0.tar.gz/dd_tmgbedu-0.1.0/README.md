# Python `dd`
The missing `dd` function in python. The `dd` function is abbreviation of die and dump, which means prints the variable and stop the executions. Here, another, `dump` function is provided, which just prints the variable, and doesn't stop the execution.

![](./docs/screen.png)



## Installation
```
pip install python_dd
```

### Uses

```python
from src.dd_tmgbedu.dd import dd

dd("Hello")
dd(1)
dd(True, True, False, 1, 2)
```

or

```python
from src.dd_tmgbedu.dd import dump

dump("Hello")
dump(1)
dump(True, False, 1, 2)
```

