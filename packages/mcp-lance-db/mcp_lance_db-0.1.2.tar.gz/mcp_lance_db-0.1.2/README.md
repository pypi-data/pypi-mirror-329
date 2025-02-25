# mcp-lance-db MCP server

mcp-lance-db

## Components

### Tools

The server implements two tools:
- add-memory: Adds a new memory to the vector database
  - Takes "content" as a required string argument
  - Stores the text with vector embeddings for later retrieval
  
- search-memories: Retrieves semantically similar memories
  - Takes "query" as a required string argument
  - Optional "limit" parameter to control number of results (default: 5)
  - Returns memories ranked by semantic similarity to the query
  - Updates server state and notifies clients of resource changes

## Configuration

The server uses the following configuration:
- Database path: "./lancedb"
- Collection name: "memories"
- Embedding provider: "sentence-transformers"
- Model: "BAAI/bge-small-en-v1.5"
- Device: "cpu"
- Similarity threshold: 0.7 (upper bound for distance range)

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-lance-db": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/kyryl/Projects/KOML/MCP/mcp-server-lancedb",
        "run",
        "mcp-lance-db"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-lance-db": {
      "command": "uvx",
      "args": [
        "mcp-lance-db"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/kyryl/Projects/KOML/MCP/mcp-server-lancedb run mcp-lance-db
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.