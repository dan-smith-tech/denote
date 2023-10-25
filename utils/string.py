import re


def apply_substitutions(string, substitutions):
    new_string = string

    for pattern, replacement in substitutions:
        new_string = re.sub(re.compile(re.escape(pattern)), replacement, new_string)

    return new_string


def escape_lines(string):
    lines = string.split("\n")
    processed_lines = []

    for line in lines:
        match = re.compile(r'^([a-z].*)$').match(line)

        if match:
            if len(processed_lines) > 0:
                processed_lines[-1] += ' ' + match.group(1)
            else:
                processed_lines.append(match.group(1))
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)


def title_page(string, page_index):
    new_string = ""

    if len(string.strip()) > 0:
        if page_index == 0:
            new_string = "\n# " + string + "\n"
        else:
            new_string = "\n## " + string + "\n"

    return new_string
