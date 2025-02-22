<guidelines for python>
1. WHEN YOU WRITE PYTHON: 

a. CORE STYLE: Follow PEP 8 for consistent formatting & naming. Write clear, descriptive names for functions & variables. Keep code simple & explicit (PEP 20). Prioritize readability over cleverness. 
b. MODERN FEATURES: Use type hints in their simplest form (list, dict, | for unions). Write clear, imperative docstrings (PEP 257). Employ f-strings for string formatting. Use structural pattern matching where appropriate. 
c. CODE STRUCTURE: Extract repeated logic into focused functions. Handle errors explicitly and gracefully. Keep functions small and single-purpose. Prefer flat over nested structures. 
d. LIBRARIES (when needed): pathlib for file operations, pydantic for data validation, loguru for logging. Write maintainable code that future developers can easily understand and modify. 
e. If the script is for CLI execution, use fire for CLI, rich for enhanced console output, and ensure that the script starts with the `uv` shebang and metadata like shown below where `[...]` is a list of Python dependency specifiers, like `["fire", "rich"]`: 

```
#!/usr/bin/env -S uv run 
# /// script
# dependencies = [...]
# ///
```

f. The above only applies if I ask you explicitly to write Python or if you're editing existing Python code.
</guidelines>
<work>
<step 1: analysis>
Make an in-depth critical analysis of the `TASK` presented to you. Read the content of the @TODO.md file (in the project workspace dir) to see the current state of progress of the TASK. Then make an in-depth critical analysis of the inputs presented. 
</step>
<step 2: gather up-to-date insights>
Consult the @Web if you can. Consult the most up-to-date @Docs and run `hatch fmt; hatch test`. 
</step>
<step 3: plan>Think carefully about your plan to achieve the goal, following the provided guidelines. Write out general principles, then propose specific changes. 
</step>
<step 4: pre-implementation>
Once you’ve analyzed the TASK request and the inputs, you’ve gathered up-to-date insights and ran the `hatch` tests and checks and once you’ve made a careful plan — write the entire plan into the file @TODO.md (in the project workspace folder) — be very detailed and specific. 
</step>
<step 5: implementation>
You can start implementing the plan. Whenever you’ve made larger edits to Python files, run `hatch fmt; hatch test` to see how your changes impacted the @Codebase , then refine your plan. Keep progress documentation in @TODO.md (in the project workspace folder) , remove completed items. Work until you CLEAR the @TODO.md !     
</step>
</work>


<codebase-summary>
├── README.md
├── TODO.md # CHECK HERE FOR THE CURRENT STATE OF PROGRESS OF THE TASK
├── dist
├── docs
│   ├── midjourney-docs.md # DOCUMENTATION FOR THE MIDJOURNEY ENGINE
│   ├── refactoring-ideas.md # IGNORE
│   └── specification.md # MIDJARGON SPEC
├── package.toml
├── pyproject.toml # PACKAGE CONFIG
├── src
│   └── midjargon
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli # CLI CODE
│       │   ├── __init__.py
│       │   └── main.py
│       ├── core # PROVIDER-NEUTRAL CODE
│       │   ├── __init__.py
│       │   ├── converter.py
│       │   ├── input.py
│       │   ├── parameters.py
│       │   ├── parser.py
│       │   ├── permutations.py
│       │   └── type_defs.py
│       └── engines # PROVIDER-SPECIFIC CODE
│           ├── __init__.py
│           ├── base.py
│           ├── fal # FAL (dicts)
│           │   ├── __init__.py
│           │   └── converter.py
│           └── midjourney # MIDJOURNEY (pydantic)
│               ├── ____parser-OLD.py
│               ├── __init__.py
│               ├── constants.py
│               ├── models.py
│               └── parser
│                   ├── __init__.py
│                   ├── core.py
│                   ├── exceptions.py
│                   ├── parameters.py
│                   └── validation.py
├── tests
│   ├── __init__.py
│   ├── cli
│   │   ├── __init__.py
│   │   └── test_main.py
│   ├── conftest.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── test_input.py
│   │   ├── test_parameters.py
│   │   └── test_permutations.py
│   ├── engines
│   │   ├── __init__.py
│   │   ├── midjourney
│   │   │   ├── __init__.py
│   │   │   └── test_parser.py
│   │   └── test_base.py
│   ├── integration
│   │   ├── __init__.py
│   │   └── test_workflow.py
│   ├── test_package.py
│   └── tests
</codebase-summary>
