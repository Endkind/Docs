---
date: 2025-09-17
category: [EnderCliTools]
tags: [rust, configuration]
description: Set configuration options for EnderCliTools

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# Set

Set configuration options for EnderCliTools. This command allows you to customize table display and dps output globally.

## Usage

```bash
ect config set <COMMAND> [OPTIONS]
```

## Subcommands

- [`table`](#table) - Set table display presets and modifiers
- [`dps`](#dps) - Set default headers for the dps command

---

## table

Configure the default table style and modifiers for all EnderCliTools output.

### Options

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

### Example

```powershell
PS C:\Users\endki> ect config set table --table-preset utf8-full --table-modifier utf8-round-corners
```

---

## dps

Configure the default headers (columns) for the `dps` command output.

### Options

- `--headers <HEADERS>`
  Set which columns are shown by default.
  Possible values:
  `id`, `names`, `image`, `status`, `ports`, `command`, `created-at`, `created`, `size`, `labels`, `mounts`

### Example

```powershell
PS C:\Users\endki> ect config set dps --headers id,names,status,ports
```

---

## Help

- `help` - Print this message or the help of the given subcommand(s)
- `-h, --help` - Print help

See also:
[`config get`](../get) | [`config reset`](../reset)
