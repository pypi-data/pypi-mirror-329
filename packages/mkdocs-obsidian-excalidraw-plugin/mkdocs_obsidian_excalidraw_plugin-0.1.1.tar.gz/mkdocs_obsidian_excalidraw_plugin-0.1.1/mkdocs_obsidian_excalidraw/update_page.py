from mkdocs.structure.nav import Page
from mkdocs.structure.files import File
import logging
import re
import os
from urllib.parse import unquote

logger = logging.getLogger('mkdocs.plugins.obsidian_excalidraw.update_page')

COMPRESSED_START_STRING = "```compressed-json"
START_STRING = "```json"
IMAGE_PATTERN = r'!\[\[(.*?)\.excalidraw\]\]'

def is_excalidraw_included(markdown) -> bool:
    return re.search(IMAGE_PATTERN, markdown) is not None

def is_excalidraw_md_file(file) -> bool:
    if isinstance(file, Page):
        return is_excalidraw_md_file(file.file)
    if isinstance(file, File):
        return is_excalidraw_md_file(file.src_uri)
    if isinstance(file, str):
        return file.endswith(".excalidraw.md")
    
def is_excalidraw_compressed(markdown) -> bool:
    return COMPRESSED_START_STRING in markdown

def get_start_string(markdown) -> bool:
    if is_excalidraw_compressed(markdown):
        return COMPRESSED_START_STRING
    return START_STRING

def find_start_end_position(markdown):
    start_string = get_start_string(markdown)
    start_index = markdown.find(start_string) + len(start_string)
    stop_index = markdown.rfind("```")
    return start_index, stop_index

def parse_excalidraw(file, prefix, config):
    logger.debug(f"got file: {file}")
    if not is_excalidraw_md_file(file):
        logger.error(f"file was not an excalidraw markdown file")
        return ""
    
    with open(file) as f:
        markdown = f.read()

    excalidraw_json = ""
    
    start_index, stop_index = find_start_end_position(markdown)
    slice_content = markdown[start_index:stop_index]
    if is_excalidraw_compressed(markdown):
        logger.warning(f"Found compressed embedded excalidraw: {file}. Disable compression in obsidian settings Excalidraw Plugin -> Saving -> `Compress Excalidraw JSON in Markdown`")
    excalidraw_json = slice_content

    logger.error(f"json: {excalidraw_json}" )
    
    return f"""```{prefix}excalidraw
{excalidraw_json}
```"""

def find_and_replace_excalidraw_images(markdown, file, prefix, config):
    content = re.sub(IMAGE_PATTERN, replace_excalidraw_includes(file, prefix, config), markdown)
    logger.info(f"excalidraw content {content}, got {markdown}")
    return content

def replace_excalidraw_includes(file, prefix, config):
    def replace(match):
        image_path = match.group(1)
        logger.debug(f"Found excalidraw reference: {image_path}")
        href = f"{image_path}.excalidraw.md" # obsidian left out the type extension! And we stripped out away the excalidraw stuff before.
        count_slashes = len(href.split("../"))
        directories: list = []
        directories = unquote(file.src_uri).split("/")
        
        for _ in range(count_slashes):
            directories.pop()

        directories.extend(href.replace("../", "").split("/"))
        href = "docs/" + "/".join(directories)
        logger.debug(f"directories: {href}")
        
        logger.debug(f"Found absolute link for {href}")

        # TODO get excalidraw markdown file content
        if not os.path.exists(href):
            logger.error(f"Excalidraw file {href} not exists.")
            return f"![[{image_path}.excalidraw]]"
        
        return parse_excalidraw(href, prefix, config)

    return replace

def update_page(markdown, file, prefix, config):
    return find_and_replace_excalidraw_images(markdown, file, prefix, config)

