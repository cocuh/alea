from unittest import TestCase

from nose.plugins.attrib import attr


class TestEmnist(TestCase):
  @attr(speed='slow')
  def test_it(self):
    from alea.dataset.emnist import EmnistDataset
    dataset = EmnistDataset()
    dataset.remove_cache()
    dataset.load_or_download()
