from typing import List

def read_from_file(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return []
    except IOError as e:
        print(f"An error occurred while reading the file {filename}: {e}")
        return []


def write_to_file(lines: List[str], filename: str):
    try:
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def write_html_file(result: str, filename: str):
    try:
        with open(filename, 'w+', encoding='utf-8') as onion_html:
            onion_html.write(result)
            print(f'{filename} wrote successfully!')
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
