Syncio is inspired by `asyncio`. you can easy to create task and gather with `syncio.gather()` (multiprocessing) or `syncio.thread_gather()` (threading).

## Example
```python
from syncio import create_task, gather


def hello(n: int) -> str:
    return f"hello {n + 1}"


tasks = [create_task(hello)(i) for i in range(3)]
results = gather(*tasks)
print("output task_1:", results["task_1"])
print("output task_2:", results["task_2"])
print("output task_3:", results["task_3"])

# or using iterator

for result in results:
    print(result)

```
author: guangrei.