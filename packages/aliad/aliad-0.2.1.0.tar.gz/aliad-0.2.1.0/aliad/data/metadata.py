
from aliad.core import TaskType, DataType, StatDataType


class TabularFeature:

    name: str
    dtype: DataType
    sdtype: StatDataType
    index: int | Tuple[int, ...]
    shape : ...

class DatasetMetadata:

    name : str

    version : Optional[str] = None

    tasktype : TaskType

    supervised_keys: List[str]
    
    disable_shuffling
    
    features : Features

    data_format : str # tabular

    file_format : str

    citation : str

    url: str

    

    files = [
        {
            'name': '...',
            'metadata': {
            }
            'hash': '...',
            'split': None / 'train' / 'validation' / 'test'
            
        }
    ]



class Dataset:

    data: 
    metadata : DataSetMetadata

    def transform(...):
        pass

    def from_tensor_slices(...):
        pass

    def from_arrays(...):
        pass

tf.data.TextLineDataset(["file1.txt", "file2.txt"])

TFRecordDataset(["file1.tfrecords", "file2.tfrecords"])