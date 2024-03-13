from os.path import join
import os
from .Derivative import Derivative
from .Fragments import Fragments


class SVFReader:
    def __init__(self, urn, token, region="US"):
        self.urn = urn
        self.token = token
        self.region = region
        self.derivative = Derivative(self.urn, self.token, self.region)

    def read_sources(self):
        resources = self.derivative.read_svf_resource()
        return resources

    def read_svf_manifest_items(self):
        items = self.derivative.read_svf_manifest_items()
        return items

    def read_fragments(self, manifest_item=None)->dict:
        fragments = {}
        if manifest_item:
            resources = self.derivative.read_svf_resource_item(manifest_item)
            for resource in resources:
                if resource.local_path.endswith("FragmentList.pack"):
                    bytes_io = self.derivative.download_stream_resource(resource)
                    buffer = bytes_io.read()
                    frags = Fragments.parse_fragments(buffer)
                    fragments[manifest_item.guid] = frags
        else:
            fragments = Fragments.parse_fragments_from_urn(self.urn, self.token, self.region)
        return fragments
    def _read_contents(self):
        # TODO :
        pass

    def download(self, output_dir):
        resources = self.read_sources()
        for resource in resources:
            localpath = resource.local_path
            combined_path = join(output_dir, localpath)
            if not os.path.exists(os.path.dirname(combined_path)):
                os.makedirs(os.path.dirname(combined_path))
            self.derivative.download_resource(resource, combined_path)
