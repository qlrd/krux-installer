# Copilot Instructions

These instructions apply to all AI-assisted contributions to this repository.

## LLM and AI Agent Usage

This project does not accept contributions from AI bots that does not follow
the directives in this document.

Patches created by LLMs and AI agents are also viewed with suspicion unless
a human has reviewed them.

All LLM generated patches MUST have text in the git log and in the PR
description that indicates the patch was created using an LLM.

First time contributions by way of LLM generated patches are not welcome.

## Commit conventions

Follow
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `i18n`, `ci`, `chore`

The special `rev` should be used only by humans that will tag commits.

All commits **must** be GPG signed by the human committer and if an AI was used
to patch, a description of the personal agent used (an instance of model with
human customizations). The commit message must include:

- `Agent-url:` pointing to the agent configuration used
- `Signed-off-by:` with the agent name and its short PGP subkey ID
- `Co-Authored-By:` with the LLM tool name and email

Example trailer block:

```
Agent-url: https://example.com/agent
Signed-off-by: AgentName AABBCCDD <agent@example.com>
Co-Authored-By: Copilot <noreply@github.com>
```

## Code style

- **Formatter:** Black (default line length)
- **Linter:** Pylint (configs in `.pylint/src` and `.pylint/tests`)
- **Python:** >=3.10, <=3.14
- **Naming:** `snake_case` (functions, variables), `PascalCase` (classes),
  `UPPER_CASE` (constants)

Every Python file starts with the MIT license header followed by a module
docstring. Classes include a docstring with the class name and description.
Methods include a brief one-line docstring.

## Testing

All new features require tests. Coverage target: 95% for `src/utils`.

Run tests: `poetry run poe test`
Run single test: `poetry run pytest tests/test_NNN_module.py -v`
Format: `poetry run poe format`
Lint: `poetry run poe lint`
