---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, docker, containers]
description: Pretty replacement for `docker ps` - displays Docker containers in a nicely formatted table
icon: command-palette
order: 3

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# dps

A pretty replacement for `docker ps` that displays Docker containers in a nicely formatted table.

## Usage

The tool can be executed in three different ways:

```bash
# Full command
enderclitools dps [OPTIONS]

# Short alias
ect dps [OPTIONS]

# Direct alias
dps [OPTIONS]
```

## Options

### Container Filtering

- `-a, --all` - Show all containers (default shows just running)
- `-f, --filter <FILTER>` - Filter output based on conditions provided
- `-n, --last <LAST>` - Show n last created containers (includes all states) [default: -1]
- `-l, --latest` - Show the latest created container (includes all states)

### Output Formatting

- `--no-trunc` - Don't truncate output
- `-q, --quiet` - Only display container IDs
- `-s, --size` - Display total file sizes

### Table Styling

- `--table-preset <TABLE_PRESET>` - Predefined table styles:
  - `ascii-full` - Full ASCII borders
  - `ascii-full-condensed` - Condensed ASCII borders
  - `ascii-no-borders` - No borders
  - `ascii-borders-only` - Only outer borders
  - `ascii-borders-only-condensed` - Condensed outer borders
  - `ascii-horizontal-only` - Only horizontal lines
  - `ascii-markdown` - Markdown table style
  - `utf8-full` - Full UTF8 borders
  - `utf8-full-condensed` - Condensed UTF8 borders
  - `utf8-no-borders` - No UTF8 borders
  - `utf8-borders-only` - Only UTF8 outer borders
  - `utf8-horizontal-only` - Only UTF8 horizontal lines
  - `nothing` - No formatting

- `--table-modifier <TABLE_MODIFIER>` - Additional table modifiers:
  - `utf8-round-corners` - Rounded corners
  - `utf8-solid-inner-borders` - Solid inner borders

### Column Configuration

- `--headers <HEADERS>` - Determines which columns are displayed:
  - `id` - Container ID
  - `names` - Container names
  - `image` - Docker image
  - `status` - Container status
  - `ports` - Port mappings
  - `command` - Executed command
  - `created-at` - Creation timestamp
  - `created` - Creation time (relative)
  - `size` - Container size
  - `labels` - Container labels
  - `mounts` - Volume mounts

- `--add-headers <ADD_HEADERS>` - Adds additional columns to the default columns (same options as `--headers`)

### Help

- `-h, --help` - Print help

## Examples

```powershell
# Basic usage - show running containers
PS C:\Users\endki> dps
╭──────────────┬───────┬───────┬─────────────┬─────────────────────────────────────╮
│ ID           ┆ Names ┆ Image ┆ Status      ┆ Ports                               │
╞══════════════╪═══════╪═══════╪═════════════╪═════════════════════════════════════╡
│ 74d2c5531c23 ┆ nginx ┆ nginx ┆ Up 1 second ┆ 0.0.0.0:80->80/tcp, [::]:80->80/tcp │
╰──────────────┴───────┴───────┴─────────────┴─────────────────────────────────────╯
```

```bash
# Show all containers
dps -a

# Show only the last 5 containers
dps -n 5

# Containers with UTF8 styling and rounded corners
dps --table-preset utf8-full --table-modifier utf8-round-corners

# Show only container IDs
dps -q

# Show specific columns
dps --headers id,names,status,ports
```
