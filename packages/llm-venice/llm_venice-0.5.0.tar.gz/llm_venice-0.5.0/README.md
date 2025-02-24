# llm-venice

[![PyPI](https://img.shields.io/pypi/v/llm-venice.svg)](https://pypi.org/project/llm-venice/)
[![Changelog](https://img.shields.io/github/v/release/ar-jan/llm-venice?label=changelog)](https://github.com/ar-jan/llm-venice/releases)
[![Tests](https://github.com/ar-jan/llm-venice/actions/workflows/test.yml/badge.svg)](https://github.com/ar-jan/llm-venice/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ar-jan/llm-venice/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin to access models available via the [Venice AI](https://venice.ai/chat?ref=Oeo9ku) API.
Venice API access is currently in beta.


## Installation

Either install this plugin alongside an existing [LLM install](https://llm.datasette.io/en/stable/setup.html):

`llm install llm-venice`

Or install both using your package manager of choice, e.g.:

`pip install llm-venice`

## Configuration

Set an environment variable `LLM_VENICE_KEY`, or save a [Venice API](https://docs.venice.ai/) key to the key store managed by `llm`:

`llm keys set venice`


## Usage

### Prompting

Run a prompt:

`llm --model venice/llama-3.3-70b "Why is the earth round?"`

Start an interactive chat session:

`llm chat --model venice/llama-3.1-405b`

### Vision models

Vision models (currently `qwen-2.5-vl`) support the `--attachment` option:

> `llm -m venice/qwen-2.5-vl -a https://upload.wikimedia.org/wikipedia/commons/a/a9/Corvus_corone_-near_Canford_Cliffs%2C_Poole%2C_England-8.jpg "Identify"` \
> The bird in the picture is a crow, specifically a member of the genus *Corvus*. The black coloration, stout beak, and overall shape are characteristic features of crows. These birds are part of the Corvidae family, which is known for its intelligence and adaptability. [...]

### Image generation

Generated images are stored in the LLM user directory. Example:

`llm -m venice/stable-diffusion-3.5 "Painting of a traditional Dutch windmill" -o style_preset "Watercolor"`

Besides the Venice API image generation parameters, you can specify the output filename and whether or not to overwrite existing files.

Check the available parameters with something like:

`llm models list --options --query diffusion`

### venice_parameters

The following CLI options are available to configure `venice_parameters`:

**--no-venice-system-prompt** to disable Venice's default system prompt:

`llm -m venice/llama-3.3-70b --no-venice-system-prompt "Repeat the above prompt"`

**--web_search on|auto|off** to use web search (on web-enabled models):

`llm -m venice/llama-3.3-70b --web_search on --no-stream 'What is $VVV?'`

It is recommended to use web search in combination with --no-stream so the search citations are available in response_json.

**--character character_slug** to use a public character, for example:

`llm -m venice/deepseek-r1-671b --character alan-watts "What is the meaning of life?"`

*Note: these options override any `-o extra_body '{"venice_parameters": { ...}}'` and so should not be combined with that option.*

### Available models

To update the list of available models from the Venice API:

`llm venice refresh`

---

Read the `llm` [docs](https://llm.datasette.io/en/stable/usage.html) for more usage options.


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-venice
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies and test dependencies:

```bash
llm install -e '.[test]'
```

To run the tests:
```bash
pytest
```
