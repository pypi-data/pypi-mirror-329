#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import json
import os
import tempfile
from rich.console import Console

console = Console()

def get_agent_dir() -> Path:
    """Get the browser-agent directory path."""
    # Get the path to the ai_kit package
    package_root = Path(__file__).parent.parent
    return package_root / "browser-agent"

def generate_ts_script(instruction: str) -> str:
    """Generate a TypeScript script for the given instruction."""
    # Escape any quotes in the instruction
    safe_instruction = instruction.replace('"', '\\"')
    
    return '''
import { Page, BrowserContext, Stagehand, ConstructorParams } from "@browserbasehq/stagehand";
import { z } from "zod";
import dotenv from "dotenv";

dotenv.config();

// Inline config
const StagehandConfig: ConstructorParams = {
    env: "LOCAL",
    apiKey: process.env.BROWSERBASE_API_KEY,
    projectId: process.env.BROWSERBASE_PROJECT_ID,
    debugDom: undefined,
    headless: false,
    domSettleTimeoutMs: 30_000,
    browserbaseSessionCreateParams: {
        projectId: process.env.BROWSERBASE_PROJECT_ID!,
    },
    modelName: "claude-3-5-sonnet-20241022",
    modelClientOptions: {
        apiKey: process.env.ANTHROPIC_API_KEY,
    },
};

function log(action: string) {
    console.log(JSON.stringify({
        timestamp: new Date().toISOString(),
        action,
        type: "LOG"
    }));
}

async function main() {
    const stagehand = new Stagehand(StagehandConfig);
    log("Initializing Stagehand");
    await stagehand.init();
    
    try {
        const page = stagehand.page;
        
        log("Navigating to Google");
        await page.goto("https://www.google.com");
        await page.waitForTimeout(1000); // Wait for page to settle
        
        log("Executing instruction: ''' + safe_instruction + '''");
        const results = await page.observe({
            instruction: "''' + safe_instruction + '''",
            onlyVisible: false,
            returnAction: true,
        });
        
        if (results && results.length > 0) {
            log(`Found ${results.length} possible elements, using first match`);
            await page.act(results[0]);
            
            log("Extracting results");
            const { content } = await page.extract({
                instruction: "Extract what happened after the action",
                schema: z.object({
                    content: z.string(),
                }),
            });
            
            console.log(JSON.stringify({
                type: "RESULT",
                success: true,
                content
            }));
        }
    } catch (error: any) {
        console.log(JSON.stringify({ 
            type: "RESULT",
            success: false, 
            error: error.message 
        }));
    } finally {
        log("Closing browser");
        await stagehand.close();
    }
}

main().catch((error: any) => {
    console.log(JSON.stringify({ 
        type: "RESULT",
        success: false, 
        error: error.message 
    }));
    process.exit(1);
});
'''

def run_browser_test(instruction: str = "Click the Google search input box"):
    """Run a browser automation test with the given instruction."""
    agent_dir = get_agent_dir()
    
    # Ensure we're in the correct directory
    if not (agent_dir / "package.json").exists():
        console.print(f"[red]Error:[/] Could not find package.json in {agent_dir}")
        sys.exit(1)
        
    # Create a temporary TypeScript file
    with tempfile.NamedTemporaryFile(suffix='.ts', mode='w', delete=False) as tf:
        tf.write(generate_ts_script(instruction))
        temp_path = tf.name
    
    try:
        # Set up environment with NODE_PATH
        env = os.environ.copy()
        env['NODE_PATH'] = str(agent_dir / 'node_modules')
        
        # Run the TypeScript file using tsx (which is like ts-node but faster)
        console.print(f"🤖 Running browser task with instruction: {instruction}")
        console.print("=" * 50)
        
        result = subprocess.run(
            ['npx', 'tsx', temp_path],
            cwd=agent_dir,  # Run from the browser-agent directory
            env=env,
            capture_output=True,
            text=True
        )
        
        # Parse output lines
        lines = result.stdout.splitlines()
        logs = []
        final_result = None
        
        for line in lines:
            try:
                data = json.loads(line)
                if data.get('type') == 'LOG':
                    logs.append(data)
                elif data.get('type') == 'RESULT':
                    final_result = data
            except json.JSONDecodeError:
                continue
        
        # Print logs in a nice format
        console.print("\n📝 Action Log:")
        console.print("-" * 13)
        for log in logs:
            console.print(f"{log['timestamp']}: {log['action']}")
        
        console.print("\n🎯 Final Result:")
        console.print("-" * 15)
        console.print(json.dumps(final_result, indent=2))
        
        if final_result and final_result.get('success'):
            console.print("\n[green]✓ Test completed successfully![/]")
        else:
            console.print("\n[red]✗ Test failed![/]")
            if final_result and 'error' in final_result:
                console.print(f"Error: {final_result['error']}")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error:[/] Failed to run TypeScript: {e}")
        console.print("\nStderr:")
        console.print(e.stderr)
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        sys.exit(1)
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)

if __name__ == "__main__":
    # Get instruction from command line argument or use default
    instruction = sys.argv[1] if len(sys.argv) > 1 else "Click the Google search input box"
    run_browser_test(instruction) 