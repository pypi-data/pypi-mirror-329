import logging
from timeit import default_timer as timer
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
import difflib

from .update_page import update_page, is_excalidraw_md_file, is_excalidraw_included

logger = logging.getLogger('mkdocs.plugins.obsidian_excalidraw.plugin')

class ObsidianExcalidraw(BasePlugin):

    config_scheme = (
        ('FencePrefix', config_options.Type(str, default='kroki-')),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_files(self, files, config):
        prefix = self.config["FencePrefix"]
        removing_files = []
        for file in files:
            logger.debug(f"search for excalidraw-files: {file}")
            if is_excalidraw_md_file(file):
                removing_files.append(file)
                continue
            
            if file.src_path.endswith(".md") and is_excalidraw_included(file.content_string):
                markdown = file.content_string
                logger.debug(f"Markdown file found and excalidraw is included: {file}")
                path = file.abs_src_path
                file.content_string = update_page(markdown, file, prefix, config)
                file.abs_src_path = path
                logger.debug(f"Changes: {"".join(list(difflib.ndiff(markdown, file.content_string)))}")

        for f in removing_files:
            files.remove(f)
            logger.debug(f"Removing file from nav, because it is an excalidraw file: {f}")
        
        return files
