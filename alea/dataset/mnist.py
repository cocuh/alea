import os
from alea.dataset.base import Dataset
import numpy as np


class MnistDataset(Dataset):
  image_shape = (28, 28, 1)

  def __init__(self):
    pass

  def get_dataset_name(self):
    return 'mnist'

  def get_download_urls(self):
    return {
      'mnist.npz': 'https://s3.amazonaws.com/img-datasets/mnist.npz',
    }

  def load(self):
    npz_path = os.path.join(self.get_cache_path(), f'mnist.npz')
    return np.load(npz_path)

  def convert(self, dir_temp: str, dir_dest: str):
    input_npz_path = os.path.join(dir_temp, 'mnist.npz')
    output_npz_path = os.path.join(dir_dest, 'mnist.npz')

    data = np.load(input_npz_path)
    np.savez(
      output_npz_path,
      images_train=data['x_train'],
      labels_train=data['y_train'],
      images_test=data['x_test'],
      labels_test=data['y_test'],
    )