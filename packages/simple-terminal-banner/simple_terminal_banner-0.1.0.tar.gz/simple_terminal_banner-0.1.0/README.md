# Simple Terminal Banner

![Build Status](https://github.com/charlbury/simple_terminal_banner/actions/workflows/python-package.yml/badge.svg)

```
** Simple Terminal Banner **************
*                                      *
*    Hello, World!                     *
*                                      *
****************************************
```

Display a simple terminal banner.

## Features

* Banner Title
* Themes
* Padding
* Margin
* Configurable border symbols
* Configurable background symbols

## Example

```python
from simple_terminal_banner import Banner

banner = Banner("Hello, World!")
banner.display()
```

Produces:

```
****************************************
*                                      *
* Hello, World!                        *
*                                      *
****************************************
```

## Titles

```
banner.title = "Banner Example"
```
Produces:
```
** Banner Example **********************
*                                      *
* Hello, World!                        *
*                                      *
****************************************
```

## Padding

### Title Padding

```
banner.title_padding = 4
```

Produces:

```
**    Banner Example    ****************
*                                      *
* Hello, World!                        *
*                                      *
****************************************
```

### Content Padding

```
banner.padding_top = 4
```

Produces:

```
**    Banner Example    ****************
*                                      *
*                                      *
*                                      *
*                                      *
* Hello, World!                        *
*                                      *
****************************************
```

## Configurable Symbols

### Border Symbols

```
banner.border_symbol = "="
```

Produces:

```
==    Banner Example    ================
=                                      =
=                                      =
=                                      =
=                                      =
= Hello, World!                        =
=                                      =
========================================
```

### Background Symbols

```
banner.background_symbol = "."
```

Produces:

```
```
