def print_and_write_to_file(text, file_path):
    """Write the given string to a file at the given filepath"""
    print(text)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f'Report successfully written to file at {file_path}')
    except FileNotFoundError as e:
        print(f'Unable to write results to file. {str(e)}')

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
