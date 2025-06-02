# CLI Documentation

## App Store Icon Hunter CLI

The CLI provides an interactive way to search for apps and download their icons.

## Installation

```bash
pip install app-store-icon-hunter
```

## Basic Usage

### Search and Download

```bash
# Basic search with interactive selection
icon-hunter search "Instagram"

# Search specific store
icon-hunter search "WhatsApp" --store appstore

# Auto-download all results
icon-hunter search "Spotify" --auto-download

# Custom icon sizes
icon-hunter search "Telegram" --sizes "64,128,256,512"

# Specify output directory
icon-hunter search "Signal" --output "./my_icons"
```

### Commands

#### `search`
Search for apps and optionally download their icons.

**Arguments:**
- `TERM`: Search term (required)

**Options:**
- `--store, -s`: Store to search (`appstore`, `googleplay`, `both`) [default: both]
- `--country, -c`: Country code [default: us]
- `--limit, -l`: Maximum results per store [default: 10]
- `--auto-download, -a`: Automatically download all results
- `--sizes, -z`: Icon sizes to download [default: 64,128,256,512]
- `--output, -o`: Output directory [default: icons]

**Examples:**
```bash
icon-hunter search "Instagram" --store appstore --limit 5
icon-hunter search "WhatsApp" --auto-download --sizes "128,256"
icon-hunter search "Spotify" --country gb --output "./spotify_icons"
```

#### `list`
Search and list apps without downloading.

**Arguments:**
- `TERM`: Search term (required)

**Options:**
- `--store, -s`: Store to search
- `--country, -c`: Country code
- `--limit, -l`: Maximum results

**Example:**
```bash
icon-hunter list "Instagram" --store both --limit 10
```

#### `interactive`
Run in interactive mode with prompts.

**Example:**
```bash
icon-hunter interactive
```

## Interactive Mode

The interactive mode guides you through the process:

1. Enter search term
2. Select store(s) to search
3. Choose country and result limit
4. Review found apps in a table
5. Select specific apps to download
6. Choose icon sizes
7. Monitor download progress

## Output Structure

Downloaded icons are organized as follows:

```
icons/
├── Instagram/
│   ├── original.png
│   ├── icon_64x64.png
│   ├── icon_128x128.png
│   ├── icon_256x256.png
│   └── icon_512x512.png
└── WhatsApp/
    ├── original.png
    ├── icon_64x64.png
    ├── icon_128x128.png
    ├── icon_256x256.png
    └── icon_512x512.png
```

## Supported Icon Sizes

- 16x16
- 32x32  
- 48x48
- 64x64
- 128x128
- 256x256
- 512x512
- 1024x1024

## Environment Variables

- `SERPAPI_KEY`: Required for Google Play Store search functionality

## Error Handling

The CLI provides clear error messages for common issues:

- Invalid store names
- Invalid country codes
- Network connectivity issues
- Missing API keys
- Invalid icon sizes

## Tips

1. Use `--auto-download` for bulk downloads
2. Specify custom `--sizes` to save space or get specific resolutions
3. Use different `--output` directories to organize downloads by project
4. The `list` command is useful for previewing results before downloading
5. Interactive mode is great for selective downloading
