import json
import os

from hatchling.metadata.plugin.interface import MetadataHookInterface

class JSONMetaDataHook(MetadataHookInterface):
    def update(self, metadata):
        src_file = os.path.join(self.root, "src", "dtcoords", "VERSION")
        with open(src_file) as src:
            metadata["version"] = src.read().strip()
