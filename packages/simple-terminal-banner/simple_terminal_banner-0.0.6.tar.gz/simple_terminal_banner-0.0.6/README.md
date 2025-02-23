# Simple Terminal Banner

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
* Configurable border symbols
* Configurable background symbols

## Example

```python
from banner import Banner

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