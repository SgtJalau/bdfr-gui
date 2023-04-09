def split_lines(text: str, max_characters_per_line: int) -> str:
    """
    Split a string into multiple lines if any of the lines are too long.
    :param text: The text to split
    :param max_characters_per_line: The maximum number of characters per line
    :return: The text with new lines inserted
    """

    # Split the text into lines
    lines = text.splitlines()

    new_lines = []

    # Split the lines into multiple lines if they are too long
    for i in range(len(lines)):
        line = lines[i]
        new_lines.extend(split_line(line, max_characters_per_line))

    # Join the lines back together
    return "\n".join(new_lines)


def split_line(line: str, max_characters_per_line: int) -> []:
    """
    Split a line into multiple lines if it is too long. Recursively splits the line if it is still too long.
    :param line:  The line to split
    :param max_characters_per_line: The maximum number of characters per line
    :return: A list of lines
    """
    if len(line) <= max_characters_per_line:
        return [line]

    # Split the line at the next space after the max characters
    split_index = line.rfind(" ", 0, max_characters_per_line)
    if split_index == -1:
        # No space found, split at the max characters
        split_index = max_characters_per_line

    # Split the line
    lines = [line[:split_index]]

    # Recursively split the rest of the line
    lines.extend(split_line(line[split_index + 1:], max_characters_per_line))

    return lines
