import json
import os
from pathlib import Path

from django.conf import settings
from unittest import TestCase

from easys_ordermanager.v3.serializer import Serializer


class SerializerV3TestCase(TestCase):

    def test_validate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dev', 'tests', 'v3', 'example.json'), 'r') as f:
            fixture = json.load(f)
        s = Serializer(data=fixture)
        self.assertTrue(s.is_valid(raise_exception=True))

    def test_validate_existing_stroer_lp_example(self):
        example_path = Path(settings.BASE_DIR) / 'dev/tests/v3/existing_stroer_lp_example.json'
        with open(example_path) as file:
            fixture = json.load(file)
            serializer = Serializer(data=fixture)
            self.assertTrue(serializer.is_valid(raise_exception=True))
