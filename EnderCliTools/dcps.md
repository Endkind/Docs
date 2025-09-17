---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, docker, docker-compose, containers]
description: Pretty replacement for `docker compose ps` - displays Docker Compose services in a nicely formatted table
icon: command-palette
order: 2

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# dcps

A pretty replacement for `docker compose ps` that displays Docker Compose services in a nicely formatted table.

## Usage

The tool can be executed in three different ways:

```bash
# Full command
enderclitools dcps [OPTIONS]

# Short alias
ect dcps [OPTIONS]

# Direct alias
dcps [OPTIONS]
```

## Options

### Container Filtering
- `-a, --all` - Show all containers (default shows just running)
- `-f, --filter <FILTER>` - Filter output based on conditions provided
- `--no-orphans` - Exclude orphaned services (not declared by project)
- `--status <STATUS>` - Filter services by status:
  - `paused` - Show only paused containers
  - `restarting` - Show only restarting containers
  - `removing` - Show only containers being removed
  - `running` - Show only running containers
  - `dead` - Show only dead containers
  - `created` - Show only created containers
  - `exited` - Show only exited containers

### Output Formatting
- `--no-trunc` - Don't truncate output
- `-q, --quiet` - Only display container IDs
- `--services` - Display services

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
  - `service` - Service name
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
# Basic usage - show running compose services
PS C:\Users\endki\laravel_example> dcps
╭───────────┬───────────────────────────┬───────────────────┬─────────────────────────────────────╮
│ Service   ┆ Image                     ┆ Status            ┆ Ports                               │
╞═══════════╪═══════════════════════════╪═══════════════════╪═════════════════════════════════════╡
│ db        ┆ postgres:latest           ┆ Up About a minute ┆ 5432/tcp                            │
├╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ queue     ┆ laravel_example-queue     ┆ Up About a minute ┆ 9000/tcp                            │
├╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ redis     ┆ redis:latest              ┆ Up About a minute ┆ 6379/tcp                            │
├╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ scheduler ┆ laravel_example-scheduler ┆ Up About a minute ┆ 9000/tcp                            │
├╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ web       ┆ laravel_example-web       ┆ Up About a minute ┆ 0.0.0.0:80->80/tcp, [::]:80->80/tcp │
╰───────────┴───────────────────────────┴───────────────────┴─────────────────────────────────────╯
```

```bash
# Show all containers including stopped ones
dcps -a

# Show only running services
dcps --status running

# Show only service names
dcps --services

# Filter by specific status
dcps --status exited

# Show specific columns
dcps --headers service,names,status,ports

# Exclude orphaned containers
dcps --no-orphans
```
