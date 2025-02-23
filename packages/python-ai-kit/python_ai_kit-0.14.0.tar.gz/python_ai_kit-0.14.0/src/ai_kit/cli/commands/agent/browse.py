import inspect
from langchain_anthropic import ChatAnthropic
from browser_use import Agent, BrowserConfig, Browser, Controller, SystemPrompt
from browser_use.browser.views import BrowserState
from browser_use.agent.views import AgentOutput
from dotenv import load_dotenv
from rich.console import Console
import json
from typing import Any
import asyncio
import os
from ai_kit.shared_console import shared_console

load_dotenv()

# https://docs.browser-use.com/development/telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "false"

def live_logging_callback(state: BrowserState, model_output: AgentOutput, step_number: int, *args: Any, **kwargs: Any) -> None:
    # Log the main parameters
    shared_console.print("[yellow]Main Parameters:[/yellow]")
    shared_console.print(f"[cyan]step_number:[/cyan] {step_number}")
    shared_console.print(f"[cyan]state:[/cyan] BrowserState object - current URL: {state.url}")
    
    # Detailed model_output logging
    shared_console.print("\n[yellow]Model Output Details:[/yellow]")
    if model_output:
        # Log current state (AgentBrain)
        shared_console.print("[cyan]Current State (AgentBrain):[/cyan]")
        shared_console.print(f"  [magenta]Evaluation:[/magenta] {model_output.current_state.evaluation_previous_goal}")
        shared_console.print(f"  [magenta]Memory:[/magenta] {model_output.current_state.memory}")
        shared_console.print(f"  [magenta]Next Goal:[/magenta] {model_output.current_state.next_goal}")
        shared_console.print(f"  [magenta]Page Summary:[/magenta] {model_output.current_state.page_summary}")
        
        # Log actions
        shared_console.print("\n[cyan]Actions:[/cyan]")
        for i, action in enumerate(model_output.action, 1):
            action_dict = action.model_dump(exclude_unset=True)
            shared_console.print(f"  [magenta]Action {i}:[/magenta] {json.dumps(action_dict, indent=2)}")
    
    # Log any additional positional args
    if args:
        shared_console.print("\n[yellow]Additional Positional Args:[/yellow]")
        for i, arg in enumerate(args):
            shared_console.print(f"[cyan]arg {i}:[/cyan] {arg.__class__.__name__} - {str(arg)}")
    
    # Log any keyword args
    if kwargs:
        shared_console.print("\n[yellow]Keyword Args:[/yellow]")
        for key, value in kwargs.items():
            shared_console.print(f"[cyan]{key}:[/cyan] {value.__class__.__name__} - {str(value)}")
    
    # Extract and log useful details from state and model_output
    live_message = f"Step {step_number}: Currently at {state.url} - title: {state.title}"
    if model_output and hasattr(model_output, 'current_state'):
        live_message += f"\nNext goal: {model_output.current_state.next_goal}"
    
    shared_console.print(f"\n[blue]{live_message}[/blue]")

class CustomSystemPrompt(SystemPrompt):
    def important_rules(self):
        existing_rules = super().important_rules()
        # new_rules = """You are a helpful assistant that browses the web for information."""
        return existing_rules


async def browse_command(instruction: str, headless: bool = False):
    llm = ChatAnthropic(model="claude-3-5-sonnet-latest")
    config = BrowserConfig(
        # chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        headless=headless,
    )

    browser = Browser(config=config)
    controller = Controller()
    agent = Agent(
        task=instruction,
        use_vision=False,
        llm=llm,
        browser=browser,
        controller=controller,
        system_prompt_class=CustomSystemPrompt,
        register_new_step_callback=live_logging_callback,
        generate_gif=False,
    )
    result = await agent.run()
    shared_console.print("[bold blue]Final Result:[/bold blue]")
    shared_console.print(result.final_result())