"""
theme.py

Code for registering and interacting with themes.
"""

import pyhtml as p


class Theme:
    def make_slide(self, slide_content: p.Tag) -> p.Tag:
        """
        Given the HTML content for a slide, return the HTML to use for the
        slide.
        """
        return slide_content

    def make_slide_selector(self, slides: list[str]) -> p.Tag:
        """
        Given a list of slides, return HTML for a slide picker.
        """
        return NotImplemented
