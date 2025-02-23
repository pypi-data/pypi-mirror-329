Introduction - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedIntroductionDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedIntroduction
============Stagehand is the AI interface to the internet.Stagehand is the easiest way to build browser automations. It is completely interoperable with Playwright and has seamless integration with Browserbase.It offers three simple AI APIs (`act`, `extract`, and `observe`) on top of the base Playwright `Page` class that provide the building blocks for web automation via natural language.Anything that can be done in a browser can be done with Stagehand. Think about stuff like:1. Log into Amazon, search for AirPods, and buy the most relevant product
2. Go to Hacker News and extract the top stories of the day
3. Go to Doordash, find the cheapest pad thai, and order it to your houseThese automations can be built with Playwright, but it can be very cumbersome to write the code, and it will be very vulnerable to minor changes in the UI.Stagehand’s AI, especially when combined with Browserbase’s stealth mode, make it easy to write durable code and bypass bot detection and captchas.​Lights, Camera, `act()`
------------------------Let’s get you started with Stagehand.Quickstart
----------Build browser automations in no time.How Stagehand Works
-------------------Go behind the scenes with Stagehand.​FAQ
----### ​What is Stagehand?Stagehand is the AI-powered successor to Playwright, offering three simple APIs (`act`, `extract`, and `observe`) that provide the building blocks for web automation via natural language.The goal of Stagehand is to provide a lightweight model-agnostic framework, without overly complex abstractions. It’s not going to order you a pizza, but it will help you execute steps like `"click the order button"`.Each Stagehand function takes in an atomic instruction, such as `act("click the login button")` or `extract("find the price of pad thai")`, generates the appropriate Playwright code to accomplish that instruction, and executes it.### ​What is a web agent?A web agent is an AI agent that aims to browse the web like a human. They can navigate the web, interact with web pages, and perform tasks. You could imagine something like telling a bot “here’s my credit card, order me pad thai” and having it do that entirely autonomously.### ​Is Stagehand a web agent?No, Stagehand is not a web agent. It is a set of tools that enables and empowers web agents and developers building them. A web agent could take an instruction like “order me pad thai” and use Stagehand to navigate to the restaurant’s website, find the menu, and order the food.### ​What are some best practices for using Stagehand?Stagehand is something like Github Copilot, but for web automation. It’s not a good idea to ask it to write your entire application, but it’s great for quickly generating self-healing Playwright code to accomplish specific tasks.Therefore, instructions should be atomic to increase reliability, and step planning should be handled by the higher level agent. You can use `observe()` to get a suggested list of actions that can be taken on the current page, and then use those to ground your step planning prompts.### ​Who built Stagehand?Stagehand is open source and maintained by the Browserbase team. We envision a world in which web agents are built with Stagehand on Browserbase.We believe that by enabling more developers to build reliable web automations, we’ll expand the market of developers who benefit from our headless browser infrastructure. This is the framework that we wished we had while tinkering on our own applications, and we’re excited to share it with you.If you’ve made it this far, hi mom!QuickstartxgithublinkedinPowered by MintlifyOn this page* Lights, Camera, act()
* FAQ
* What is Stagehand?
* What is a web agent?
* Is Stagehand a web agent?
* What are some best practices for using Stagehand?
* Who built Stagehand?

Best Practices - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedBest PracticesDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedBest Practices
==============How to get the most out of Stagehand​Prompting Tips
---------------Prompting Stagehand is more literal and atomic than other higher level frameworks, including agentic frameworks. Here are some guidelines to help you craft effective prompts:### ​Do**Use `act()` as a fallback when Playwright fails**```
try {
    // Wait for search button and click it
    const quickStartSelector = `#content-area > div.relative.mt-8.prose.prose-gray.dark\:prose-invert > div > a:nth-child(1)`;
    await page.waitForSelector(quickStartSelector);
    await page.locator(quickStartSelector).click();
    await page.waitForLoadState("networkidle");
} catch {
    // Use Stagehand as a fallback to get the job done
	console.log("Error occurred, falling back to Stagehand");
	await page.act({
		action: "Click the link to the quickstart",
	});
}```**Use specific and concise actions**```
await page.act({ action: "click the login button" });const productInfo = await page.extract({
  instruction: "find the red shoes",
  schema: z.object({
    productName: z.string(),
    price: z.number(),
  }),
});```**Break down complex tasks into smaller, atomic steps**Instead of combining actions:```
// Avoid this
await page.act({ action: "log in and purchase the first item" });```Split them into individual steps:```
await page.act({ action: "click the login button" });
// ...additional steps to log in...
await page.act({ action: "click on the first item" });
await page.act({ action: "click the purchase button" });```**Use `observe()` to get actionable suggestions from the current page**```
const actions = await page.observe();
console.log("Possible actions:", actions);// You can also use `observe()` with a custom prompt
const buttons = await page.observe({
	instruction: "find all the buttons on the page",
});```
### ​Don’t**Use broad or ambiguous instructions**```
// Too vague
await page.act({ action: "find something interesting on the page" });```**Combine multiple actions into one instruction**```
// Avoid combining actions
await page.act({ action: "fill out the form and submit it" });```**Expect Stagehand to perform high-level planning or reasoning**```
// Outside Stagehand's scope
await page.act({ action: "book the cheapest flight available" });```By following these guidelines, you’ll increase the reliability and effectiveness of your web automations with Stagehand. Remember, Stagehand excels at executing precise, well-defined actions so keeping your instructions atomic will lead to the best outcomes.We leave the agentic behavior to higher-level agentic systems which can use Stagehand as a tool.QuickstartHow Stagehand WorksxgithublinkedinPowered by MintlifyOn this page* Prompting Tips
* Do
* Don’t

Introduction - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedIntroductionDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedIntroduction
============Stagehand is the AI interface to the internet.Stagehand is the easiest way to build browser automations. It is completely interoperable with Playwright and has seamless integration with Browserbase.It offers three simple AI APIs (`act`, `extract`, and `observe`) on top of the base Playwright `Page` class that provide the building blocks for web automation via natural language.Anything that can be done in a browser can be done with Stagehand. Think about stuff like:1. Log into Amazon, search for AirPods, and buy the most relevant product
2. Go to Hacker News and extract the top stories of the day
3. Go to Doordash, find the cheapest pad thai, and order it to your houseThese automations can be built with Playwright, but it can be very cumbersome to write the code, and it will be very vulnerable to minor changes in the UI.Stagehand’s AI, especially when combined with Browserbase’s stealth mode, make it easy to write durable code and bypass bot detection and captchas.​Lights, Camera, `act()`
------------------------Let’s get you started with Stagehand.Quickstart
----------Build browser automations in no time.How Stagehand Works
-------------------Go behind the scenes with Stagehand.​FAQ
----### ​What is Stagehand?Stagehand is the AI-powered successor to Playwright, offering three simple APIs (`act`, `extract`, and `observe`) that provide the building blocks for web automation via natural language.The goal of Stagehand is to provide a lightweight model-agnostic framework, without overly complex abstractions. It’s not going to order you a pizza, but it will help you execute steps like `"click the order button"`.Each Stagehand function takes in an atomic instruction, such as `act("click the login button")` or `extract("find the price of pad thai")`, generates the appropriate Playwright code to accomplish that instruction, and executes it.### ​What is a web agent?A web agent is an AI agent that aims to browse the web like a human. They can navigate the web, interact with web pages, and perform tasks. You could imagine something like telling a bot “here’s my credit card, order me pad thai” and having it do that entirely autonomously.### ​Is Stagehand a web agent?No, Stagehand is not a web agent. It is a set of tools that enables and empowers web agents and developers building them. A web agent could take an instruction like “order me pad thai” and use Stagehand to navigate to the restaurant’s website, find the menu, and order the food.### ​What are some best practices for using Stagehand?Stagehand is something like Github Copilot, but for web automation. It’s not a good idea to ask it to write your entire application, but it’s great for quickly generating self-healing Playwright code to accomplish specific tasks.Therefore, instructions should be atomic to increase reliability, and step planning should be handled by the higher level agent. You can use `observe()` to get a suggested list of actions that can be taken on the current page, and then use those to ground your step planning prompts.### ​Who built Stagehand?Stagehand is open source and maintained by the Browserbase team. We envision a world in which web agents are built with Stagehand on Browserbase.We believe that by enabling more developers to build reliable web automations, we’ll expand the market of developers who benefit from our headless browser infrastructure. This is the framework that we wished we had while tinkering on our own applications, and we’re excited to share it with you.If you’ve made it this far, hi mom!QuickstartxgithublinkedinPowered by MintlifyOn this page* Lights, Camera, act()
* FAQ
* What is Stagehand?
* What is a web agent?
* Is Stagehand a web agent?
* What are some best practices for using Stagehand?
* Who built Stagehand?

Quickstart - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedQuickstartDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedQuickstart
==========Use create-browser-app to get started in 1 minute1PrerequisitesBefore you begin, you’ll need to install Node.js and NPM. We highly recommend using nvm to manage your Node.js versions, and running on Node version 20+.We highly recommend using the Node.js runtime environment to run Stagehand scripts, as opposed to newer alternatives like Deno or Bun.2Create a new projectYou can use npx to create a new project. You should have npx included with `npm`, the default package manager for Node.js.* npm
* pnpm
* yarn```
npx create-browser-app --example quickstart```To create a blank Stagehand project without the quickstart example, run:* npm
* pnpm
* yarn```
npx create-browser-app```This will create a new directory called `my-app`, and install the Stagehand package. It will ask you the following questions:```
✔ Select AI model to use: OpenAI GPT-4o
✔ Would you like to run locally or on Browserbase? Browserbase
✔ Enable DOM debugging features? Yes
✔ Enable prompt caching? Yes```
### Large Language ModelsIn addition, you’ll need either an OpenAI API Key or Anthropic API key. Stagehand allows you to choose between the following models:* OpenAI GPT-4o (Get API Key)
* Anthropic Claude 3.5 Sonnet (Get API Key)We also support GPT-4o-mini, but it is not recommended for production use.### BrowserbaseLastly, if you want access to advanced features like custom contexts, extensions, and captcha solving, you’ll need a Browserbase account. We give you 10 free sessions to get started. You can get your Project ID and API Key from the Browserbase dashboard.3Install dependencies and run the script* npm
* pnpm
* yarn```
cd my-app
npm install
npm run start```Use the package manager of your choice to install the dependencies. We also have a `postinstall` script that will automatically install the Playwright browser with `playwright install`.
Check out the Playbook
----------------------If you’re interested in seeing the source code for what’s created, you can check out the Browserbase Playbook.Check out the CLI repo
----------------------If you’re interested in the source code for the `create-browser-app` CLI, you can check out the CLI repo.IntroductionBest PracticesxgithublinkedinPowered by Mintlify

Examples and Guides - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedExamples and GuidesDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedExamples and Guides
===================Ready-to-run templates via create-browser-appCheck out the Playbook
----------------------We’ve created a Github repository with plenty of ready-to-run guides for Stagehand, including persistent contexts and deploying to Vercel.​Next.js + Vercel
-----------------Check out the Next.js + Vercel example to see how to build a Next.js app and one-click deploy it to Vercel.​Custom LLM Clients
-------------------```
# For Vercel AI SDK
npx create-browser-app --example custom-client-aisdk# For Ollama
npx create-browser-app --example custom-client-ollama```This example shows how to use a custom LLM client in Stagehand. We have working examples for Vercel AI SDK and Ollama. This helps you use your own LLM client in Stagehand if you don’t want to use 4o/Sonnet.This helps you connect to LLMs like DeepSeek, Llama, Perplexity, Groq, and more!​Persistent Contexts
--------------------```
npx create-browser-app --example persist-context```This example uses Browserbase’s context persistence to create a persistent context that can be used across multiple runs.This is really useful for automating on sites that require login, or for automating on sites that have a captcha. Once you’ve logged in, you can use the same context to automate on the same site without having to log in again.​Deploying to Vercel
--------------------```
npx create-browser-app --example deploy-vercel```This example creates a scaffolded Vercel function that can easily be deployed to Vercel with `npx vercel deploy`.It creates a `GET` endpoint at `/api/stagehand` that can be used to run Stagehand script in `index.ts`.Contribute to StagehandxgithublinkedinPowered by MintlifyOn this page* Next.js + Vercel
* Custom LLM Clients
* Persistent Contexts
* Deploying to Vercel

Contribute to Stagehand - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedContribute to StagehandDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedContribute to Stagehand
=======================Best practices for making a meaningful contribution to Stagehand​Codeowners and Subject-Matter Experts
======================================**Stagehand repo codeowners are Anirudh Kamath and Paul Klein.** Any contribution must be explicitly approved by a codeowner.Stagehand subject-matter experts are as follows:* **Sean McGuire** - general repo, but especially evals and `extract`
* **Navid Pour** - general repo, but especially `act`
* **Sameel Arif** - general repo
* **Filip Michalsky** - general repo and integrations like Langchain or Claude MCP
* **Miguel Gonzalez** - general repo and accessibility tree (a11y tree) implementationSpecial thanks to Jeremy Press (the OG) and all the contributors for your help in making Stagehand the best browser automation framework.***Please do not hesitate to reach out to anyone listed here in the public Slack channel***​Before you start
=================​General Workflow
-----------------Get listed as one of our beloved contributors!1. **Discuss your proposed contribution before starting.** Not doing this runs you the risk of entirely discarding something you put considerable time and effort into. You can DM Anirudh on Slack or book 30 minutes for a 1on1 call.
2. **Open a Pull Request.** Create a fork of this repository, and follow GitHub’s instructions to create a Pull Request. This allows our team to review your contribution and leave comments.
3. **Wait for Review**. We’ll do our best to get to your contribution as soon as possible. If it’s been 2-3 days and you have yet to receive any comments, DM Anirudh on Slack
4. **Merge into `evals` branch.** We don’t let external contributors run our CI via GitHub Actions to prevent spam and misuse. If your contribution passes an initial screen, we’ll run our evals on it
   
   1. By default, all PRs run the following tests that you can also run from the repo source:
      1. Lint (`npm run lint`) - Runs `prettier` and `eslint`. If this fails, you can most likely run `npm run format` to fix some simple linting errors.
      2. Build (`npm run build`) - Lints and builds TS → JS in `dist/` via `tsup`
      3. End-to-End (`npm run e2e`) - These are deterministic end-to-end Playwright tests to ensure the integrity of basic Playwright functionality of `stagehand.page` and `stagehand.context` as well as compatibility with the Browserbase API
      4. Combination (`npm run evals category combination`) - This runs AI-based end-to-end tests using combinations of `act`, `extract`, and `observe`
   2. If you’re changing anything about `act`, `extract`, or `observe` itself, we might also run specific act/extract/observe evals to ensure existing functionality doesn’t significantly drop.
5. **Cleanup and merge to main**. Once it’s in `evals`, unfortunately the original contributor can’t make any further changes. The internal Stagehand team will be responsible for cleaning up the code and bringing it into main.​Help make everyone’s lives easier
----------------------------------1. **Use draft PRs.** If your PR is a work in progress, please convert it to a draft (see below) while you’re working on it, and mark it for review/add reviewers when you’re ready. This helps us prevent clutter in the review queue.
2. **Provide a reproducible test plan.** Include an eval (preferred) or example. We can’t merge your PR if we can’t run anything that specifically highlights your contribution.
   
   1. Write a script in `evals/tasks` as `someTask.ts`
   2. Add your script to `evals.config.json` with default category `combination` (*or act/extract/observe if you’re* *only* *testing* *act/extract/observe*).
3. **Add a changeset.** Run `npx changeset` to add a changeset that will directly reflect in the `CHANGELOG` in the upcoming release.
   
   1. `patch` - no net new functionality to an end-user
   2. `minor` - some net new functionality to an end-user (new function parameter, new exposed type, etc.)
   3. `major` - you shouldn’t be committing a major change
How Stagehand WorksExamples and GuidesxgithublinkedinPowered by MintlifyOn this page* Codeowners and Subject-Matter Experts
* Before you start
* General Workflow
* Help make everyone’s lives easier

Stagehand SDK Reference - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceStagehand SDK ReferenceDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceStagehand SDK Reference
=======================View each method in the Stagehand SDK and learn how to use them.Configuration
-------------Configure Stagehand the way you want.Act
---Perform actions on the current page.Extract
-------Extract structured data from the page.Observe
-------Get candidate DOM elements for actions.Playwright InteroperabilityxgithublinkedinPowered by Mintlify

Introduction - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedIntroductionDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedIntroduction
============Stagehand is the AI interface to the internet.Stagehand is the easiest way to build browser automations. It is completely interoperable with Playwright and has seamless integration with Browserbase.It offers three simple AI APIs (`act`, `extract`, and `observe`) on top of the base Playwright `Page` class that provide the building blocks for web automation via natural language.Anything that can be done in a browser can be done with Stagehand. Think about stuff like:1. Log into Amazon, search for AirPods, and buy the most relevant product
2. Go to Hacker News and extract the top stories of the day
3. Go to Doordash, find the cheapest pad thai, and order it to your houseThese automations can be built with Playwright, but it can be very cumbersome to write the code, and it will be very vulnerable to minor changes in the UI.Stagehand’s AI, especially when combined with Browserbase’s stealth mode, make it easy to write durable code and bypass bot detection and captchas.​Lights, Camera, `act()`
------------------------Let’s get you started with Stagehand.Quickstart
----------Build browser automations in no time.How Stagehand Works
-------------------Go behind the scenes with Stagehand.​FAQ
----### ​What is Stagehand?Stagehand is the AI-powered successor to Playwright, offering three simple APIs (`act`, `extract`, and `observe`) that provide the building blocks for web automation via natural language.The goal of Stagehand is to provide a lightweight model-agnostic framework, without overly complex abstractions. It’s not going to order you a pizza, but it will help you execute steps like `"click the order button"`.Each Stagehand function takes in an atomic instruction, such as `act("click the login button")` or `extract("find the price of pad thai")`, generates the appropriate Playwright code to accomplish that instruction, and executes it.### ​What is a web agent?A web agent is an AI agent that aims to browse the web like a human. They can navigate the web, interact with web pages, and perform tasks. You could imagine something like telling a bot “here’s my credit card, order me pad thai” and having it do that entirely autonomously.### ​Is Stagehand a web agent?No, Stagehand is not a web agent. It is a set of tools that enables and empowers web agents and developers building them. A web agent could take an instruction like “order me pad thai” and use Stagehand to navigate to the restaurant’s website, find the menu, and order the food.### ​What are some best practices for using Stagehand?Stagehand is something like Github Copilot, but for web automation. It’s not a good idea to ask it to write your entire application, but it’s great for quickly generating self-healing Playwright code to accomplish specific tasks.Therefore, instructions should be atomic to increase reliability, and step planning should be handled by the higher level agent. You can use `observe()` to get a suggested list of actions that can be taken on the current page, and then use those to ground your step planning prompts.### ​Who built Stagehand?Stagehand is open source and maintained by the Browserbase team. We envision a world in which web agents are built with Stagehand on Browserbase.We believe that by enabling more developers to build reliable web automations, we’ll expand the market of developers who benefit from our headless browser infrastructure. This is the framework that we wished we had while tinkering on our own applications, and we’re excited to share it with you.If you’ve made it this far, hi mom!QuickstartxgithublinkedinPowered by MintlifyOn this page* Lights, Camera, act()
* FAQ
* What is Stagehand?
* What is a web agent?
* Is Stagehand a web agent?
* What are some best practices for using Stagehand?
* Who built Stagehand?

Langchain JS - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationIntegrationsLangchain JSDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Integrations* Langchain JS
* MCP Server
IntegrationsLangchain JS
============Integrate Stagehand with Langchain JSStagehand can be integrated into Langchain JS by wrapping Stagehand’s browser automation functionality with the `StagehandToolkit`.This toolkit provides specialized tools such as `navigate`, `act`, `extract`, and `observe`, all powered by Stagehand’s underlying capabilities.For more details on this integration and how to work with Langchain, see the official Langchain documentation.Below is a high-level overview to get started:​Installation
-------------Install the necessary packages:```
npm install @langchain/langgraph @langchain/community @langchain/core @browserbasehq/stagehand```​Create a Stagehand instance
----------------------------```
const stagehand = new Stagehand({
env: "LOCAL",
headless: false,
verbose: 2,
debugDom: true,
enableCaching: false,
});```​Generate a Stagehand Toolkit object
------------------------------------```
const stagehandToolkit = await StagehandToolkit.fromStagehand(stagehand);```​Use the tools
--------------* `stagehand_navigate`: Navigate to a specific URL.
* `stagehand_act`: Perform browser automation tasks like clicking buttons and typing in fields.
* `stagehand_extract`: Extract structured data from pages using Zod schemas.
* `stagehand_observe`: Investigate the DOM for possible actions or relevant elements.Example standalone usage:```
// Find the relevant tool
const navigateTool = stagehandToolkit.tools.find(
(t) => t.name === "stagehand_navigate");// Invoke it
await navigateTool.invoke("https://www.google.com");// Suppose you want to act on the page
const actionTool = stagehandToolkit.tools.find(
(t) => t.name === "stagehand_act");await actionTool.invoke('Search for "OpenAI"');// Observe the current page
const observeTool = stagehandToolkit.tools.find(
(t) => t.name === "stagehand_observe");const result = await observeTool.invoke(
"What actions can be performed on the current page?");console.log(JSON.parse(result));// Verification
const currentUrl = stagehand.page.url();
// e.g., ensure it contains "google.com/search"```​Remote Browsers (Browserbase)
------------------------------Instead of env: “LOCAL”, specify env: “BROWSERBASE” and pass in your Browserbase credentials through environment variables:
`BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID`​Using LangGraph Agents
-----------------------The `StagehandToolkit` can also be plugged into LangGraph’s existing agent system. This lets you orchestrate more complex flows by combining Stagehand’s tools with other Langchain tools.With the `StagehandToolkit`, you can quickly integrate natural-language-driven browser automation into workflows supported by Langchain. This enables use cases such as:* Searching, extracting, and summarizing data from websites
* Automating login flows
* Navigating or clicking through forms based on instructions from a larger chain of agentsConsult Stagehand’s and Langchain’s official references for troubleshooting and advanced integrations or reach out to us on Slack.MCP ServerxgithublinkedinPowered by MintlifyOn this page* Installation
* Create a Stagehand instance
* Generate a Stagehand Toolkit object
* Use the tools
* Remote Browsers (Browserbase)
* Using LangGraph Agents

How Stagehand Works - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedHow Stagehand WorksDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedHow Stagehand Works
===================Go behind the scenes​How It Works
-------------The SDK has two major phases:1. Processing the DOM (including chunking - *see below*).
2. Taking LLM powered actions based on the current state of the DOM.### ​DOM processingStagehand uses a combination of techniques to prepare the DOM.The DOM Processing steps look as follows:1. Via Playwright, inject a script into the DOM accessible by the SDK that can run processing.
2. Crawl the DOM and create a list of candidate elements.
   * Candidate elements are either leaf elements (DOM elements that contain actual user facing substance), or are interactive elements.
   * Interactive elements are determined by a combination of roles and HTML tags.
3. Candidate elements that are not active, visible, or at the top of the DOM are discarded.
   * The LLM should only receive elements it can faithfully act on on behalf of the agent/user.
4. For each candidate element, an xPath is generated. This guarantees that if this element is picked by the LLM, we’ll be able to reliably target it.
5. Return both the list of candidate elements, as well as the map of elements to xPath selectors across the browser back to the SDK, to be analyzed by the LLM.#### ​ChunkingWhile LLMs will continue to increase context window length and reduce latency, giving any reasoning system less stuff to think about should make it more reliable. As a result, DOM processing is done in chunks in order to keep the context small per inference call. In order to chunk, the SDK considers a candidate element that starts in a section of the viewport to be a part of that chunk. In the future, padding will be added to ensure that an individual chunk does not lack relevant context. See this diagram for how it looks:### ​VisionThe `act()` and `observe()` methods can take a `useVision` flag. If this is set to `true`, the LLM will be provided with a annotated screenshot of the current page to identify which elements to act on. This is useful for complex DOMs that the LLM has a hard time reasoning about, even after processing and chunking. By default, this flag is set to `"fallback"`, which means that if the LLM fails to successfully identify a single element, Stagehand will retry the attempt using vision.### ​LLM analysisNow we have a list of candidate elements and a way to select them. We can present those elements with additional context to the LLM for extraction or action. While untested on a large scale, presenting a “numbered list of elements” guides the model to not treat the context as a full DOM, but as a list of related but independent elements to operate on.In the case of action, we ask the LLM to write a playwright method in order to do the correct thing. In our limited testing, playwright syntax is much more effective than relying on built in javascript APIs, possibly due to tokenization.Lastly, we use the LLM to write future instructions to itself to help manage its progress and goals when operating across chunks.### ​Stagehand vs PlaywrightBelow is an example of how to extract a list of companies from the AI Grant website using both Stagehand and Playwright.Best PracticesContribute to StagehandxgithublinkedinPowered by MintlifyOn this page* How It Works
* DOM processing
* Chunking
* Vision
* LLM analysis
* Stagehand vs Playwright

Configuration - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceConfigurationDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceConfiguration
=============How to configure Stagehand​Stagehand constructor
----------------------```
// Basic usage
// Defaults to Browserbase; if no API key is provided, it will default to LOCAL
// Default model is gpt-4o
const stagehand = new Stagehand();// Custom configuration
const stagehand = new Stagehand({
	env: "LOCAL",
	verbose: 1,
	headless: true,
	enableCaching: true,
	logger: (logLine: LogLine) => {
		console.log(`[${logLine.category}] ${logLine.message}`);
	},
});// Resume existing Browserbase session
const stagehand = new Stagehand({
	env: "BROWSERBASE",
	browserbaseSessionID: "existing-session-id",
});```This constructor is used to create an instance of Stagehand.### ​**Arguments:** `ConstructorParams`​env'LOCAL' | 'BROWSERBASE'Defaults to `'BROWSERBASE'`
​apiKeystringYour Browserbase API key. Defaults to `BROWSERBASE_API_KEY` environment variable
​projectIdstringYour Browserbase project ID. Defaults to `BROWSERBASE_PROJECT_ID` environment variable
​browserBaseSessionCreateParamsSessionCreateParamsConfiguration options for creating new Browserbase sessions
​browserbaseSessionIDstringID of an existing Browserbase session to resume
​modelNameAvailableModelSpecifying the default language model to use
​modelClientOptionsobjectConfiguration options for the language model client (i.e. `apiKey`)
​enableCachingbooleanEnables caching of LLM responses. When set to `true`, the LLM requests will be cached on disk and reused for identical requests. Defaults to `false`
​headlessbooleanDetermines if the browser runs in headless mode. Defaults to `false`. When the env is set to `BROWSERBASE`, this will be ignored
​domSettleTimeoutMsintegerSpecifies the timeout in milliseconds for waiting for the DOM to settle. Defaults to `30_000` (30 seconds)
​logger(message: LogLine) => void`message` is a `LogLine` object. Handles log messages. Useful for custom logging implementations. For more information, see the Logging page
​verboseintegerEnables several levels of logging during automation: `0`: limited to no logging, `1`: SDK-level logging, `2`: LLM-client level logging (most granular)
​debugDombooleanDraws bounding boxes around elements presented to the LLM during automation
​llmClientLLMClientA custom LLM client implementation that conforms to the `LLMClient` abstract class
​systemPromptstringA custom system prompt to use for the LLM in addition to the default system prompt for act, extract, and observe methods.### ​**Returns:** Stagehand objectThe constructor returns an instance of the `Stagehand` class configured with the specified options. However, to use Stagehand, you must still initialize it either with `init()` or `initFromPage()`.​`stagehand.init()`
-------------------```
await stagehand.init();````init()` asynchronously initializes the Stagehand instance. It should be called before any other methods.​`stagehand.close()`
--------------------```
await stagehand.close();````close()` is a cleanup method to remove the temporary files created by Stagehand. It’s recommended that you call this explicitly when you’re done with your automation.Model SupportActxgithublinkedinPowered by MintlifyOn this page* Stagehand constructor
* Arguments: ConstructorParams
* Returns: Stagehand object
* stagehand.init()
* stagehand.close()

Playwright Interoperability - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferencePlaywright InteroperabilityDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferencePlaywright Interoperability
===========================How Stagehand interacts with PlaywrightStagehand is built on top of Playwright, so you can use Playwright methods directly through the Stagehand instance.​`page` and `context`
---------------------`stagehand.page` and `stagehand.context` are instances of Playwright’s `Page` and `BrowserContext` respectively. Use these methods to interact with the Playwright instance that Stagehand is using.```
const page = stagehand.page;
// Base Playwright methods work
await page.goto("https://github.com/browserbase/stagehand");// Stagehand overrides Playwright objects
await page.act({
	action: "click on the contributors"
})```​Stagehand v. Playwright
------------------------Below is an example of how to extract a list of companies from the AI Grant website using both Stagehand and Playwright.Stagehand SDK ReferenceModel SupportxgithublinkedinPowered by MintlifyOn this page* page and context
* Stagehand v. Playwright

Extract - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceExtractDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceExtract
=======Extract structured data from the page.```
  const item = await page.extract({
    instruction: "extract the price of the item",
    schema: z.object({
      price: z.number(),
    }),
  });  const price = item.price; // `item` has schema { price: number }````extract()` grabs structured text from the current page using zod. Given instructions and `schema`, you will receive structured data.We strongly suggest you set `useTextExtract` to `true` if you are extracting data from a longer body of text.
### ​**Arguments:** `ExtractOptions<T extends z.AnyZodObject>`​instructionstringrequiredProvides instructions for extraction
​schemaz.AnyZodObjectrequiredDefines the structure of the data to extract
​useTextExtractbooleanThis method converts the page to text, which is much cleaner for LLMs than the DOM. However, it may not work for use cases that involve DOM metadata elements.
​modelNameAvailableModelSpecifies the model to use
​modelClientOptionsobjectConfiguration options for the model client. See `ClientOptions`.
​domSettleTimeoutMsnumberTimeout in milliseconds for waiting for the DOM to settle### ​**Returns:** `Promise<ExtractResult<T extends z.AnyZodObject>>`Resolves to the structured data as defined by the provided `schema`.ActObservexgithublinkedinPowered by MintlifyOn this page* Arguments: ExtractOptions<T extends z.AnyZodObject>
* Returns: Promise<ExtractResult<T extends z.AnyZodObject>>

Observe - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceObserveDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceObserve
=======Get candidate DOM elements for actions.`observe()` is used to get a list of actions that can be taken on the current page. It’s useful for adding context to your planning step, or if you unsure of what page you’re on.```
  const observations = await page.observe();````observe()` returns an array of objects, each with an XPath `selector` and short `description`.If you are looking for a specific element, you can also pass in an instruction to observe via: `observe({ instruction: "your instruction"})`.```
  const [{ selector, description }] = await page.observe({
    instruction: "Find the buttons on this page",
  });```Observe can also return a suggested action for the candidate element by setting the `returnAction` option to true. Here is a sample `ObserveResult`:```
  {
    "description": "A brief description of the component",
    "method": 'click',
    "arguments": [],
    "selector": 'xpath=/html/body[1]/div[1]/main[1]/button[1]'
  }```
### ​**Arguments:** `ObserveOptions`​instructionstringProvides instructions for the observation. Defaults to “Find actions that can be performed on this page.”
​returnActionbooleanReturns an observe result object that contains a suggested action for the candidate element. The suggestion includes method, and arguments (if any). Defaults to false.
​onlyVisiblebooleanIf true, returns only visible elements. Uses DOM inspection instead of accessibility trees. Defaults to false.
​useAccessibilityTreebooleandeprecated[Deprecated] Previously used for accessibility tree observation. Use `onlyVisible: false` instead.
​modelNameAvailableModelSpecifies the model to use
​modelClientOptionsobjectConfiguration options for the model client
​useVisionboolean | 'fallback'deprecated[Deprecated] Previously used to control vision-based processing. Vision processing is now always enabled.
​domSettleTimeoutMsnumberTimeout in milliseconds for waiting for the DOM to settle### ​**Returns:** `Promise<ObserveResult[]>`Each `ObserveResult` object contains a `selector` and `description`.​selectorstringrequiredA string representing the element selector
​descriptionstringrequiredA string describing the possible actionIf the `returnAction` option is set to true, the following fields will be included in the result.​methodstringThe method to call on the element
​argumentsobjectThe arguments to pass to the methodExtractLoggingxgithublinkedinPowered by MintlifyOn this page* Arguments: ObserveOptions
* Returns: Promise<ObserveResult[]>

Model Support - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceModel SupportDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceModel Support
=============Which models are supported by StagehandStagehand leverages a generic LLM client architecture to support various language models from different providers. This design allows for flexibility, enabling the integration of new models with minimal changes to the core system. Different models work better for different tasks, so you can choose the model that best suits your needs.​Currently Supported Models
---------------------------Stagehand currently supports the latest models from OpenAI and Anthropic.#### ​OpenAI Models* `gpt-4o`
* `gpt-4o-2024-08-06`
* `o1-mini`
* `o1-preview`
* `gpt-4o-mini` (not recommended due to low parameter count)#### ​Anthropic Models* `claude-3-5-sonnet-latest`
* `claude-3-5-sonnet-20240620`
* `claude-3-5-sonnet-20241022`These models can be specified in Stagehand Config as `modelName` or when calling methods like `act()` and `extract()`.​Custom Models
--------------Custom LLM clients are a very new feature and don’t have advanced features like prompt caching yet.We also don’t yet support adding custom LLMClients directly to act/extract/observe methods; they can only be specified in the Stagehand Config.
Check out an Ollama example
---------------------------Check out an example of how to implement a custom model like Llama 3.2 using Ollama.Stagehand supports custom models by implementing your own `LLMClient` interface. This allows you to use any language model that is supported by the `LLMClient` interface.To implement a custom model, you can create a new class that implements the `LLMClient` interface. You can then pass this class to the `Stagehand` instance as the `llmClient` parameter in the Stagehand Config.```
const customLLMClient: LLMClient = new CustomLLMClient();
const stagehand = new Stagehand({ ...StagehandConfig, llmClient: customLLMClient });
await stagehand.init();```For more information on how to implement a custom model, check out the LLMClient interface.Playwright InteroperabilityConfigurationxgithublinkedinPowered by MintlifyOn this page* Currently Supported Models
* OpenAI Models
* Anthropic Models
* Custom Models

Act - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceActDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceAct
===Perform actions on the current page.```
 // Basic usage
 await page.act({ action: "click on add to cart" }); // Using variables
 await page.act({
   action: "enter %username% into the username field",
   variables: {
     username: "john.doe@example.com",
   },
 }); // Multiple variables
 await page.act({
   action: "fill in the form with %username% and %password%",
   variables: {
     username: "john.doe",
     password: "secretpass123",
   },
 });````act()` allows Stagehand to interact with a web page. Provide an `action` like `"Click on the add to cart button"`, or `"Type 'Browserbase' into the search bar"`.Small atomic goals perform the best. Avoid using `act()` to perform complex actions.You can pass an `ObserveResult` to `act()` to perform the suggested action, which will yield a faster and cheaper result (no LLM inference).### ​**Arguments:** `ActOptions` | `ObserveResult``ActOptions`:​actionstringrequiredDescribes the action to perform
​modelNameAvailableModelSpecifies the model to use
​modelClientOptionsobjectConfiguration options for the model client
​useVisionboolean | 'fallback'Determines if vision-based processing should be used. Defaults to “fallback”
​variablesRecord<string, string>Variables to use in the action. Variables in the action string are referenced using %variable\_name%
​domSettleTimeoutMsnumberTimeout in milliseconds for waiting for the DOM to settle`ObserveResult`:​selectorstringrequiredA string representing the element selector
​descriptionstringrequiredA string describing the possible action
​methodstringrequiredThe method to call on the element
​argumentsobjectrequiredThe arguments to pass to the method### ​**Returns:** `Promise<ActResult>`​successbooleanrequiredIf the action was completed successfully
​messagestringrequiredDetails about the action’s execution
​actionstringrequiredThe action performedConfigurationExtractxgithublinkedinPowered by MintlifyOn this page* Arguments: ActOptions | ObserveResult
* Returns: Promise<ActResult>

Logging - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationReferenceLoggingDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Reference* Stagehand SDK Reference
* Playwright Interoperability
* Model Support
* Configuration
* Act
* Extract
* Observe
* Logging
ReferenceLogging
=======Edit the default logging behaviorStagehand logs log a `LogLine` object. You can override the default logger by passing in a custom logger function to the constructor.```
const stagehand = new Stagehand({
	logger: (logLine: LogLine) => {
		console.log(`[${logLine.category}] ${logLine.message}`);
	},
});```Below is the list of fields in the `LogLine` object. `message` is the main log message content, and `auxiliary` contains parameters that can be used to provide additional context and color to the log.​idstringUnique identifier for the log line
​categorystringCategory/type of the log message
​messagestringrequiredThe main log message content
​level0 | 1 | 2Logging verbosity level
​timestampstringTimestamp of when the log was created
​auxiliaryobjectAdditional metadata where each key contains a `value` and `type`. The `value` will always be a string, but `type` can be `"object"`, `"string"`, `"html"`, `"integer"`, `"float"`, or `"boolean"`You can see an example of a log line in `OpenAIClient.ts`. You’ll notice here how `auxiliary` contains a `requestId` and `cachedResponse`.```
this.logger({
	category: "llm_cache",
	message: "LLM cache hit - returning cached response",
	level: 1,
	auxiliary: {
		requestId: {
			value: options.requestId,
			type: "string",
		},
		cachedResponse: {
			value: JSON.stringify(cachedResponse),
			type: "object",
		},
	}
});```
ObservexgithublinkedinPowered by Mintlify

MCP Server - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationIntegrationsMCP ServerDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Integrations* Langchain JS
* MCP Server
IntegrationsMCP Server
==========Integrate Stagehand with MCP ServerA Model Context Protocol (MCP) server provides AI-powered web automation capabilities using Stagehand into Claude Desktop.​Running the MCP Server
-----------------------1. Clone or download the Stagehand MCP server repository.
2. In the project directory, install dependencies:
   
   ```
   npm install
   npm run build
   
   ```
3. Set up your Claude Desktop configuration to use the server.```
{
  "mcpServers": {
    "stagehand": {
      "command": "node",
      "args": ["path/to/mcp-server-browserbase/stagehand/dist/index.js"],
      "env": {
        "BROWSERBASE_API_KEY": "<YOUR_BROWSERBASE_API_KEY>",
        "BROWSERBASE_PROJECT_ID": "<YOUR_BROWSERBASE_PROJECT_ID>",
        "OPENAI_API_KEY": "<YOUR_OPENAI_API_KEY>",
      }
    }
  }
}```4. Then run the server:```
node dist/index.js```5. Restart your Claude Desktop app and you should see the tools available clicking the 🔨 icon.
6. Start using the tools! Below is a demo video of Claude doing a Google search for OpenAI using Stagehand MCP server and Browserbase for a remote headless browser.​Stagehand commands via MCP Server
----------------------------------* **stagehand\_navigate**
  
  * Navigate to any URL in the browser
  * Input:
    * `url` (string): The URL to navigate to
* **stagehand\_act**
  
  * Perform an action on the web page
  * Inputs:
    * `action` (string): The action to perform (e.g., “click the login button”)
    * `variables` (object, optional): Variables used in the action template
* **stagehand\_extract**
  
  * Extract data from the web page based on an instruction and schema
  * Inputs:
    * `instruction` (string): Instruction for extraction (e.g., “extract the price of the item”)
    * `schema` (object): JSON schema for the extracted data
* **stagehand\_observe**
  
  * Observe actions that can be performed on the web page
  * Input:
    * `instruction` (string, optional): Instruction for observation### ​ResourcesThe server provides access to two types of resources:1. **Console Logs** (`console://logs`)
   
   * Browser console output in text format
   * Includes all console messages from the browser
2. **Screenshots** (`screenshot://<name>`)
   
   * PNG images of captured screenshots
   * Accessible via the screenshot name specified during capture​Further Reading
----------------For more in-depth coverage, usage patterns, or troubleshooting:• Model Context Protocol (MCP): https://modelcontextprotocol.io/introduction  • Join our Slack community: https://join.slack.com/t/stagehand-devLangchain JSxgithublinkedinPowered by MintlifyOn this page* Running the MCP Server
* Stagehand commands via MCP Server
* Resources
* Further Reading

Introduction - 🤘 Stagehand🤘 Stagehand home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/stagehand/images/logo_dark.svg)Search or ask...* Support
Search...NavigationGet StartedIntroductionDocumentationReferenceIntegrations* Join our Slack!
* GitHub
* NPM Package
##### Get Started* Introduction
* Quickstart
* Best Practices
* How Stagehand Works
* Contribute to Stagehand
* Examples and Guides
Get StartedIntroduction
============Stagehand is the AI interface to the internet.Stagehand is the easiest way to build browser automations. It is completely interoperable with Playwright and has seamless integration with Browserbase.It offers three simple AI APIs (`act`, `extract`, and `observe`) on top of the base Playwright `Page` class that provide the building blocks for web automation via natural language.Anything that can be done in a browser can be done with Stagehand. Think about stuff like:1. Log into Amazon, search for AirPods, and buy the most relevant product
2. Go to Hacker News and extract the top stories of the day
3. Go to Doordash, find the cheapest pad thai, and order it to your houseThese automations can be built with Playwright, but it can be very cumbersome to write the code, and it will be very vulnerable to minor changes in the UI.Stagehand’s AI, especially when combined with Browserbase’s stealth mode, make it easy to write durable code and bypass bot detection and captchas.​Lights, Camera, `act()`
------------------------Let’s get you started with Stagehand.Quickstart
----------Build browser automations in no time.How Stagehand Works
-------------------Go behind the scenes with Stagehand.​FAQ
----### ​What is Stagehand?Stagehand is the AI-powered successor to Playwright, offering three simple APIs (`act`, `extract`, and `observe`) that provide the building blocks for web automation via natural language.The goal of Stagehand is to provide a lightweight model-agnostic framework, without overly complex abstractions. It’s not going to order you a pizza, but it will help you execute steps like `"click the order button"`.Each Stagehand function takes in an atomic instruction, such as `act("click the login button")` or `extract("find the price of pad thai")`, generates the appropriate Playwright code to accomplish that instruction, and executes it.### ​What is a web agent?A web agent is an AI agent that aims to browse the web like a human. They can navigate the web, interact with web pages, and perform tasks. You could imagine something like telling a bot “here’s my credit card, order me pad thai” and having it do that entirely autonomously.### ​Is Stagehand a web agent?No, Stagehand is not a web agent. It is a set of tools that enables and empowers web agents and developers building them. A web agent could take an instruction like “order me pad thai” and use Stagehand to navigate to the restaurant’s website, find the menu, and order the food.### ​What are some best practices for using Stagehand?Stagehand is something like Github Copilot, but for web automation. It’s not a good idea to ask it to write your entire application, but it’s great for quickly generating self-healing Playwright code to accomplish specific tasks.Therefore, instructions should be atomic to increase reliability, and step planning should be handled by the higher level agent. You can use `observe()` to get a suggested list of actions that can be taken on the current page, and then use those to ground your step planning prompts.### ​Who built Stagehand?Stagehand is open source and maintained by the Browserbase team. We envision a world in which web agents are built with Stagehand on Browserbase.We believe that by enabling more developers to build reliable web automations, we’ll expand the market of developers who benefit from our headless browser infrastructure. This is the framework that we wished we had while tinkering on our own applications, and we’re excited to share it with you.If you’ve made it this far, hi mom!QuickstartxgithublinkedinPowered by MintlifyOn this page* Lights, Camera, act()
* FAQ
* What is Stagehand?
* What is a web agent?
* Is Stagehand a web agent?
* What are some best practices for using Stagehand?
* Who built Stagehand?