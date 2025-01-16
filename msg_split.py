from bs4 import BeautifulSoup

class FragmentTooLargeError(Exception):
    def __init__(self, message, element=None):
        super().__init__(message)
        self.element = element


def split_html_structure(html_content, max_len=1000):
    soup = BeautifulSoup(html_content, "html.parser")

    fragments = []
    current_fragment = ""
    tag_stack = []

    def close_tags(fragment, stack):
        for tag in reversed(stack):
            fragment += f"</{tag}>"
        return fragment

    def reopen_tags(fragment, stack):
        for tag in stack:
            fragment += f"<{tag}>"
        return fragment

    def can_split(tag):
        return tag.name in {"p", "b", "strong", "i", "ul", "ol", "div", "span"}

    def process_element(element, current_fragment, tag_stack):
        nonlocal fragments

        if element.name:
            if can_split(element):
                tag_stack.append(element.name)
                opening_tag = f"<{element.name}>"
                closing_tag = f"</{element.name}>"

                if len(opening_tag) + len(closing_tag) > max_len:
                    raise FragmentTooLargeError(
                        f"Тег <{element.name}> слишком велик для max_len ({max_len} символов).", element
                    )

                if len(current_fragment) + len(opening_tag) + len(closing_tag) > max_len:
                    current_fragment = close_tags(current_fragment, tag_stack[:-1])
                    fragments.append(current_fragment)
                    current_fragment = reopen_tags("", tag_stack[:-1]) + opening_tag
                else:
                    current_fragment += opening_tag

                for child in element.contents:
                    current_fragment = process_element(child, current_fragment, tag_stack)

                current_fragment += closing_tag
                tag_stack.pop()
            else:
                element_str = str(element)
                if len(element_str) > max_len:
                    raise FragmentTooLargeError(
                        f"Элемент {element} слишком велик для max_len ({max_len} символов).", element
                    )

                if len(current_fragment) + len(element_str) > max_len:
                    current_fragment = close_tags(current_fragment, tag_stack)
                    fragments.append(current_fragment)
                    current_fragment = reopen_tags("", tag_stack)
                current_fragment += element_str

        else:
            text = str(element)

            if len(text) > max_len:
                raise FragmentTooLargeError(
                    f"Текстовый элемент слишком велик для max_len ({max_len} символов): {text[:50]}...", text
                )

            if len(current_fragment) + len(text) > max_len:
                current_fragment = close_tags(current_fragment, tag_stack)
                fragments.append(current_fragment)
                current_fragment = reopen_tags("", tag_stack) + text
            else:
                current_fragment += text

        return current_fragment

    for child in soup.contents:
        current_fragment = process_element(child, current_fragment, tag_stack)

    if current_fragment:
        current_fragment = close_tags(current_fragment, tag_stack)
        fragments.append(current_fragment)

    return fragments
