import unittest

from iiif_prezi3 import Collection, Manifest, Canvas, Range, LngString


class AddMetadataTest(unittest.TestCase):
    def setUp(self):
        self.collection = Collection();

    def test_add_metadata(self):
        self.collection.add_metadata("label", "value");
        assert isinstance(self.collection.metadata, list)
        assert self.collection.metadata[-1].label == LngString(__root__={'none': ['label']})
        assert self.collection.metadata[-1].value == LngString(__root__={'none': ['value']})
