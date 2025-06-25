# teleport-docs-mcp
Build a MCP server for Teleport Documentation

## Pre

### Ollama

Install [Ollama](https://ollama.com/), then:
```bash
ollama pull mxbai-embed-large
ollama pull qwen3
```

### uv

Install `uv`:
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Setup env:
```bash
uv venv
source .venv/bin/activate
uv pip sync
```

## MCP config

```json
{
  "mcpServers": {
    "teleport-docs": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/stevehuang/go/github.com/greedy52/teleport-docs-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```
Replace with your directory path!
