def add_http_prefix(string: str):
    # Add "http://" prefix to a string
    prefixed_string = "http://" + string
    return prefixed_string

def extract_string(string: str):
    # Extract the desired portion of a string
    extracted_string = string.split(".")[0]
    return extracted_string

def add_html_extension(string: str):
    # Add the .html extension in a string
    string += ".html"
    return string

def add_http_prefix_in_the_onion_address(address: str):
    # Add "http://" prefix to the onion address and return the result
    modified_address = add_http_prefix(address)
    return modified_address

def rename_file(string: str):
    # Extract the onion string, add the .html extension, and return the result
    # This has a result so that the name of the file is the same with the onion address

    if "http://" in string:
        string = string.replace("http://", "")

    onion_string = extract_string(string)
    filename = add_html_extension(onion_string)
    return filename

def extract_filename(url):
    slash_index = url.rfind("/")
    filename = url[slash_index + 1:]
    return filename


def write_html_file(result, filename):
    with open(filename, 'w+', encoding='utf-8') as onion_html:
        onion_html.write(result)