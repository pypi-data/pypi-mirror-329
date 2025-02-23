from enum import Enum
import logging
import textwrap


class BannerThemes(Enum):
    DEFAULT = 'default'
    SIMPLE = 'simple'
    HASH = 'hash'
    STAR = 'star'
    SPACE = 'space'
    NONE = 'none'


# create a simple class to create a banner
class Banner:
    def __init__(self, message=None):

        self.title = None
        self.title_padding = 1
        self.title_margin = 1
        self.width = 40
        self.wrap = True
        self.padding_top = 1
        self.padding_bottom = 1
        self.padding_left = 1
        self.padding_right = 1
        self.margin_top = 0
        self.margin_bottom = 1
        self.margin_left = 0
        self.margin_right = 0
        self.border_symbol = "*"
        self.background_symbol = " "
        self.padding_symbol = " "

        self._rows = []
        self._border_width = 1

        if message:
            self.add_row(message)
        self.message = message

    def display(self):
        if self.margin_top > 0: print(self._create_margin_top())
        print(self._title())
        print(self._create_padding_top())
        if self._rows:
            for row in self._rows:
                print(row)
        else:
            print(self._line(self.message))
        print(self._create_padding_bottom())
        print(self._separator())
        if self.margin_bottom > 0: print(self._create_margin_bottom())

    def add_row(self, content=None, type=None):
        if type in ['blank', 'empty', 'line']:
            self._rows.append(self._blank_line())
        elif type in ['separator', 'divider']:
            self._rows.append(self._create_padding_top())
            self._rows.append(self._separator())
            self._rows.append(self._create_padding_bottom())
        else:
            # content = self._check_content_length(content)
            self._line(content)

        return

    def set_message(self, message):
        self._rows = []
        self.add_row(message)

    def set_wrap(self, wrap):
        # if wrap is changed, we need to reprocess any existing rows
        # to calculate the correct wrapping
        self.wrap = wrap

    def theme(self, theme_name):
        if theme_name == "default":
            self.border_symbol = "*"
            self.background_symbol = " "
            self.padding_symbol = " "
        elif theme_name == "simple":
            self.border_symbol = "-"
            self.background_symbol = " "
            self.padding_symbol = " "
        elif theme_name == "hash":
            self.border_symbol = "#"
            self.background_symbol = " "
            self.padding_symbol = " "
        elif theme_name == "star":
            self.border_symbol = "*"
            self.background_symbol = " "
            self.padding_symbol = " "
        elif theme_name == "space":
            self.border_symbol = " "
            self.background_symbol = " "
            self.padding_symbol = " "
        elif theme_name == "none":
            self.border_symbol = ""
            self.background_symbol = ""
            self.padding_symbol = ""
            self.title_padding = 0
            self.title_margin = 0
        else:
            self.border_symbol = "*"
            self.background_symbol = " "
            self.padding_symbol = " "

    def _line(self, content):
        checked_content_list = self._check_content_length(content)

        for checked_content in checked_content_list:
            self._rows.append(
                self._create_row(checked_content)
            )

    def _create_row(self, content):
        return (
            f"{self.border_symbol}"
            f"{self.padding_symbol * self.padding_left}"
            f"{content}"
            f"{self.background_symbol * int(self.width-len(content)-self.padding_left-self.padding_right-2)}"
            f"{self.padding_symbol * self.padding_right}"
            f"{self.border_symbol}"
        )

    def _check_content_length(self, content):
        checked_content_list = []
        if len(content) > self.width - \
            (self.padding_left + self.padding_right) - \
            (self._border_width * 2):
            if self.wrap:
                checked_content_list = textwrap.wrap(
                    content,
                    width=self.width-(self.padding_left+self.padding_right+(self._border_width*2)))
                # for line in wrapped_content:
                #     self.add_row(line)
            else:
                checked_content_list.append(content[:self.width-(self.padding_left+self.padding_right+(self._border_width*2))])
        else:
            checked_content_list.append(content)
        return checked_content_list

    def _title(self):
        if self.title is None or self.title == "":
            return self._separator()

        if len(self.title) > self.width - (self._border_width * 2) - (self.title_margin * 2) - (self.title_padding * 2):
            logging.warning(f"Title is too long ({len(self.title)} chars) and has been truncated to fit banner: Total width:{self.width}, Title margin {self.title_margin * 2}, Title padding {self.title_padding * 2}, Allowed Title Length:{self.width-(self.title_margin*2)-(self.title_padding*2)}.")
            self.title = self.title[:self.width-(self._border_width*2)-(self.title_margin*2)-(self.title_padding*2)]

        return (
            f"{self.border_symbol}"
            f"{self.border_symbol * self.title_margin}"
            f"{' ' * self.title_padding}"
            f"{self.title}"
            f"{' ' * self.title_padding}"
            f"{self.border_symbol * self.title_margin}"
            f"{self.border_symbol * int(self.width-len(self.title)-(self._border_width*2)-(self.title_padding*2)-(self.title_margin*2))}"
            f"{self.border_symbol}"
        )

    def _separator(self):
        return self.border_symbol * self.width

    def _create_padding_top(self):
        padding_lines = ""
        for i in range(self.padding_top):
            padding_lines += self._padding_line() + "\n"

        # remove the last newline character
        return padding_lines[:-1]

    def _create_padding_bottom(self):
        padding_lines = ""
        for i in range(self.padding_bottom):
            padding_lines += self._padding_line() + "\n"

        # remove the last newline character
        return padding_lines[:-1]

    def _create_margin_top(self):
        margin_lines = ""
        for i in range(self.margin_top):
            margin_lines += "\n"

        return margin_lines

    def _create_margin_bottom(self):
        margin_lines = ""
        for i in range(self.margin_bottom):
            margin_lines += "\n"

        return margin_lines

    def _padding_line(self):
        return self.border_symbol \
            + self.padding_symbol * self.padding_left \
            + self.padding_symbol * (self.width - 2 - self.padding_left - self.padding_right) \
            + self.padding_symbol * self.padding_right \
            + self.border_symbol

    def _blank_line(self):
        return self.border_symbol \
            + self.padding_symbol * self.padding_left \
            + self.background_symbol * (self.width - 2 - self.padding_left - self.padding_right) \
            + self.padding_symbol * self.padding_right \
            + self.border_symbol
