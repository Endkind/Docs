---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, configuration]
description: Get configuration options for EnderCliTools

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# Get

Get configuration options for EnderCliTools. This command allows you to view current settings for table display and dps output.

## Usage

```bash
ect config get [COMMAND] [OPTIONS]
```

## Subcommands

- [`table`](#table) - Show table configuration
- [`dps`](#dps) - Show dps configuration

---

## table

Show the current table style and modifiers.

### Options

- `-a, --all` - Show all available table configuration options
- `--preset` - Show only the table preset
- `--modifier` - Show only the table modifier

### Example

```powershell
PS C:\Users\endki> ect config get table
╭────────────────┬──────────────────╮
│ OPTION         ┆ VALUE            │
╞════════════════╪══════════════════╡
│ table.preset   ┆ Utf8Full         │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ table.modifier ┆ Utf8RoundCorners │
╰────────────────┴──────────────────╯
```

---

## dps

Show the current default headers (columns) for the `dps` command.

### Options

- `-a, --all` - Show all available dps configuration options
- `--headers` - Show only the dps headers

### Example

```powershell
PS C:\Users\endki> ect config get dps
╭────────────────┬───────────────────────────────────╮
│ OPTION         ┆ VALUE                             │
╞════════════════╪═══════════════════════════════════╡
│ dps.headers    ┆ [Id, Names, Image, Status, Ports] │
╰────────────────┴───────────────────────────────────╯
```

---

## All configuration

Show all configuration options.

### Example

```powershell
PS C:\Users\endki> ect config get
╭────────────────┬───────────────────────────────────╮
│ OPTION         ┆ VALUE                             │
╞════════════════╪═══════════════════════════════════╡
│ table.preset   ┆ Utf8Full                          │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ table.modifier ┆ Utf8RoundCorners                  │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ dps.headers    ┆ [Id, Names, Image, Status, Ports] │
╰────────────────┴───────────────────────────────────╯
```

---

## Help

- `help` - Print this message or the help of the given subcommand(s)
- `-h, --help` - Print help

See also:
[`config set`](../set) | [`config reset`](../reset)
