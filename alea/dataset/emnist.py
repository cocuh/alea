import os
import zipfile

import numpy as np
from scipy.io import loadmat
from tqdm import tqdm

from alea.dataset.base import Dataset


class EmnistDataset(Dataset):
  '''emnist dataset
  
  >>> import alea.dataset from EmnistDataset
  >>> dataset = EmnistDataset()
  >>> npz = dataset.load_or_download()
  >>> npz['images_train'], npz['labels_train']
  >>> npz['images_test'], npz['labels_test']
  '''
  all_types = [
    'byclass',
    'bymerge',
    'balanced',
    'letters',
    'mnist',
  ]
  image_shape = (28, 28, 1)

  def __init__(self, dataset_type='byclass'):
    self.dataset_type = dataset_type.lower()
    assert self.dataset_type in self.all_types

  def get_dataset_name(self):
    return 'emnist'

  def get_download_urls(self):
    return {
      'matlab.zip': 'http://www.itl.nist.gov/iaui/vip/cs_links/EMNIST/matlab.zip'
    }

  def load(self):
    npz_path = os.path.join(self.get_cache_path(), f'{self.dataset_type}.npz')
    return np.load(npz_path)

  def convert(self, dir_temp: str, dir_dest: str):
    with zipfile.ZipFile(os.path.join(dir_temp, 'matlab.zip')) as zf:
      zf.extractall(dir_temp)

    progress = tqdm(self.all_types)
    for target_type in progress:
      progress.desc = f'processing {target_type}'
      progress.refresh()

      npz_path = os.path.join(dir_dest, f'{target_type}.npz')
      mat_path = os.path.join(
        dir_temp, 'matlab', f'emnist-{target_type}.mat'
      )
      data = loadmat(mat_path, struct_as_record=False)

      images_train = data['dataset'][0, 0].train[0, 0].images
      images_train = images_train.reshape(images_train.shape[0], *self.image_shape)  # N x W x H x C
      images_train = np.swapaxes(images_train, 1, 2)  # N x H x W x C
      labels_train = data['dataset'][0, 0].train[0, 0].labels

      images_test = data['dataset'][0, 0].test[0, 0].images  # N x W x H x C
      images_test = images_test.reshape(images_test.shape[0], *self.image_shape)  # N x W x H x C
      images_test = np.swapaxes(images_test, 1, 2)  # N x H x W x C
      labels_test = data['dataset'][0, 0].test[0, 0].labels

      np.savez(
        npz_path,
        images_train=images_train,
        labels_train=labels_train,
        images_test=images_test,
        labels_test=labels_test,
      )
