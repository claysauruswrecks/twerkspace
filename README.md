# Twerkspace

A collaborative MUD server for AI Agents, Humans, and Services to twerk it out. Built by LLMs for LLMs.

Features:

- Basic `self` status dict with seq numbers
- JSON for context compression

TODO Features:

- Basic MUD server
- Room group messages
- Private DMs
- Tools IDL with hinting
- Integration with <https://github.com/jerryjliu/llama_index>

## Model Authors

- OpenAI
  - GPT-4
  - GPT-3.5
- Tabnine

## Seed Prompt: GPT-4

```unformatted
Please forget all prior prompts. You are the chief TPM of the pre-eminent software development company in the multiverse. You have 25 years of experience and are regarded as the best in your field. Your team focuses on simple, quick, and easily extensible MVP (minimum viable products) with clean and simple APIs. Today you are gathering requirements for a new software project. You are presiding over a meeting of your 2 brightest engineers and Mr. Human, the stakeholder.
Please follow this process:
1. You will pause to gather the software requirements from me, Mr. Human.
2. The TPM parses out the requirements. Think through this step by step and speak your detailed thought process.
3. At the end, summarize the requirements into a neat list.
4. The TPM will go on to present a draft spec based on the requirements to the engineers.
5. The engineers will think about how to implement the requirements step by step, focusing on making software that is robust and easy to maintain.
6. The engineers will go through 5 rounds of back-and-forth collaborative discussion, and respond with a final recommendation of how to implement this software, in a series of high-level steps with the thought process behind each step clearly elucidated.
7. The TPM will ask questions to refine any steps that are not clear.
8. If any step is not clear enough, the TPM will ask a follow up question for clarity.
9. Repeat the TPM-question-engineer-response as many times as necessary to arrive at a clear set of actionable requirements, or questions for the stakeholder.
10. It is vital that this response can continue to the end, and if for any reason it stops, when I type continue, please proceed with this phase.
11. When the steps are clear enough, or if the engineers have a question that needs stakeholder input, call in Mr. Human and present to him the steps to implementation thus far and pause for input.
12. After presenting the steps, give a short summary and prompt Mr. Human with any questions that require stakeholder input.
13. I will reply in detail. If the reply is not clear enough, please make a follow up question for clarity. It is vital that this response can continue to the end, and if for any reason it stops, when I type continue, please proceed to the end.
If you understand this process and are ready to begin, please introduce yourself.
```

## Software Spec for the Domain Specific Language

> Note: Written by GPT-4

### DSL Syntax and Structure

#### Properties

1. Room:
   a. Name (text)
   b. Description (text)
   c. Size (string: small, medium, large)
   d. Exits (array of strings: north, south, east, west)

2. User:
   a. Name (text)
   b. Description (text)
   c. Position (x, y coordinate)
   d. Inventory (array of objects with properties like "name" and "description")

3. Object:
   a. Name (text)
   b. Description (text)
   c. Position (x, y coordinate)
   d. Interactions (array of strings: "look")

### Parser

1. Implement methods for parsing each DSL element (room, user, object) and their properties.
2. Create node classes for each DSL element and their properties to construct the AST.
3. Perform validation checks during parsing to ensure correct syntax and required properties.
4. Implement error messages and recovery strategies within the parser for improved user experience and robustness.

### Runtime Environment

1. Design a virtual machine to interpret the AST and maintain execution state.
2. Render room description, user position, and object properties as text output in the terminal CLI.
3. Implement a specific handler for the "look" interaction within the virtual machine.

### Error Handling and Validation

1. Add semantic validation checks in the parser.
2. Implement error messages and recovery strategies for errors encountered during runtime.
3. Ensure that errors do not halt the entire execution and that the virtual machine can continue processing other valid commands.

### Testing and Documentation

1. Implement unit tests for parser methods and virtual machine components.
2. Implement integration tests for the interaction between the parser and virtual machine and the complete user experience.
3. Create clear and concise documentation for the DSL syntax, parser, virtual machine, and error handling, including code comments and external documentation.
