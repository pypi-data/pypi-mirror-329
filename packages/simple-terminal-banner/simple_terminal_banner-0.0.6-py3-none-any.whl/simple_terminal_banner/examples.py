from simple_terminal_banner import Banner, BannerThemes

# create a simple banner showing the easiest possible
# way to have a quick and easy banner message displayed
banner = Banner("Hello, World!")
banner.display()

# create a banner that also has a title
titled_banner = Banner("This banner message has a title.")
titled_banner.title = "Banner with a title"
titled_banner.display()

# There are some pre-defined themes that can be used
# to change the look of the banner. Here are examples
# of all the available themes.
for index, theme in enumerate(BannerThemes):
    banner.theme(theme.value)
    banner.title = f"{index+1}. Theme: {theme.value.capitalize()}"
    banner.set_message(f"Theme name: {theme.value}")
    banner.display()

quit()

print(list(BannerThemes))
for theme in BannerThemes:
    print(theme.name)

basic_banner = Banner("Hello, World!")
basic_banner.title = "12345678901234567890123456789012345678901234567890"
basic_banner.title_padding = 0
basic_banner.title_margin = 0
basic_banner.display()
# quit()
banner = Banner("1234567890")
print()
banner.title = "Simple Terminal Banner"
banner.width = 40
banner.padding_left = 4
banner.padding_right = 4
banner.set_message("Hello, World!")
banner.display()
print()



multiline_banner = Banner()
multiline_banner.title = "Multiline Banner"
multiline_banner.width = 40
multiline_banner.padding_left = 4
multiline_banner.padding_right = 4
multiline_banner.margin_bottom = 1
multiline_banner.add_row("Hello, World!")
multiline_banner.add_row(type="blank")
multiline_banner.add_row("This is a multiline banner.")
multiline_banner.add_row("It can display multiple lines.")
multiline_banner.add_row(type="separator")
multiline_banner.add_row("This is the last line.")
multiline_banner.display()

no_border_banner = Banner()
no_border_banner.theme("none")
no_border_banner.title = "No Border, Margin or Padding, wrapped"
no_border_banner.width = 40
no_border_banner.add_row("Hello, World! This is the way you introduce most code examples in tutorials. It came from a book about C in the 1980s, but it's become a meme.")
no_border_banner.display()

no_border_banner.set_wrap(False)
no_border_banner.display()

no_padding_banner = Banner()
no_padding_banner.title = "No Margin or Padding, wrapped text"
no_padding_banner.width = 40
no_padding_banner.padding_left = 2
no_padding_banner.padding_right = 2
no_padding_banner.margin_bottom = 1
no_padding_banner.add_row("Hello, World! This is the way you introduce most code examples in tutorials. It came from a book about C in the 1980s, but it's become a meme.")
no_padding_banner.display()
