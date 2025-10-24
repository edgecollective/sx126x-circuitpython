# Meshtastic Logger v11 - Local Tiles

This version includes offline map tiles for Massachusetts, New Hampshire, and Vermont.

## Setup

1. **Download tiles** (first time only):
   ```bash
   python3 download_tiles.py
   ```
   This downloads OpenStreetMap tiles for MA, NH, and VT (zoom levels 6-12).

2. **Start the tile server**:
   ```bash
   python3 tile_server.py
   ```
   This starts a local HTTP server on port 8080.

3. **Access the map**:
   Open http://localhost:8080/ in your browser.

## Files

- `index.html` - Map interface (modified to use local tiles)
- `live_logger.py` - Data logger with terminal display
- `download_tiles.py` - Script to download map tiles
- `tile_server.py` - Local HTTP server for tiles
- `tiles/` - Directory containing downloaded map tiles

## Usage

### Start the logger:
```bash
python3 live_logger.py [options]

Options:
  -p, --port           Meshtastic serial port
  -g, --gps-port      GPS serial port  
  -n, --my-node       Your node ID/AKA
  -i, --interval      Polling interval (seconds, default: 10)
  -f, --file          CSV file name (default: log.csv)
  -m, --max-nodes     Max unique nodes to track (default: 50)
```

### Start the tile server (in another terminal):
```bash
python3 tile_server.py
```

### View the map:
Open http://localhost:8080/ in your browser

## Features

- **Fully offline**: Complete offline functionality - no internet required after setup
- **Local tiles**: 3,705 map tiles covering MA, NH, VT (zoom 6-12)
- **Local assets**: Leaflet CSS, JS, and images served locally
- **Real-time updates**: Map updates automatically from latest.csv
- **Node labels**: Shows node names directly on markers
- **SNR-based colors**: Visual signal strength indication
- **Building-level detail**: Zoom up to level 12 for precise positioning

## Tile Coverage

- **Geographic area**: Massachusetts, New Hampshire, Vermont
- **Zoom levels**: 6-12 (covers regional to building-level detail)
- **Storage**: 63MB tiles + 196KB assets = ~63MB total
- **Update frequency**: Tiles cached locally, update manually if needed

## Notes

- **One-time setup**: Internet required only for initial tile/asset download
- **Fully self-contained**: All map tiles and assets stored locally
- **No external dependencies**: Works completely offline after setup
- **Tile server required**: Local server must run to serve tiles and assets
- **Complete coverage**: All zoom levels (6-12) available offline