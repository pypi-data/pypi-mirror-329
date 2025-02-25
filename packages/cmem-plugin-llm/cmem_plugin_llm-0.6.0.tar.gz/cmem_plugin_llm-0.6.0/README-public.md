# cmem-plugin-llm

Interact with Large Language Models.

[![eccenca Corporate Memory][cmem-shield]][cmem-link]

This is a plugin for [eccenca](https://eccenca.com) [Corporate Memory](https://documentation.eccenca.com). You can install it with the [cmemc](https://eccenca.com/go/cmemc) command line clients like this:

```
cmemc admin workspace python install cmem-plugin-llm
```
  
[![poetry][poetry-shield]][poetry-link] [![ruff][ruff-shield]][ruff-link] [![mypy][mypy-shield]][mypy-link] [![copier][copier-shield]][copier] 

[cmem-link]: https://documentation.eccenca.com
[cmem-shield]: https://img.shields.io/endpoint?url=https://dev.documentation.eccenca.com/badge.json
[poetry-link]: https://python-poetry.org/
[poetry-shield]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
[ruff-link]: https://docs.astral.sh/ruff/
[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&label=Code%20Style
[mypy-link]: https://mypy-lang.org/
[mypy-shield]: https://www.mypy-lang.org/static/mypy_badge.svg
[copier]: https://copier.readthedocs.io/
[copier-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json

### Create Embedding

This plugin contain the following capabilitities:

- create embeddings: it allows to create embeddings from an arbitrary data point or from specified data point paths (properties/columns).
After being processed each data point receive two additional paths the ```_embedding``` path and the ```_embedding_source``` path.
  - The ```_embedding``` path contain the generated embedding.
  - The ```_embedding_source``` path contain the paths utilized for generate the embeddings in text format.

#### Parameters

- ```url```: openAI compatible endpoint, default ```https://api.openai.com/v1```
- ```model```: embedding model, default ```text-embedding-3-small```
- ```api_key```: api key of the endpoint, default blank
- ```timout_single_request```: the request timenout in milliseconds, default ```10000```
- ```entries_processing_buffer```: number of processed entries per request, default ```1000```
- ```embedding_paths```: specify which paths should be used for embedding generation, default all
- ```embedding_output_text```: output path that will contain the embedding text, default ```_embedding_source```
- ```embedding_output_path```: output path that will contain the generated embedding, default ```_embedding```

### Execute Instruction

This plugin contain the following capabilitities:

- execute instruction: it allows to execute an LLM instruction over a given list of entities.
After being processed each entity receive one additional path, the ```_instruction_output```.
  - The ```_instruction_output``` path contains the output of the executed instruction over the entitiy.


#### Parameters

- ```url```: openAI compatible endpoint, default ```https://api.openai.com/v1```
- ```model```: embedding model, default ```gpt-o```
- ```api_key```: api key of the endpoint, default blank
- ```timout_single_request```: the request timenout in milliseconds, default ```10000```
- ```instruction_template```: the instruction template
  default instruct template: ```Write a paragraph about this entity: ${entity}```
- ```prompt_template```: the prompt template
  default prompt template:
  ```
              [{
                  "role": "developer",
                  "content": "You are a helpful assistant."
              },
              {
                  "role": "user",
                  "content": "${instruct}"
              }]
  ```
- ```instruct_output_path```: output path that will contain the output of the executed instruction, default ```_instruction_output```