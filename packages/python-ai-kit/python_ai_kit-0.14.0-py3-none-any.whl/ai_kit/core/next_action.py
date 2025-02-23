from ai_kit.core.router import Router, RouteRegistry, RouteDefinition
from ai_kit.cli.registry import registry_instance

ROUTER_SYSTEM_PROMPT = """
You are a helpful assistant that routes next actions to an AI agent based on a task.

When to use what:

1. We need external information (past knowledge cutoff, current event, specific data, updated documentation, etc.), and we dont already have urls
    1. web search
2. We need external information and its too complex for search/fetch
    1. browser agent
3. We need to save documentation to refer back to later
    1. web crawl
4. We dont need any external information, we can go ahead and complete the task
    1. finished
"""

class NextActionRouter:
    def __init__(self):
        registry = self._register_routes()
        self.router = Router(registry, system_prompt=ROUTER_SYSTEM_PROMPT, model="gemini-2.0-flash")

    def _register_routes(self) -> RouteRegistry:
        registry = RouteRegistry()
        COMMANDS_TO_IGNORE = ["think", "help", "list", "status", "init", "version"]
        # Register all command
        for cmd in registry_instance.commands:
            if cmd["name"] in COMMANDS_TO_IGNORE:
                continue
            registry.register(
                RouteDefinition(
                    name=cmd["name"], description=cmd["description"]
                )
            )

        registry.register(
            RouteDefinition(
                name="finished", description="We dont need to execute any more commands, we can go ahead and complete the task."
            )
        )
        return registry

    def route(self, prompt: str, thought_result: str) -> str:
        router_prompt = f"""
        Here is the original prompt: 
        {prompt}

        Here is the thought stream we got from our reasoning model:
        {thought_result}

        Suggest a follow up action.
        {ROUTER_SYSTEM_PROMPT}
        """
        return self.router.route(router_prompt)