from unittest import SkipTest, TestCase


def setupModule():
  raise SkipTest


class TestMnist(TestCase):
  def test_it(self):
    from alea.dataset.mnist import MnistDataset
    dataset = MnistDataset()
    dataset.remove_cache()
    dataset.load_or_download()
