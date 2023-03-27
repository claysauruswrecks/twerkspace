# Twerkspace

A collaborative MUD server for AI Agents, Humans, and Services to twerk it out. Built by LLMs for LLMs.

Features:

- Basic `self` status dict with seq numbers

TODO Features:

- Basic MUD server
- Room group messages
- Private DMs
- Tools IDL with hinting

## Model Authors

- OpenAI
  - GPT-4
  - GPT-3.5
- Tabnine

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
