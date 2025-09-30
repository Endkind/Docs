---
date: 2025-09-30
category: [GitHub Actions, Laravel]
tags: [github-actions, php, laravel, automation]
description: GitHub Action to install PHP via php.new and run composer install for Laravel projects
icon: rocket

author:
  - name: Endkind
    link: https://github.com/Endkind
    avatar: https://github.com/Endkind.png
---

# Laravel Setup Action

GitHub Action to install **PHP on Linux and Windows GitHub Actions runners** via **php.new**, verify the installation, and run `composer install` (only if a `composer.json` is present in the repository root).

> **Status:** Linux and Windows supported. macOS unsupported.

---

## Inputs

| Name          | Type   | Default | Description                        |
| ------------- | ------ | ------- | ---------------------------------- |
| `php-version` | string | `"8.4"` | PHP version for php.new (default). |

---

## Usage

### Basic Usage

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install PHP via php.new and install Composer deps
        uses: endkind/laravel-setup-action@v1
        with:
          php-version: "8.4"
```

### Pin a Specific PHP Version

```yaml
- uses: endkind/laravel-setup-action@v1
  with:
    php-version: "8.3"
```

### Use Default PHP Version

```yaml
- uses: endkind/laravel-setup-action@v1
```

---

## Features

- **Automatic PHP Installation**: Installs PHP via [php.new](https://php.new) on Linux and Windows runners
- **Version Flexibility**: Supports specifying any PHP version compatible with php.new
- **Composer Integration**: Automatically runs `composer install` if `composer.json` exists
- **Installation Verification**: Verifies PHP and Composer are correctly installed

---

## Examples

### Laravel CI/CD Pipeline

```yaml
name: Laravel CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP and Composer dependencies
        uses: endkind/laravel-setup-action@v1
        with:
          php-version: "8.3"

      - name: Run tests
        run: php artisan test
```

### Multi-Version Testing

```yaml
name: Multi-Version Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php-version: ["8.2", "8.3", "8.4"]
    
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP ${{ matrix.php-version }}
        uses: endkind/laravel-setup-action@v1
        with:
          php-version: ${{ matrix.php-version }}

      - name: Run tests
        run: php artisan test
```

### Windows Runner Support

```yaml
name: Windows Build

on: [push]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP on Windows
        uses: endkind/laravel-setup-action@v1
        with:
          php-version: "8.4"

      - name: Build application
        run: php artisan optimize
```

---

## Supported PHP Versions

The action supports all PHP versions available via [php.new](https://php.new). Common versions include:

- PHP 8.4 (default)
- PHP 8.3
- PHP 8.2
- PHP 8.1
- PHP 8.0

---

## Requirements

- GitHub Actions runner (Linux or Windows)
- Repository with a `composer.json` file (optional, but recommended for Laravel projects)

---

## Notes

- **macOS Support**: Currently not supported
- **Composer Install**: Only runs if `composer.json` is present in the repository root
- **php.new**: This action uses [php.new](https://php.new) for PHP installation

---

## Related Resources

- [GitHub Repository](https://github.com/Endkind/laravel-setup-action)
- [php.new Documentation](https://php.new)
- [Laravel Documentation](https://laravel.com/docs)

---
