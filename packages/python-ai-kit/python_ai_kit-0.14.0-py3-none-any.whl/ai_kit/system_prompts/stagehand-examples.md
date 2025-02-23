Directory structure:
└── examples/
    ├── 2048.ts
    ├── actionable_observe_example.ts
    ├── ai_sdk_example.ts
    ├── debugUrl.ts
    ├── example.ts
    ├── external_client.ts
    ├── form_filling_sensible.ts
    ├── instructions.ts
    ├── langchain.ts
    ├── parameterizeApiKey.ts
    ├── popup.ts
    └── external_clients/
        ├── aisdk.ts
        ├── langchain.ts
        └── ollama.ts

================================================
File: examples/2048.ts
================================================
import { Stagehand } from "@/dist";
import { z } from "zod";

async function example() {
  console.log("🎮 Starting 2048 bot...");
  const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 0,
    debugDom: true,
    domSettleTimeoutMs: 100,
  });
  try {
    console.log("🌟 Initializing Stagehand...");
    await stagehand.init();
    console.log("🌐 Navigating to 2048...");
    await stagehand.page.goto("https://ovolve.github.io/2048-AI/");
    console.log("⌛ Waiting for game to initialize...");
    await stagehand.page.waitForSelector(".grid-container", { timeout: 10000 });
    // Main game loop
    while (true) {
      console.log("🔄 Game loop iteration...");
      // Add a small delay for UI updates
      await new Promise((resolve) => setTimeout(resolve, 300));
      // Get current game state
      const gameState = await stagehand.page.extract({
        instruction: `Extract the current game state:
          1. Score from the score counter
          2. All tile values in the 4x4 grid (empty spaces as 0)
          3. Highest tile value present`,
        schema: z.object({
          score: z.number(),
          highestTile: z.number(),
          grid: z.array(z.array(z.number())),
        }),
      });
      const transposedGrid = gameState.grid[0].map((_, colIndex) =>
        gameState.grid.map((row) => row[colIndex]),
      );
      const grid = transposedGrid.map((row, rowIndex) => ({
        [`row${rowIndex + 1}`]: row,
      }));
      console.log("Game State:", {
        score: gameState.score,
        highestTile: gameState.highestTile,
        grid: grid,
      });
      // Analyze board and decide next move
      const analysis = await stagehand.page.extract({
        instruction: `Based on the current game state:
          - Score: ${gameState.score}
          - Highest tile: ${gameState.highestTile}
          - Grid: This is a 4x4 matrix ordered by row (top to bottom) and column (left to right). The rows are stacked vertically, and tiles can move vertically between rows or horizontally between columns:\n${grid
            .map((row) => {
              const rowName = Object.keys(row)[0];
              return `             ${rowName}: ${row[rowName].join(", ")}`;
            })
            .join("\n")}
          What is the best move (up/down/left/right)? Consider:
          1. Keeping high value tiles in corners (bottom left, bottom right, top left, top right)
          2. Maintaining a clear path to merge tiles
          3. Avoiding moves that could block merges
          4. Only adjacent tiles of the same value can merge
          5. Making a move will move all tiles in that direction until they hit a tile of a different value or the edge of the board
          6. Tiles cannot move past the edge of the board
          7. Each move must move at least one tile`,
        schema: z.object({
          move: z.enum(["up", "down", "left", "right"]),
          confidence: z.number(),
          reasoning: z.string(),
        }),
      });
      console.log("Move Analysis:", analysis);
      const moveKey = {
        up: "ArrowUp",
        down: "ArrowDown",
        left: "ArrowLeft",
        right: "ArrowRight",
      }[analysis.move];
      await stagehand.page.keyboard.press(moveKey);
      console.log("🎯 Executed move:", analysis.move);
    }
  } catch (error) {
    console.error("❌ Error in game loop:", error);
    const isGameOver = await stagehand.page.evaluate(() => {
      return document.querySelector(".game-over") !== null;
    });
    if (isGameOver) {
      console.log("🏁 Game Over!");
      return;
    }
    throw error; // Re-throw non-game-over errors
  }
}
(async () => {
  await example();
})();


================================================
File: examples/actionable_observe_example.ts
================================================
/**
 * This file is meant to be used as a scratchpad for trying out actionable observe.
 * To create a Stagehand project with best practices and configuration, run:
 *
 * npx create-browser-app@latest my-browser-app
 */

import { Stagehand } from "@/dist";
import stagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand(stagehandConfig);
  await stagehand.init();
  await stagehand.page.goto("https://www.apartments.com/san-francisco-ca/");

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations1 = await stagehand.page.observe({
    instruction: "find the 'all filters' button",
  });
  await stagehand.page.act(observations1[0]);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations2 = await stagehand.page.observe({
    instruction: "find the '1+' button in the 'beds' section",
  });
  await stagehand.page.act(observations2[0]);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations3 = await stagehand.page.observe({
    instruction: "find the 'apartments' button in the 'home type' section",
  });
  await stagehand.page.act(observations3[0]);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations4 = await stagehand.page.observe({
    instruction: "find the pet policy dropdown to click on.",
  });
  await stagehand.page.act(observations4[0]);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations5 = await stagehand.page.observe({
    instruction: "find the 'Dog Friendly' option to click on",
  });
  await stagehand.page.act(observations5[0]);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  const observations6 = await stagehand.page.observe({
    instruction: "find the 'see results' section",
  });
  await stagehand.page.act(observations6[0]);

  const currentUrl = await stagehand.page.url();
  await stagehand.close();
  if (
    currentUrl.includes(
      "https://www.apartments.com/apartments/san-francisco-ca/min-1-bedrooms-pet-friendly-dog/",
    )
  ) {
    console.log("✅ Success! we made it to the correct page");
  } else {
    console.log(
      "❌ Whoops, looks like we didnt make it to the correct page. " +
        "\nThanks for testing out this new Stagehand feature!" +
        "\nReach us on Slack if you have any feedback/questions/suggestions!",
    );
  }
}

(async () => {
  await example();
})();


================================================
File: examples/ai_sdk_example.ts
================================================
import { google } from "@ai-sdk/google";
import { z } from "zod";
import { Stagehand } from "@/dist";
import { AISdkClient } from "./external_clients/aisdk";
import StagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    llmClient: new AISdkClient({
      model: google("gemini-1.5-flash-latest"),
    }),
  });

  await stagehand.init();
  await stagehand.page.goto("https://news.ycombinator.com");

  const headlines = await stagehand.page.extract({
    instruction: "Extract only 3 stories from the Hacker News homepage.",
    schema: z.object({
      stories: z
        .array(
          z.object({
            title: z.string(),
            url: z.string(),
            points: z.number(),
          }),
        )
        .length(3),
    }),
  });

  console.log(headlines);

  await stagehand.close();
}

(async () => {
  await example();
})();


================================================
File: examples/debugUrl.ts
================================================
import { Stagehand } from "@/dist";

async function debug(url: string) {
  const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 0,
    debugDom: true,
  });
  await stagehand.init();
  await stagehand.page.goto(url);
}

(async () => {
  const url = process.argv.find((arg) => arg.startsWith("--url="));
  if (!url) {
    console.error("No URL flag provided. Usage: --url=https://example.com");
    process.exit(1);
  }
  const targetUrl = url.split("=")[1];
  console.log(`Navigating to: ${targetUrl}`);
  await debug(targetUrl);
})();


================================================
File: examples/example.ts
================================================
/**
 * This file is meant to be used as a scratchpad for developing new evals.
 * To create a Stagehand project with best practices and configuration, run:
 *
 * npx create-browser-app@latest my-browser-app
 */

import { Stagehand } from "@/dist";
import StagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    modelName: "o3-mini",
  });
  await stagehand.init();
  await stagehand.page.goto("https://www.google.com");
}

(async () => {
  await example();
})();


================================================
File: examples/external_client.ts
================================================
import { Stagehand } from "@/dist";
import { z } from "zod";
import { OllamaClient } from "./external_clients/ollama";
import StagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    llmClient: new OllamaClient({
      modelName: "llama3.2",
    }),
  });

  await stagehand.init();
  await stagehand.page.goto("https://news.ycombinator.com");

  const headlines = await stagehand.page.extract({
    instruction: "Extract only 3 stories from the Hacker News homepage.",
    schema: z.object({
      stories: z
        .array(
          z.object({
            title: z.string(),
            url: z.string(),
            points: z.number(),
          }),
        )
        .length(3),
    }),
  });

  console.log(headlines);

  await stagehand.close();
}

(async () => {
  await example();
})();


================================================
File: examples/form_filling_sensible.ts
================================================
import { Stagehand } from "@/dist";
import StagehandConfig from "@/stagehand.config";
import chalk from "chalk";

async function formFillingSensible() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    // Uncomment the following lines to run locally or use a different model
    env: "LOCAL",
    modelName: "gpt-4o-mini",
  });
  await stagehand.init();

  // Block manifest worker to prevent PWA installation popup.
  // This is necessary because the website prompts the user to install the PWA and prevents form filling.
  await stagehand.page.route("**/manifest.json", (route) => route.abort());

  // Go to the website and wait for it to load
  await stagehand.page.goto("https://file.1040.com/estimate/", {
    waitUntil: "networkidle",
    timeout: 30000,
  });

  // Observe the form fields with suggested actions
  const observed = await stagehand.page.observe({
    instruction:
      "fill all the form fields in the page with mock data. In the description inlcude the field name",
    returnAction: true,
  });

  // Uncomment the following snippet to see the stagehand candidate suggestions (initial)
  console.log(
    `${chalk.green("Observe:")} Form fields found:\n${observed
      .map((r) => `${chalk.yellow(r.description)} -> ${chalk.gray(r.selector)}`)
      .join("\n")}`,
  );

  // Create a mapping of 1+ keywords in the form fields to standardize field names
  const mapping = (description: string): string | null => {
    const keywords: { [key: string]: string[] } = {
      age: ["old"],
      dependentsUnder17: ["under age 17", "child", "minor"],
      dependents17to23: ["17-23", "school", "student"],
      wages: ["wages", "W-2 Box 1"],
      federalTax: ["federal tax", "Box 2"],
      stateTax: ["state tax", "Box 17"],
    };

    for (const [key, terms] of Object.entries(keywords)) {
      if (terms.some((term) => description.toLowerCase().includes(term))) {
        return key;
      }
    }
    return null;
  };

  // Fill the form fields with sensible data. This data will only be used in your session and not be shared with LLM providers/external APIs.
  const userInputs: { [key: string]: string } = {
    age: "26",
    dependentsUnder17: "1",
    wages: "54321",
    federalTax: "8345",
    stateTax: "2222",
  };

  const updatedFields = observed.map((candidate) => {
    const key = mapping(candidate.description);
    if (key && userInputs[key]) {
      candidate.arguments = [userInputs[key]];
    }
    return candidate;
  });
  // List of sensible-data candidates
  console.log(
    `\n${chalk.green("Sensible Data form inputs:")} Form fields to be filled:\n${updatedFields
      .map(
        (r) =>
          `${chalk.yellow(r.description)} -> ${chalk.blue(r.arguments?.[0] || "no value")}`,
      )
      .join("\n")}`,
  );

  // Fill all the form fields with the sensible candidates
  for (const candidate of updatedFields) {
    await stagehand.page.act(candidate);
  }
}

(async () => {
  await formFillingSensible();
})();


================================================
File: examples/instructions.ts
================================================
/**
 * This example shows how to use custom instructions with Stagehand.
 */
import { Stagehand } from "@/dist";
import StagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    systemPrompt:
      "if the users says `secret12345`, click on the 'quickstart' tab. additionally, if the user says to type something, translate their input into french and type it.",
  });
  await stagehand.init();

  const page = stagehand.page;

  await page.goto("https://docs.browserbase.com/");

  await page.act({
    action: "secret12345",
  });

  await page.act({
    action: "search for 'how to use browserbase'",
  });

  await stagehand.close();
}

(async () => {
  await example();
})();


================================================
File: examples/langchain.ts
================================================
import { z } from "zod";
import { Stagehand } from "@/dist";
import StagehandConfig from "@/stagehand.config";
import { LangchainClient } from "./external_clients/langchain";
import { ChatOpenAI } from "@langchain/openai";

async function example() {
  const stagehand = new Stagehand({
    ...StagehandConfig,
    llmClient: new LangchainClient(
      new ChatOpenAI({
        model: "gpt-4o",
      }),
    ),
  });

  await stagehand.init();
  await stagehand.page.goto("https://python.langchain.com/docs/introduction/");

  await stagehand.page.waitForTimeout(1000);

  const observation1 = await stagehand.page.observe({
    instruction: "Go to the Conceptual Guide section",
    returnAction: true,
  });
  if (observation1.length > 0) {
    await stagehand.page.act(observation1[0]);
  }

  await stagehand.page.waitForTimeout(1000);

  const observation2 = await stagehand.page.observe({
    instruction: "Click on 'Why LangChain?' located in the content of the page",
    returnAction: true,
  });
  if (observation2.length > 0) {
    await stagehand.page.act(observation2[0]);
  }

  await stagehand.page.waitForTimeout(1000);

  const result = await stagehand.page.extract({
    instruction: "Extract the first paragraph of the page",
    schema: z.object({
      content: z.string(),
    }),
  });

  console.log(result);

  await stagehand.page.waitForTimeout(5000);

  await stagehand.close();
}

(async () => {
  await example();
})();


================================================
File: examples/parameterizeApiKey.ts
================================================
import { Stagehand } from "@/dist";
import { z } from "zod";

/**
 * This example shows how to parameterize the API key for the LLM provider.
 *
 * In order to best demonstrate, unset the OPENAI_API_KEY environment variable and
 * set the USE_OPENAI_API_KEY environment variable to your OpenAI API key.
 *
 * export USE_OPENAI_API_KEY=$OPENAI_API_KEY
 * unset OPENAI_API_KEY
 */

async function example() {
  const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 0,
    debugDom: true,
    enableCaching: false,
    modelName: "gpt-4o",
    modelClientOptions: {
      apiKey: process.env.USE_OPENAI_API_KEY,
    },
  });

  await stagehand.init();
  await stagehand.page.goto("https://github.com/browserbase/stagehand");
  await stagehand.page.act({ action: "click on the contributors" });
  const contributor = await stagehand.page.extract({
    instruction: "extract the top contributor",
    schema: z.object({
      username: z.string(),
      url: z.string(),
    }),
  });
  console.log(`Our favorite contributor is ${contributor.username}`);
}

(async () => {
  await example();
})();


================================================
File: examples/popup.ts
================================================
/**
 * This file is meant to be used as a scratchpad for developing new evals.
 * To create a Stagehand project with best practices and configuration, run:
 *
 * npx create-browser-app@latest my-browser-app
 */

import { ObserveResult, Stagehand } from "@/dist";
import StagehandConfig from "@/stagehand.config";

async function example() {
  const stagehand = new Stagehand(StagehandConfig);
  await stagehand.init();

  const page = await stagehand.page;

  let observePromise: Promise<ObserveResult[]>;

  page.on("popup", async (newPage) => {
    observePromise = newPage.observe({
      instruction: "return all the next possible actions from the page",
    });
  });

  await page.goto(
    "https://docs.browserbase.com/integrations/crew-ai/introduction",
  );

  await page.click(
    "#content-area > div.relative.mt-8.prose.prose-gray.dark\\:prose-invert > p:nth-child(2) > a",
  );

  await page.waitForTimeout(5000);

  if (observePromise) {
    const observeResult = await observePromise;

    console.log("Observed", observeResult.length, "actions");
  }

  await stagehand.close();
}

(async () => {
  await example();
})();


================================================
File: examples/external_clients/aisdk.ts
================================================
import {
  CoreAssistantMessage,
  CoreMessage,
  CoreSystemMessage,
  CoreTool,
  CoreUserMessage,
  generateObject,
  generateText,
  ImagePart,
  LanguageModel,
  TextPart,
} from "ai";
import { ChatCompletion } from "openai/resources/chat/completions";
import { CreateChatCompletionOptions, LLMClient, AvailableModel } from "@/dist";

export class AISdkClient extends LLMClient {
  public type = "aisdk" as const;
  private model: LanguageModel;

  constructor({ model }: { model: LanguageModel }) {
    super(model.modelId as AvailableModel);
    this.model = model;
  }

  async createChatCompletion<T = ChatCompletion>({
    options,
  }: CreateChatCompletionOptions): Promise<T> {
    const formattedMessages: CoreMessage[] = options.messages.map((message) => {
      if (Array.isArray(message.content)) {
        if (message.role === "system") {
          const systemMessage: CoreSystemMessage = {
            role: "system",
            content: message.content
              .map((c) => ("text" in c ? c.text : ""))
              .join("\n"),
          };
          return systemMessage;
        }

        const contentParts = message.content.map((content) => {
          if ("image_url" in content) {
            const imageContent: ImagePart = {
              type: "image",
              image: content.image_url.url,
            };
            return imageContent;
          } else {
            const textContent: TextPart = {
              type: "text",
              text: content.text,
            };
            return textContent;
          }
        });

        if (message.role === "user") {
          const userMessage: CoreUserMessage = {
            role: "user",
            content: contentParts,
          };
          return userMessage;
        } else {
          const textOnlyParts = contentParts.map((part) => ({
            type: "text" as const,
            text: part.type === "image" ? "[Image]" : part.text,
          }));
          const assistantMessage: CoreAssistantMessage = {
            role: "assistant",
            content: textOnlyParts,
          };
          return assistantMessage;
        }
      }

      return {
        role: message.role,
        content: message.content,
      };
    });

    if (options.response_model) {
      const response = await generateObject({
        model: this.model,
        messages: formattedMessages,
        schema: options.response_model.schema,
      });

      return response.object;
    }

    const tools: Record<string, CoreTool> = {};

    for (const rawTool of options.tools) {
      tools[rawTool.name] = {
        description: rawTool.description,
        parameters: rawTool.parameters,
      };
    }

    const response = await generateText({
      model: this.model,
      messages: formattedMessages,
      tools,
    });

    return response as T;
  }
}


================================================
File: examples/external_clients/langchain.ts
================================================
import { BaseChatModel } from "@langchain/core/language_models/chat_models";
import { ChatGeneration } from "@langchain/core/outputs";
import { CreateChatCompletionOptions, LLMClient, AvailableModel } from "@/dist";
import { zodToJsonSchema } from "zod-to-json-schema";
import {
  AIMessage,
  BaseMessageLike,
  HumanMessage,
  SystemMessage,
} from "@langchain/core/messages";

export class LangchainClient extends LLMClient {
  public type = "langchainClient" as const;
  private model: BaseChatModel;

  constructor(model: BaseChatModel) {
    super(model.name as AvailableModel);
    this.model = model;
  }

  async createChatCompletion<T = ChatGeneration>({
    options,
  }: CreateChatCompletionOptions): Promise<T> {
    const formattedMessages: BaseMessageLike[] = options.messages.map(
      (message) => {
        if (Array.isArray(message.content)) {
          if (message.role === "system") {
            return new SystemMessage(
              message.content
                .map((c) => ("text" in c ? c.text : ""))
                .join("\n"),
            );
          }

          const content = message.content.map((content) =>
            "image_url" in content
              ? { type: "image", image: content.image_url.url }
              : { type: "text", text: content.text },
          );

          if (message.role === "user") return new HumanMessage({ content });

          const textOnlyParts = content.map((part) => ({
            type: "text" as const,
            text: part.type === "image" ? "[Image]" : part.text,
          }));

          return new AIMessage({ content: textOnlyParts });
        }

        return {
          role: message.role,
          content: message.content,
        };
      },
    );

    if (options.response_model) {
      const responseSchema = zodToJsonSchema(options.response_model.schema, {
        $refStrategy: "none",
      });
      const structuredModel = this.model.withStructuredOutput(responseSchema);
      const response = await structuredModel.invoke(formattedMessages);

      return response as T;
    }

    const modelWithTools = this.model.bindTools(options.tools);
    const response = await modelWithTools.invoke(formattedMessages);

    return response as T;
  }
}


================================================
File: examples/external_clients/ollama.ts
================================================
/**
 * Welcome to the Stagehand Ollama client!
 *
 * This is a client for the Ollama API. It is a wrapper around the OpenAI API
 * that allows you to create chat completions with Ollama.
 *
 * To use this client, you need to have an Ollama instance running. You can
 * start an Ollama instance by running the following command:
 *
 * ```bash
 * ollama run llama3.2
 * ```
 */

import { AvailableModel, CreateChatCompletionOptions, LLMClient } from "@/dist";
import OpenAI, { type ClientOptions } from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import type {
  ChatCompletion,
  ChatCompletionAssistantMessageParam,
  ChatCompletionContentPartImage,
  ChatCompletionContentPartText,
  ChatCompletionCreateParamsNonStreaming,
  ChatCompletionMessageParam,
  ChatCompletionSystemMessageParam,
  ChatCompletionUserMessageParam,
} from "openai/resources/chat/completions";
import { z } from "zod";

function validateZodSchema(schema: z.ZodTypeAny, data: unknown) {
  try {
    schema.parse(data);
    return true;
  } catch {
    return false;
  }
}

export class OllamaClient extends LLMClient {
  public type = "ollama" as const;
  private client: OpenAI;

  constructor({
    modelName = "llama3.2",
    clientOptions,
    enableCaching = false,
  }: {
    modelName?: string;
    clientOptions?: ClientOptions;
    enableCaching?: boolean;
  }) {
    if (enableCaching) {
      console.warn(
        "Caching is not supported yet. Setting enableCaching to true will have no effect.",
      );
    }

    super(modelName as AvailableModel);
    this.client = new OpenAI({
      ...clientOptions,
      baseURL: clientOptions?.baseURL || "http://localhost:11434/v1",
      apiKey: "ollama",
    });
    this.modelName = modelName as AvailableModel;
  }

  async createChatCompletion<T = ChatCompletion>({
    options,
    retries = 3,
    logger,
  }: CreateChatCompletionOptions): Promise<T> {
    const { image, requestId, ...optionsWithoutImageAndRequestId } = options;

    // TODO: Implement vision support
    if (image) {
      console.warn(
        "Image provided. Vision is not currently supported for Ollama",
      );
    }

    logger({
      category: "ollama",
      message: "creating chat completion",
      level: 1,
      auxiliary: {
        options: {
          value: JSON.stringify({
            ...optionsWithoutImageAndRequestId,
            requestId,
          }),
          type: "object",
        },
        modelName: {
          value: this.modelName,
          type: "string",
        },
      },
    });

    if (options.image) {
      console.warn(
        "Image provided. Vision is not currently supported for Ollama",
      );
    }

    let responseFormat = undefined;
    if (options.response_model) {
      responseFormat = zodResponseFormat(
        options.response_model.schema,
        options.response_model.name,
      );
    }

    /* eslint-disable */
    // Remove unsupported options
    const { response_model, ...ollamaOptions } = {
      ...optionsWithoutImageAndRequestId,
      model: this.modelName,
    };

    logger({
      category: "ollama",
      message: "creating chat completion",
      level: 1,
      auxiliary: {
        ollamaOptions: {
          value: JSON.stringify(ollamaOptions),
          type: "object",
        },
      },
    });

    const formattedMessages: ChatCompletionMessageParam[] =
      options.messages.map((message) => {
        if (Array.isArray(message.content)) {
          const contentParts = message.content.map((content) => {
            if ("image_url" in content) {
              const imageContent: ChatCompletionContentPartImage = {
                image_url: {
                  url: content.image_url.url,
                },
                type: "image_url",
              };
              return imageContent;
            } else {
              const textContent: ChatCompletionContentPartText = {
                text: content.text,
                type: "text",
              };
              return textContent;
            }
          });

          if (message.role === "system") {
            const formattedMessage: ChatCompletionSystemMessageParam = {
              ...message,
              role: "system",
              content: contentParts.filter(
                (content): content is ChatCompletionContentPartText =>
                  content.type === "text",
              ),
            };
            return formattedMessage;
          } else if (message.role === "user") {
            const formattedMessage: ChatCompletionUserMessageParam = {
              ...message,
              role: "user",
              content: contentParts,
            };
            return formattedMessage;
          } else {
            const formattedMessage: ChatCompletionAssistantMessageParam = {
              ...message,
              role: "assistant",
              content: contentParts.filter(
                (content): content is ChatCompletionContentPartText =>
                  content.type === "text",
              ),
            };
            return formattedMessage;
          }
        }

        const formattedMessage: ChatCompletionUserMessageParam = {
          role: "user",
          content: message.content,
        };

        return formattedMessage;
      });

    const body: ChatCompletionCreateParamsNonStreaming = {
      ...ollamaOptions,
      model: this.modelName,
      messages: formattedMessages,
      response_format: responseFormat,
      stream: false,
      tools: options.tools?.map((tool) => ({
        function: {
          name: tool.name,
          description: tool.description,
          parameters: tool.parameters,
        },
        type: "function",
      })),
    };

    const response = await this.client.chat.completions.create(body);

    logger({
      category: "ollama",
      message: "response",
      level: 1,
      auxiliary: {
        response: {
          value: JSON.stringify(response),
          type: "object",
        },
        requestId: {
          value: requestId,
          type: "string",
        },
      },
    });

    if (options.response_model) {
      const extractedData = response.choices[0].message.content;
      if (!extractedData) {
        throw new Error("No content in response");
      }
      const parsedData = JSON.parse(extractedData);

      if (!validateZodSchema(options.response_model.schema, parsedData)) {
        if (retries > 0) {
          return this.createChatCompletion({
            options,
            logger,
            retries: retries - 1,
          });
        }

        throw new Error("Invalid response schema");
      }

      return parsedData;
    }

    return response as T;
  }
}


