from arkaine.toolbox.research.researcher import Researcher
from arkaine.flow import Linear, DoWhile
from arkaine.tools.tool import Tool
from arkaine.tools.argument import Argument


class DeepResearcher(Tool):
    def __init__(
        self,
        name: str,
        description: str = (
            "A researcher that iteratively researches a topic, "
            "expanding on follow up questions, until either the topic is "
            "sufficiently researched or a maximum depth or time constraint "
            "is triggered."
        ),
        max_depth: int = 3,
        max_time_seconds: int = 600,
        id: str = None,
    ):
        self.name = name
        self.description = description
        self.max_depth = max_depth
        self.max_time_seconds = max_time_seconds
        self.id = id

        args = [
            Argument(
                name="question",
                description=(
                    "The question to research; ensure you are "
                    "specific, detailed, and concise in asking "
                    "your question/topic."
                ),
                type="str",
                required=True,
            )
        ]

        super().__init__(
            name,
            description=description,
            arguments=args,
        )
