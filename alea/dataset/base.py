import abc
import os
import shutil
import tempfile
from typing import Any, Dict

import filelock
import requests
from tqdm import tqdm

DATASET_CACHE_PATH = os.path.expanduser('~/.cache/alea/dataset')


def download(
    filepath: str, url: str, dataset_name: str,
    file_index: int, total_file_num: int,
    chunk_size=1024 * 1024,
):
  description = f'download {dataset_name} [{file_index+1}/{total_file_num}]'

  req = requests.get(url, stream=True)
  total_size = int(req.headers.get('content-length', 0))

  progressbar = tqdm(
    req.iter_content(chunk_size=chunk_size),
    desc=description, total=total_size,
    unit='B', unit_scale=True,
  )
  with open(filepath, 'wb') as fp:
    for data in progressbar:
      fp.write(data)
      progressbar.update(len(data))
    else:
      progressbar.close()


class Dataset(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_dataset_name(self) -> str:
    return 'youjo'

  @abc.abstractmethod
  def get_download_urls(self) -> Dict[str, str]:
    return {
      'youjo.npz': 'http://example.com/youjo.npz',
    }

  @abc.abstractmethod
  def load(self) -> Any:
    pass

  @abc.abstractmethod
  def convert(self, dir_src: str, dir_dest: str):
    pass

  def remove_cache(self):
    return shutil.rmtree(self.get_cache_path(), ignore_errors=True)

  def load_or_download(self):
    self.download_if_needed()
    return self.load()

  def get_cache_path(self):
    return os.path.join(DATASET_CACHE_PATH, self.get_dataset_name())

  def download_if_needed(self):
    dataset_dir = self.get_cache_path()
    dataset_name = self.get_dataset_name()

    os.makedirs(DATASET_CACHE_PATH, exist_ok=True)

    lock = filelock.FileLock(dataset_dir + '.lock')
    try:
      with lock:
        if not os.path.exists(dataset_dir):
          total_file_num = len(self.get_download_urls())
          with tempfile.TemporaryDirectory() as temp_td, \
              tempfile.TemporaryDirectory() as dest_td:
            for file_idx, (filename, url) in enumerate(self.get_download_urls().items()):
              tmp_filepath = os.path.join(temp_td, filename)
              download(tmp_filepath, url, dataset_name, file_idx, total_file_num)
            else:
              shutil.rmtree(dataset_dir, ignore_errors=True)
              self.convert(temp_td, dest_td)
              shutil.copytree(dest_td, dataset_dir)
    except Exception as exp:
      lock.release()
      raise exp
