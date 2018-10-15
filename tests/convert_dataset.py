from unittest import TestCase

import defia_core


class TestColab(TestCase):

    def test_convert_supervisely_to_yolo(self):
        defia_core.convert_supervisely_to_yolo('data/supervisely/Defi2-ImagesFournies', 'build/tests/yolo', (540, 540))





