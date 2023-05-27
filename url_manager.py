def add_http_prefix(url: str):
    # Add "http://" prefix to a string
    prefixed_url = "http://" + url
    return prefixed_url

def extract_url(url: str):
    # Extract the desired portion of a string
    slash_index = url.rfind("/")
    if slash_index:
        extracted_url = url[slash_index + 1:]
    else:
        extracted_url = url.split(".")[0]
    return extracted_url

def add_html_extension(url: str):
    # Add the .html extension in a string
    url += ".html"
    return url

def rename_file(url: str):
    # Extract the onion string, add the .html extension, and return the result
    # This has a result so that the name of the file is the same with the onion address

    if "http://" in url:
        url = url.replace("http://", "")

    onion_url = extract_url(url)
    filename = add_html_extension(onion_url)
    return filename

