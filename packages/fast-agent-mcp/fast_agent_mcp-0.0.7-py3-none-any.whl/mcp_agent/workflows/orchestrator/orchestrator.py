"""
Orchestrator implementation for MCP Agent applications.
"""

import contextlib
from typing import (
    Callable,
    List,
    Literal,
    Optional,
    Type,
    TYPE_CHECKING,
)

from mcp_agent.agents.agent import Agent, AgentConfig
from mcp_agent.workflows.llm.augmented_llm import (
    AugmentedLLM,
    MessageParamT,
    MessageT,
    ModelT,
    RequestParams,
)
from mcp_agent.workflows.llm.model_factory import ModelFactory
from mcp_agent.workflows.orchestrator.orchestrator_models import (
    format_plan_result,
    format_step_result,
    NextStep,
    Plan,
    PlanResult,
    Step,
    StepResult,
    TaskWithResult,
)
from mcp_agent.workflows.orchestrator.orchestrator_prompts import (
    FULL_PLAN_PROMPT_TEMPLATE,
    ITERATIVE_PLAN_PROMPT_TEMPLATE,
    SYNTHESIZE_PLAN_PROMPT_TEMPLATE,
    TASK_PROMPT_TEMPLATE,
)
from mcp_agent.logging.logger import get_logger

if TYPE_CHECKING:
    from mcp_agent.context import Context

logger = get_logger(__name__)


class Orchestrator(AugmentedLLM[MessageParamT, MessageT]):
    """
    In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks,
    delegates them to worker LLMs, and synthesizes their results. It does this
    in a loop until the task is complete.

    When to use this workflow:
        - This workflow is well-suited for complex tasks where you can't predict the
        subtasks needed (in coding, for example, the number of files that need to be
        changed and the nature of the change in each file likely depend on the task).

    Example where orchestrator-workers is useful:
        - Coding products that make complex changes to multiple files each time.
        - Search tasks that involve gathering and analyzing information from multiple sources
        for possible relevant information.
    """

    def __init__(
        self,
        llm_factory: Callable[[Agent], AugmentedLLM[MessageParamT, MessageT]],
        planner: AugmentedLLM | None = None,
        available_agents: List[Agent | AugmentedLLM] | None = None,
        plan_type: Literal["full", "iterative"] = "full",
        context: Optional["Context"] = None,
        **kwargs,
    ):
        """
        Args:
            llm_factory: Factory function to create an LLM for a given agent
            planner: LLM to use for planning steps (if not provided, a default planner will be used)
            plan_type: "full" planning generates the full plan first, then executes. "iterative" plans the next step, and loops until success.
            available_agents: List of agents available to tasks executed by this orchestrator
            context: Application context
        """
        # Initialize with orchestrator-specific defaults
        orchestrator_params = RequestParams(
            use_history=False,  # Orchestrator doesn't support history
            max_iterations=30,  # Higher default for complex tasks
            maxTokens=8192,  # Higher default for planning TODO this will break some models - make configurable.
            parallel_tool_calls=True,
        )

        # If kwargs contains request_params, merge with our defaults but force use_history False
        if "request_params" in kwargs:
            base_params = kwargs["request_params"]
            merged = base_params.model_copy()
            merged.use_history = False  # Force this setting
            kwargs["request_params"] = merged
        else:
            kwargs["request_params"] = orchestrator_params

        super().__init__(context=context, **kwargs)

        self.llm_factory = llm_factory

        # Create default planner with AgentConfig
        request_params = self.get_request_params(kwargs.get("request_params"))
        planner_config = AgentConfig(
            name="LLM Orchestrator",
            instruction="""
            You are an expert planner. Given an objective task and a list of MCP servers (which are collections of tools)
            or Agents (which are collections of servers), your job is to break down the objective into a series of steps,
            which can be performed by LLMs with access to the servers or agents.
            """,
            servers=[],  # Planner doesn't need direct server access
            default_request_params=request_params,
            model=request_params.model if request_params else None,
        )

        self.planner = planner or llm_factory(agent=Agent(config=planner_config))

        self.plan_type: Literal["full", "iterative"] = plan_type
        self.server_registry = self.context.server_registry
        self.agents = {agent.name: agent for agent in available_agents or []}

    async def generate(
        self,
        message: str | MessageParamT | List[MessageParamT],
        request_params: RequestParams | None = None,
    ) -> List[MessageT]:
        """Request an LLM generation, which may run multiple iterations, and return the result"""
        params = self.get_request_params(request_params)
        objective = str(message)
        plan_result = await self.execute(objective=objective, request_params=params)

        return [plan_result.result]

    async def generate_str(
        self,
        message: str | MessageParamT | List[MessageParamT],
        request_params: RequestParams | None = None,
    ) -> str:
        """Request an LLM generation and return the string representation of the result"""
        params = self.get_request_params(request_params)

        result = await self.generate(
            message=message,
            request_params=params,
        )

        return str(result[0])

    async def generate_structured(
        self,
        message: str | MessageParamT | List[MessageParamT],
        response_model: Type[ModelT],
        request_params: RequestParams | None = None,
    ) -> ModelT:
        """Request a structured LLM generation and return the result as a Pydantic model."""
        params = self.get_request_params(request_params)

        result_str = await self.generate_str(message=message, request_params=params)

        structured_config = AgentConfig(
            name="Structured Output",
            instruction="Produce a structured output given a message",
            servers=[],  # No server access needed for structured output
        )

        llm = self.llm_factory(agent=Agent(config=structured_config))

        structured_result = await llm.generate_structured(
            message=result_str,
            response_model=response_model,
            request_params=params,
        )

        return structured_result

    async def execute(
        self, objective: str, request_params: RequestParams | None = None
    ) -> PlanResult:
        """Execute task with result chaining between steps"""
        iterations = 0

        params = self.get_request_params(request_params)

        plan_result = PlanResult(objective=objective, step_results=[])

        while iterations < params.max_iterations:
            if self.plan_type == "iterative":
                # Get next plan/step
                next_step = await self._get_next_step(
                    objective=objective, plan_result=plan_result, request_params=params
                )
                logger.debug(f"Iteration {iterations}: Iterative plan:", data=next_step)
                plan = Plan(steps=[next_step], is_complete=next_step.is_complete)
            elif self.plan_type == "full":
                plan = await self._get_full_plan(
                    objective=objective, plan_result=plan_result, request_params=params
                )
                logger.debug(f"Iteration {iterations}: Full Plan:", data=plan)
            else:
                raise ValueError(f"Invalid plan type {self.plan_type}")

            plan_result.plan = plan

            if plan.is_complete:
                # Only mark as complete if we have actually executed some steps
                if len(plan_result.step_results) > 0:
                    plan_result.is_complete = True

                    # Synthesize final result into a single message
                    synthesis_prompt = SYNTHESIZE_PLAN_PROMPT_TEMPLATE.format(
                        plan_result=format_plan_result(plan_result)
                    )

                    plan_result.result = await self.planner.generate_str(
                        message=synthesis_prompt,
                        request_params=params.model_copy(update={"max_iterations": 1}),
                    )

                    return plan_result
                else:
                    # Don't allow completion without executing steps
                    plan.is_complete = False

            # Execute each step, collecting results
            # Note that in iterative mode this will only be a single step
            for step in plan.steps:
                step_result = await self._execute_step(
                    step=step,
                    previous_result=plan_result,
                    request_params=params,
                )

                plan_result.add_step_result(step_result)

                plan_result.add_step_result(step_result)

            logger.debug(
                f"Iteration {iterations}: Intermediate plan result:", data=plan_result
            )
            iterations += 1

        raise RuntimeError(
            f"Task failed to complete in {params.max_iterations} iterations"
        )

    async def _execute_step(
        self,
        step: Step,
        previous_result: PlanResult,
        request_params: RequestParams | None = None,
    ) -> StepResult:
        """Execute a step's subtasks in parallel and synthesize results"""
        params = self.get_request_params(request_params)

        step_result = StepResult(step=step, task_results=[])
        context = format_plan_result(previous_result)

        # Prepare tasks and LLMs
        task_llms = []
        async with contextlib.AsyncExitStack() as stack:
            for task in step.tasks:
                agent = self.agents.get(task.agent)
                if not agent:
                    raise ValueError(f"No agent found matching {task.agent}")

                if isinstance(agent, AugmentedLLM):
                    llm = agent
                else:
                    # Use existing LLM if agent has one
                    if hasattr(agent, "_llm") and agent._llm:
                        llm = agent._llm
                    else:
                        # Only create new context if needed
                        ctx_agent = await stack.enter_async_context(agent)
                        # Create factory with agent's own configuration
                        agent_factory = ModelFactory.create_factory(
                            model_string=agent.config.model,
                            request_params=agent.config.default_request_params,
                        )
                        llm = await ctx_agent.attach_llm(agent_factory)

                task_llms.append((task, llm))

            # Execute all tasks within the same context
            futures = []
            for task, llm in task_llms:
                task_description = TASK_PROMPT_TEMPLATE.format(
                    objective=previous_result.objective,
                    task=task.description,
                    context=context,
                )
                # Get the agent's config for task execution
                agent = self.agents.get(task.agent)
                task_params = (
                    agent.config.default_request_params
                    if hasattr(agent, "config")
                    else params
                )
                futures.append(
                    llm.generate_str(
                        message=task_description, request_params=task_params
                    )
                )

            # Wait for all tasks, including any tool calls they make
            results = await self.executor.execute(*futures)

            # Process results while contexts are still active
            for (task, _), result in zip(task_llms, results):
                step_result.add_task_result(
                    TaskWithResult(**task.model_dump(), result=str(result))
                )

            # Format final result while contexts are still active
            step_result.result = format_step_result(step_result)

        return step_result

    async def _get_full_plan(
        self,
        objective: str,
        plan_result: PlanResult,
        request_params: RequestParams | None = None,
    ) -> Plan:
        """Generate full plan considering previous results"""
        params = self.get_request_params(request_params)
        params = params.model_copy(update={"use_history": False})

        agents = "\n".join(
            [
                f"{idx}. {self._format_agent_info(agent)}"
                for idx, agent in enumerate(self.agents, 1)
            ]
        )

        prompt = FULL_PLAN_PROMPT_TEMPLATE.format(
            objective=objective,
            plan_result=format_plan_result(plan_result),
            agents=agents,
        )

        plan = await self.planner.generate_structured(
            message=prompt,
            response_model=Plan,
            request_params=params,
        )

        return plan

    async def _get_next_step(
        self,
        objective: str,
        plan_result: PlanResult,
        request_params: RequestParams | None = None,
    ) -> NextStep:
        """Generate just the next needed step"""
        params = self.get_request_params(request_params)
        params = params.model_copy(update={"use_history": False})

        agents = "\n".join(
            [
                f"{idx}. {self._format_agent_info(agent)}"
                for idx, agent in enumerate(self.agents, 1)
            ]
        )

        prompt = ITERATIVE_PLAN_PROMPT_TEMPLATE.format(
            objective=objective,
            plan_result=format_plan_result(plan_result),
            agents=agents,
        )

        next_step = await self.planner.generate_structured(
            message=prompt,
            response_model=NextStep,
            request_params=params,
        )
        return next_step

    def _format_server_info(self, server_name: str) -> str:
        """Format server information for display to planners"""
        server_config = self.server_registry.get_server_config(server_name)
        server_str = f"Server Name: {server_name}"
        if not server_config:
            return server_str

        description = server_config.description
        if description:
            server_str = f"{server_str}\nDescription: {description}"

        return server_str

    def _format_agent_info(self, agent_name: str) -> str:
        """Format Agent information for display to planners"""
        agent = self.agents.get(agent_name)
        if not agent:
            return ""

        servers = "\n".join(
            [
                f"- {self._format_server_info(server_name)}"
                for server_name in agent.server_names
            ]
        )

        return f"Agent Name: {agent.name}\nDescription: {agent.instruction}\nServers in Agent: {servers}"
