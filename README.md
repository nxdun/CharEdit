# CharEdit

Lightweight desktop editor for 3D character cards and Blender model presets.

## Features

- **Direct Property Editing**: Adjust anatomy proportions, face topology, hairstyles, materials, and colors without opening full 3D software.
- **Copy Checkpoints**: 5 instant snapshot slots (`CP` panel) to stage, compare, and revert iterations.
- **Card Thumbnail Control**: Swap or restore embedded card preview renders.
- **Data Portability**: Export and import character presets as JSON.
- **Agent Integration**: Built-in [Model Context Protocol (MCP)](mcp_server/) server for AI agents and Blender automation.

## Usage

1. Launch `HS2CharEdit.exe` or build with .NET 6 (`dotnet run --project HS2CharEdit`).
2. Drag and drop any 3D character card PNG onto the window.
3. Modify parameters across tabs.
4. Save snapshot states with **CP** on the toolbar.
5. Click **Save** to write the updated card PNG.

## MCP Server

Local MCP server for Blender scripts and AI agent pairing:

```powershell
uv --directory mcp_server run server.py
```

## License

GPL-3.0
