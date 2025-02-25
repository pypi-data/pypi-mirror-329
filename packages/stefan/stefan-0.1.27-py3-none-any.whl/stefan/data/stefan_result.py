from datetime import timedelta
from pydantic import BaseModel

class StefanResult(BaseModel):
    """
    Result of a Stefan execution.
    """
    task: str
    result: str
    cost: float
    duration: timedelta

    @property
    def result_as_markdown(self) -> str:
        return _RESULT_MARKDOWN_TEMPLATE.format(
            task=self.task,
            result=self.result,
            cost=self.cost,
            duration=self.duration
        )

_RESULT_MARKDOWN_TEMPLATE = """
## Stefan execution result:

Štefan got the following task:

{task}

which was finished with the following result:

```
{result}
```

Execution cost: {cost} USD
Total execution time: {duration}

"""