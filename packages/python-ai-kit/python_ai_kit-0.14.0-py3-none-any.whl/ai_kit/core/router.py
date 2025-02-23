from pydantic import BaseModel, Field
from typing import Dict, Optional
import logging
from ai_kit.utils.fs import package_root, load_system_prompt
from ai_kit.config.client_config import ClientFactory
from ai_kit.core.llms.client import Client

logger = logging.getLogger(__name__)

PACKAGE_ROOT = package_root()
ROUTER_PROMPT_PATH = f"{PACKAGE_ROOT}/system_prompts/router.md"
class RouteDefinition(BaseModel):
    """
    Defines an available route:
    - name (unique identifier)
    - description (what the route is used for)
    """

    name: str
    description: str

class RouteRegistry:
    """
    Manages a collection of RouteDefinition objects.
    You can register new routes and build a prompt snippet.
    """

    def __init__(self):
        self._routes: Dict[str, RouteDefinition] = {}

    def register(self, route: RouteDefinition):
        """
        Register a new route definition by name.
        """
        if route.name in self._routes:
            logger.warning(f"Overwriting an existing route: {route.name}")
        self._routes[route.name] = route

    def get_route(self, name: str) -> Optional[RouteDefinition]:
        """
        Retrieve a route definition by name (or None if not found).
        """
        return self._routes.get(name)

    def routes_prompt_snippet(self) -> str:
        """
        Create a text snippet enumerating available routes in a user-friendly way.
        This can be inserted into the system prompt so the LLM can choose accurately.
        """
        # Example snippet listing each route with its description
        lines = ["Choose EXACTLY one of these routes by name:\n"]
        for route in self._routes.values():
            lines.append(f'Name: "{route.name}" - {route.description}')
        return "\n".join(lines)

    @property
    def route_names(self):
        return list(self._routes.keys())

class RoutingDecision(BaseModel):
    """
    The structured output from the model indicating which route to use.
    """

    route: str = Field(..., description="The chosen route name")
    confidence: float = Field(..., description="Confidence from 0.0 to 1.0")
    reasoning: str = Field(..., description="Brief explanation of the choice")

class Router:
    def __init__(
        self, route_registry: RouteRegistry, model: Optional[str] = None, system_prompt: Optional[str] = None
    ):
        """
        :param route_registry: The registry containing all valid routes.
        :param model: Optional model name. If not provided, load from config.json.
        """
        self.registry = route_registry
        self.user_system_prompt = system_prompt
        self.model = model
        self.client: Client = ClientFactory.get_client_by_model(model)

    def get_system_prompt(self) -> str:
        """
        Build a system prompt enumerating available routes with instructions.
        """
        # Insert the route list snippet
        route_list = self.registry.routes_prompt_snippet()
        system_prompt = load_system_prompt(ROUTER_PROMPT_PATH) # ! This is the base router prompt for every instance of router
        assert system_prompt is not None and system_prompt.strip() != ""
        with_route_list = system_prompt.format(route_list=route_list) # ! Inject route list

        if self.user_system_prompt: # ! Add user system prompt if we have it
            output = with_route_list + "\n\n" + "Extra Instructions:\n" + self.user_system_prompt
        else:
            output = with_route_list

        return output

    def route(self, query: str) -> RoutingDecision:
        """
        Perform the routing by:
        1. Constructing the prompt (with available routes).
        2. Asking the LLM to pick a route using structured output.
        3. Validating and returning the chosen route + confidence, reasoning.
        4. Optional fallback logic if route is unrecognized or confidence is too low.
        """
        system_prompt = self.get_system_prompt()
        # Debug here.
        # print("GOT SYSTEM PROMPT FOR ROUTER: ", system_prompt)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": system_prompt + "\n\n" + query},
        ]
        # Call the LLM client with a structured output request
        decision: RoutingDecision = self.client.structured_output_completion(
            messages=messages,
            schema=RoutingDecision,
        )

        # Fallback check: if the chosen route is not in the registry, or low confidence
        if decision.route not in self.registry.route_names:
            logger.warning(
                f"Unrecognized route chosen: {decision.route}. Falling back to default."
            )
            decision.route = "some_other_route"
            decision.reasoning += " [FELL BACK due to invalid route]"
            decision.confidence = 0.5

        elif decision.confidence < 0.3:
            logger.warning(f"Low confidence route chosen: {decision.route}.")
            # Decide if you want a fallback
            # or trust the LLM's output anyway
            # For demonstration, let's keep it
            # but note the low confidence in logs.
            pass

        return decision
