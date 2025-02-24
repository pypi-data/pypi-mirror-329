from typing import List, Tuple, Union
import numpy as np
import torch
from torch.utils.data import Dataset

from model_wrapper.utils import is_float


class ListDataset(Dataset[Tuple[List, ...]]):
	r"""Dataset wrapping List.
    可以配合ListTensorCollector使用
	Each sample will be retrieved by indexing list.

	Args:
		*lists (List): lists that have the same length.
	"""
	
	def __init__(self, *lists: Union[List, np.ndarray]) -> None:
		assert all(len(lists[0]) == len(sub_list) for sub_list in lists), "Size mismatch between tensors"
		self.lists = lists
	
	def __getitem__(self, index):
		if len(self.lists) == 1:
			return self.lists[0][index]
		return tuple(sub_list[index] for sub_list in self.lists)
	
	def __len__(self):
		return len(self.lists[0])
	

class ListTensorCollector:
	""" 可以有多列数据 
	配合ListDataset使用
	"""
	
	def __init__(self, *dtypes: torch.dtype):
		if dtypes:
			self.dtypes = dtypes[0] if len(dtypes) == 1 and isinstance(dtypes[0], (tuple, list)) else dtypes
		else:
			self.dtypes = None
	
	def __call__(self, batch):
		batch = (x for x in zip(*batch))
		if self.dtypes:
			return tuple(torch.tensor(x, dtype=self.dtypes[i]) for i, x in enumerate(batch))
		
		return tuple(torch.tensor(x if isinstance(x, np.ndarray) else np.array(x), dtype=torch.float if is_float(x[0]) else torch.long) for x in batch)
	

if __name__ == '__main__':
	import numpy as np
	from torch.utils.data import DataLoader

	X1 = np.random.randn(8, 3)
	X2 = np.random.randn(8, 2)
	y = np.random.randint(0, 2, 8)
	
	dataset = ListDataset(X1, X2, y)
	dataloader = DataLoader(dataset, batch_size=4, collate_fn=ListTensorCollector([torch.float16, torch.float64, torch.long]))
	for d in dataloader:
		print(d[0].dtype, d[1].dtype, d[2].dtype)
