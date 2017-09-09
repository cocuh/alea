from unittest import TestCase, SkipTest


def setupModule():
  raise SkipTest

class TestEmnist(TestCase):
  def test_it(self):
    from alea.dataset.emnist import EmnistDataset
    dataset = EmnistDataset()
    dataset.remove_cache()
    dataset.load_or_download()
