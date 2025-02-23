# filepath: /Users/sjg/tmp/simple_terminal_banner/tests/test_banner.py
import unittest
from simple_terminal_banner import Banner, BannerThemes

class TestBanner(unittest.TestCase):

    def test_banner_creation(self):
        banner = Banner("Hello, World!")
        self.assertEqual(banner.message, "Hello, World!")

    def test_no_message(self):
        banner = Banner()
        banner.display()
        self.assertIsNone(banner.message)

    def test_banner_display(self):
        banner = Banner("Hello, World!")
        banner.display()
        # Since display prints to the console, you might want to capture stdout and assert its content

    def test_banner_title(self):
        banner = Banner("Hello, World!")
        banner.title = "Test Title"
        self.assertEqual(banner.title, "Test Title")

    def test_banner_themes(self):
        theme_symbols = {
                'default': '*',
                'simple': '-',
                'hash': '#',
                'star': '*',
                'space': ' ',
                'none': ''}
        banner = Banner("Hello, World!")
        for theme in BannerThemes:
            banner.theme(theme.value)
            self.assertEqual(banner.border_symbol, theme_symbols[theme.value])

    def test_multiline_banner(self):
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
        # Capture stdout and assert its content if needed

    def test_set_title(self):
        banner = Banner()
        banner.title = "Test Title"
        self.assertEqual(banner.title, "Test Title")

    def test_set_theme(self):
        banner = Banner()
        banner.theme("hash")
        self.assertEqual(banner.border_symbol, "#")
        self.assertEqual(banner.background_symbol, " ")
        self.assertEqual(banner.padding_symbol, " ")

    def test_add_row(self):
        banner = Banner()
        banner.add_row("Test Row")
        self.assertIn("Test Row", banner._rows[0])

    def test_padding_and_margins(self):
        banner = Banner()
        banner.padding_top = 2
        banner.padding_bottom = 2
        banner.margin_top = 1
        banner.margin_bottom = 1
        self.assertEqual(banner.padding_top, 2)
        self.assertEqual(banner.padding_bottom, 2)
        self.assertEqual(banner.margin_top, 1)
        self.assertEqual(banner.margin_bottom, 1)

    def test_different_widths(self):
        banner = Banner()
        banner.width = 50
        self.assertEqual(banner.width, 50)

    def test_multiline_content(self):
        banner = Banner()
        banner.add_row("This is a long line that should be wrapped if the width is too small.")
        self.assertTrue(len(banner._rows) > 1)


if __name__ == '__main__':
    unittest.main()