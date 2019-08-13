def create_or_list_from(items: list) -> str:
    """
    Create a string like '"item1", "item2", or "item3"' from a list of items.
    """
    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return f'"{items[0]}"'
    elif len(items) == 2:
        return f'"{items[0]}" and "{items[1]}"'
    else:
        return _create_or_statement_from(items)


def _create_or_statement_from(items):
    result = '"'
    result += '", "'.join(items[:-1])
    result += f'", or "{items[-1]}"'
    return result
