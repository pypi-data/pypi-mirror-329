from time import perf_counter
from ai_kit.core.llms.client import Client
from typing import List, Dict
from ai_kit.core.router import Router, RouteRegistry, RouteDefinition
from ai_kit.utils import print_stream
from ai_kit.utils.fs import package_root, load_system_prompt
from ai_kit.shared_console import shared_console
from ai_kit.core.prompt_loader import PromptLoader
from ai_kit.config.client_config import ClientFactory

# Constants
PACKAGE_ROOT = package_root()
AGENT_RULES_PATH = f"{PACKAGE_ROOT}/system_prompts/cursorrules/agent.mdc"

# This is an extra system prompt we're passing for steerability.
USER_ROUTER_SYSTEM_PROMPT = """
Your job is to route between three options:

# Nothink
For simple requests that don't require any thinking. This includes conversaion, simple math and coding tasks.

# Think
For most tasks, general coding tasks, and tasks that don't require deep thinking. This includes general coding tasks, tasks that are procedurally complex, and tasks that don't require deep reasoning. Use this most of the time

# Deepthink
For advanced reasoning, highly advanced coding, and tasks requiring deep analysis. This includes complex coding tasks across a codebase, reasoning, and complex problem solving. This should be used only for the most complex tasks like difficult debugging tasks, difficult code generation tasks, and difficult reasoning tasks. Only use this for the most complex tasks.
"""

USER_THINKING_SYSTEM_PROMPT = f"""
You are a helpful assistant that can think deeply about a problem and solve it.

{load_system_prompt(AGENT_RULES_PATH)}
"""  # injecting the agent rules as a system prompt

class ThinkHandler:
    def __init__(
        self,
        think_model: str = "r1-70b",
        deepthink_model: str = "r1",
    ):
        self.think_client = ClientFactory.get_client_by_model(think_model)
        self.deepthink_client = ClientFactory.get_client_by_model(deepthink_model)
        self.router = Router(
            route_registry=self._register_routes(),
            model="gemini-2.0-flash",
            system_prompt=USER_ROUTER_SYSTEM_PROMPT,
        )
        self.agent_rules = load_system_prompt(AGENT_RULES_PATH)

    def _register_routes(self) -> RouteRegistry:
        """Setup available routes with their conditions."""
        registry = RouteRegistry()
        registry.register(
            RouteDefinition(
                name="deepthink",
                description="Advanced reasoning, highly advanced coding, and tasks requiring deep analysis.",
            )
        )

        registry.register(
            RouteDefinition(
                name="think",
                description="Most tasks, general coding tasks, and tasks that don't require deep thinking.",
            )
        )

        registry.register(
            RouteDefinition(
                name="nothink",
                description="Extremely simple conversation that doesn't need any thinking..",
            )
        )

        registry.register(
            RouteDefinition(
                name="fallback",
                description="Fallback route if no other route is a good match.",
            )
        )
        return registry

    async def handle_think(self, prompt: str):
        """Call the router to determine the best route for the prompt."""
        s = perf_counter()
        with shared_console.status("[bold yellow]Routing..."):
            decision = self.router.route(prompt)
            e = perf_counter()
        shared_console.print(
            f"[yellow]Routed to: [bold blue]{decision.route}[/bold blue] in [bold yellow]{e - s:0.2f}[/bold yellow] seconds. [/yellow]"
        )
        thought_result = None
        if decision.route == "deepthink":
            thought_result = await self._handle_deepthink(prompt)
        elif decision.route == "think":
            thought_result = await self._handle_think(prompt)
        elif decision.route == "nothink":
            self._handle_nothink()
            thought_result = "no thinking required for this task"
        else:  # fallback
            await self._handle_think()
            thought_result = "no thinking required for this task"

    async def get_messages(self, prompt: str) -> List[Dict[str, str]]:
        prompt_loader = PromptLoader()
        processed_prompt = await prompt_loader.load(prompt)
        user_prompt = f"""
        Here are some system instructions: 
        {USER_THINKING_SYSTEM_PROMPT}

        Here is the user's prompt. Use the tools available to you to solve the problem.
        {processed_prompt}
        """
        messages = [
            {"role": "system", "content": user_prompt},
            {"role": "user", "content": processed_prompt},
        ]
        return messages

    async def _handle_deepthink(self, prompt: str) -> str:
        """Handle requests requiring deep thinking."""
        s = perf_counter()
        with shared_console.status("[bold green]Thinking Deeply..."):
            shared_console.print(
                f"Calling [bold blue]{self.deepthink_client.model}[/bold blue]..."
            )
            messages = await self.get_messages(prompt)
            response = await self.deepthink_client.reasoning_completion(
                messages=messages,
                stream=True,
                thoughts_only=True,
            )
            shared_console.print("\n[bold]Thinking Process:[/bold]")
            await print_stream(response)
        e = perf_counter()
        shared_console.print(f"[yellow]Thought for {e - s:0.2f} seconds.[/yellow]")

    async def _handle_think(self, prompt: str) -> str:
        """Handle requests requiring deep thinking."""
        s = perf_counter()
        with shared_console.status("[bold green]Thinking..."):
            messages = await self.get_messages(prompt)
            response = await self.think_client.reasoning_completion(
                messages=messages,
                stream=True,
                thoughts_only=True,
            )
            thought_result = await print_stream(response)
        e = perf_counter()
        shared_console.print(f"[yellow]Thought for {e - s:0.2f} seconds.[/yellow]")
        return thought_result

    def _handle_nothink(self):
        """Handle simple requests that don't require deep thinking."""
        shared_console.print(f"I don't need to think about this.")


async def think_command(prompt: str, think_model: str, deepthink_model: str):
    """CLI entry point for the think command."""
    handler = ThinkHandler(
        think_model=think_model,
        deepthink_model=deepthink_model,
    )
    await handler.handle_think(prompt)
