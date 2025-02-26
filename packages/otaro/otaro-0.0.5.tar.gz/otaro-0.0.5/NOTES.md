# otaro

- Problem with current prototype is that it is too different from the usual workflow of developers
    - Likewise with DSPy
- Defining LLMs programmatically has potential though
- How do we use LLMs now?
    - API, prompt, pre and post processing
- What if we define it as a JSON or YAML?
    - Then load it via a library
    - Optimizing returns a JSON
        - Contains scores
    - JSON defines the API as well
- BAML
    - Or a schema grammar that optimizes for minimal tokens and maximum noise resistance
    - Does schema declaration need nesting?
        - Rules?
        - **If we are talking about how the LLM responds, rules are not required**
        - If we know the schema, we can parse an output for more efficiently and in a more noise-resistant manner, kinda like constrained generation, but constrained parsing
            - i.e. we want to parse the most likely output from a noisy input
            - If we can place restrictions on the schema (e.g. no reused keys, or all keys must start with _), it becomes even easier to parse
    - Support imports? e.g. commonly used rules
        - Can use imports to improve base config without overwriting
- **Config automatically gets better when you run it**
    - Automatically updates prompt and adds error correction
    - Use lock=True to prevent it from changing
    - Add versioning within config file
        - i.e. use latest prompt by default but retain last 5 prompts
    - Stores examples whenever it is run
        - Tries to rectify any error and add error correction
        - Developer can check records later and fix examples, which will then be used to improve the prompt

## To-do

- Basic YAML config
    - Inputs
        - bool
        - int
        - float
        - str
        - enum
        - list
        - object
    - Outputs
    - Rules
    - Imports
- Basic optimization
    - Optimize desc
NAP
- Basic parsing
- Config - Demos
- Basic API
- Config - Basic rules
---
- Basic tests
    - Tests for different input/output types of varying complexities
- Support sync and async
- Examples
- Documentation
---
- Optimization - error correction
- Optimization - demos
- Optimized parsing
- Infer types from YAML for autocomplete and hinting
- Examples logging

## Notes

- Demos ideally need `reasoning` attribute as well
- Need to optimize loading time of config file
- Need to optimize "optimization" - we are running more calls than necessary

## Tests

```
$ uv run coverage run --source ./otaro -m pytest
$ uv run coverage report -m
```
