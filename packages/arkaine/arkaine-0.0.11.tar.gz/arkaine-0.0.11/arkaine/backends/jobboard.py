"""
The goal of the job board backend is to utilize multiple agents to
organize tool calling via "a job board". Basically, the agent explains
the task. Then, a separate agent (one per tool) utilizes the tool
descriptions to determine if the tool can be utilized to handle it at all.

Then a third agent reviews these applications of utilization and decide which ones
to utilize.

These tasks are then triggered, combined, and the agent is asked if they have another
follow up task or can conclude their task.

"""

from arkaine.backends.backend import Backend


class JobBoardBackend(Backend):
    """
    todo
    """

    def __init__(
        self,
        llm: LLM,
        tools: List[Tool],
        additional_descriptions: List[Optional[str]] = [],
    ):
        """
        todo
        """
        super().__init__(
            llm=llm,
            tools=tools,
            max_simultaneous_tools=0,
            initial_state={},
        )

        if len(additional_descriptions) > 0:
            if len(additional_descriptions) != len(tools):
                raise ValueError(
                    "additional_descriptions must be the same length as tools"
                )
            self.additional_descriptions = additional_descriptions
        else:
            self.additional_descriptions = [None] * len(tools)

    def make_task_posting(self, ctx: Context, task: str) -> str:
        """
        The goal of this sub-agent is to generate a human readable task posting
        as if it was going on a job board so that we can ask other agents to
        "apply" their expertise to it.
        """

        pass

    def make_job_applications(
        self, ctx: Context, task_posting: str
    ) -> List[Tuple[str, str, bool]]:
        """
        The goal of this sub-agent is to generate a list of job applications
        that can be used to apply to the task posting.

        The return is a list of tuples - the first element is the id of the tool, the second is
        the reason that it believes that it should be utilized, and the third is a boolean
        on whether it believes that the tool should be utilized.
        """

        pass

    def review_job_applications(
        self,
        ctx: Context,
        task_posting: str,
        job_applications: List[Tuple(str, str)],
    ) -> List[Tuple[str, bool]]:
        """
        The goal of this sub-agent is to review the job applications and determine
        which ones are the best fit for the task posting. It returns the reason it believes that
        the tool would/would not be a good fit, and then whether it should be utilized or not.
        """

        pass

    def parse_for_tool_calls(
        self, ctx: Context, text: str, stop_at_first_tool: bool = False
    ) -> ToolCalls:
        """
        todo
        """

        pass

    def parse_for_result(self, ctx: Context, text: str) -> Optional[Any]:
        """
        todo
        """

        pass

    def tool_results_to_prompts(
        self, ctx: Context, prompt: Prompt, results: ToolResults
    ) -> List[Prompt]:
        """
        todo
        """

        pass

    def prepare_prompt(self, ctx: Context, **kwargs) -> Prompt:
        """
        todo
        """

        pass
