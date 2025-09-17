---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, configuration]
description: Reset configuration options for EnderCliTools

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# Reset

Reset configuration options for EnderCliTools. This command allows you to restore default settings for table display and dps output. A backup of your previous configuration will be created automatically.

## Usage

```bash
ect config reset [COMMAND] [OPTIONS]
```

## Subcommands

- [`table`](#table) - Reset table configuration to defaults
- [`dps`](#dps) - Reset dps configuration to defaults

---

## table

Reset the table style and modifiers to their default values.

### Options

- `-a, --all` - Reset all table configuration options
- `--preset` - Reset only the table preset
- `--modifier` - Reset only the table modifier

### Example

```powershell
PS C:\Users\endki> ect config reset table
Backup created at: C:\Users\endki\AppData\Roaming\endkind\enderclitools\config\config.toml.1758112128.bak
```

---

## dps

Reset the default headers (columns) for the `dps` command to their default values.

### Options

- `-a, --all` - Reset all dps configuration options
- `--headers` - Reset only the dps headers

### Example

```powershell
PS C:\Users\endki> ect config reset dps
Backup created at: C:\Users\endki\AppData\Roaming\endkind\enderclitools\config\config.toml.1758112121.bak
```

---

## All configuration

Reset all configuration options to their default values.

### Example

```powershell
PS C:\Users\endki> ect config reset
Backup created at: C:\Users\endki\AppData\Roaming\endkind\enderclitools\config\config.toml.1758112121.bak
```

---

## Help

- `help` - Print this message or the help of the given subcommand(s)
- `-h, --help` - Print help

See also:
[`config set`](../set) | [`config get`](../get)
