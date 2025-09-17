---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, configuration]
description: Configuration management for EnderCliTools - manage settings and preferences
icon: gear
order: 1

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# Config

Configuration management for EnderCliTools. This command allows you to manage settings and preferences for the various tools.

## Usage

The config command can be executed in two ways:

```bash
# Full command
enderclitools config <COMMAND>

# Short alias
ect config <COMMAND>
```

## Subcommands

The config command has the following subcommands:

- [`set`](./set) - Set configuration values
- [`get`](./get) - Get configuration values
- [`reset`](./reset) - Reset configuration to defaults
- `help` - Print help message or help for specific subcommand

## Examples

```powershell
# Get help for the config command
PS C:\Users\endki> ect config --help

# Get help for a specific subcommand
PS C:\Users\endki> ect config set --help
PS C:\Users\endki> ect config get --help
PS C:\Users\endki> ect config reset --help
```

## Configuration Structure

EnderCliTools stores its configuration in a structured format that allows you to customize the behavior of various tools like `dps`, `dcps`, and others. Each tool can have its own specific settings while sharing common configuration options.

See the individual subcommand documentation for detailed usage examples and available configuration options.
