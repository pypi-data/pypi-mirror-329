# Choose MCP Server Setup

1. Start by downloading the Claude Desktop Client: https://claude.ai/download

2. Install the MCP server

Edit the `claude_desktop_config.json` file (located in `~/Library/Application\ Support/Claude`) and add the following to the mcpServers section:

```javascript
{
	"mcpServers": {
		"Choose MCP Server": {
			"command": "uvx",
			"args": ["choose-mcp-server"],
			"env": {
				"PROJECT_ID": YOUR_PROJECT_ID,
				"DATASET": YOUR_DATASET
			}
		}
	}
}
```

3. Open Claude Desktop and start asking questions!

## Troubleshooting

For Windows users, you may need to add the `APPDATA` environment variable to your Claude Desktop config file.

```javascript
"env": {
    ...,
	"APPDATA": "C:\\Users\\YOUR_USERNAME\\AppData\\Roaming",
}
```
