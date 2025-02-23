from ai_kit.core.llms.google_genai_client import GoogleGenAI
from ai_kit.shared_console import shared_console
from ai_kit.cli.registry import registry_instance
from ai_kit.utils.fs import load_system_prompt, package_root

PACKAGE_ROOT = package_root()
USER_AGENT_RULES = load_system_prompt(
    f"{PACKAGE_ROOT}/system_prompts/cursorrules/agent.mdc"
)
COMMAND_REGISTRY_PROMPT = registry_instance.markdown_prompt

SYSTEM_PROMPT = f"""
You are a helpful assistant that recommends next steps to an AI agent.

Here are the commands available to you:
{COMMAND_REGISTRY_PROMPT}

Here are the users instructions about those tools:
{USER_AGENT_RULES}

NOTE: You are automatically triggered after running the "think" command, so you should never recommend the "think" command again unless it is for a related topic but not the original task itself.

Your job is to recommend "next steps" to the AI agent based on the command descriptions. For example, if the user is asking about something that requires external informaiton, you might recommend a web search.

Your recommendations should be in first person like this:
- "I think I should do a web search for updated docs for this package"
- "I should spawn a browser agent to figure this out, since its past my knowledge cutoff and is too complex for search/fetch"
- "I should crawl these docs to a local folder so I can read them later"
- "I think I'm ready to complete the task."
"""


class Recommender:
    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model = model
        self.client = GoogleGenAI(model=model)

    async def recommend(self, task: str) -> str:
        response = await self.client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": task},
            ]
        )
        shared_console.print(f"[bold green]<next_action>")
        shared_console.print(response["choices"][0]["message"]["content"])
        shared_console.print(f"[bold green]</next_action>")