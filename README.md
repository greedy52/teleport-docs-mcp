# teleport-docs-mcp

Build a MCP server for Teleport Documentation

## How it works

Embeddings generated from [teleport docs](https://github.com/gravitational/teleport/tree/master/docs/pages)
are saved in a Chroma database. A MCP tool is provided to do the vector search
and return the result from the database. Note that no LLM model is used to
interpret the result within the MCP tool. It's up to the AI tool that calls the
MCP tool to interpret the result.

## Pre-req

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


## If need to rebuild database

The vector database is prepopulated and provided with this repo. You can
refresh the data by removing existing indexes, and copy the latest pages from
the [teleport](https://github.com/gravitational/teleport/tree/master/docs/pages)
OSS GitHub repo.

To prep files:
```bash
rm -rf docs/pages
rm -rf docs/pages_fixed
cp /path/to/teleport/docs/pages docs/pages`
cp /path/to/teleport/examples docs/examples`
python3 fix_include.py
```

To generate new db:
```bash
rm -rf chroma_index/
python3 embed.py
```

It takes a while to generate though.
