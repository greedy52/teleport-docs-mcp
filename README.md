# teleport-docs-mcp

Build a MCP server for Teleport Documentation

## How it works

Embeddings generated from [teleport docs](https://github.com/gravitational/teleport/tree/master/docs/pages)
are saved in a Chroma database. A MCP tool is provided to do the vector search
and return the result from the database. Note that no LLM model is used to
interpret the result within the MCP tool. It's up to the AI tool that calls the
MCP tool to interpret the result.

## Pre-req

### Ollama

Install [Ollama](https://ollama.com/), then:
```bash
ollama pull mxbai-embed-large
```

### uv

Install `uv`:
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

## MCP config

Replace with your directory path!
```json
{
  "mcpServers": {
    "teleport-docs": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/teleport-docs-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Refresh database

The vector database is prepopulated and provided with this repo. You can
refresh the data by removing existing indexes, and copy the latest pages from
the [teleport](https://github.com/gravitational/teleport/tree/master/docs/pages)
OSS GitHub repo.

- `rm -rf chroma_index/`
- `cp /path/to/teleport/docs/pages docs/pages`
- `python3 embed.py`

It takes a while to generate though.
