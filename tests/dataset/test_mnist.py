from unittest import TestCase

from nose.plugins.attrib import attr


class TestMnist(TestCase):
  @attr(speed='slow')
  def test_it(self):
    from alea.dataset.mnist import MnistDataset
    dataset = MnistDataset()
    dataset.remove_cache()
    dataset.load_or_download()
