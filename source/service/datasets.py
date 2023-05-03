"""
Defines class that hides the logic/path for saving and loading specific datasets
used across this project, as well as providing a brief description for each dataset.

To define a new dataset, create a property in Datasets.__init__() following the existing patthern.

The DATA variable is assigned an instance of the Datasets class and can be imported into other
scripts/notebooks.

To load the dataset called `the_dataset`, use the following code:

```
from source.services.data import DATA
df = DATA.the_dataset.load()
```

To save the dataset called `the_dataset`, use the following code:

```
from source.services.data import DATA

df = ...logic..
DATA.the_dataset.save(df)
```
"""
import source.config.config as config
from source.library.dataset_types import DatasetsBase, PickledDataLoader


class Datasets(DatasetsBase):
    """Defines the datasets available to the project."""

    def __init__(self) -> None:
        # define the datasets before calling __init__()
        self.langchain_docs = PickledDataLoader(
            description="scaped langchain docs",
            dependencies=[],
            directory=config.DIR_DATA_RAW,
            cache=False,
        )
        self.langchain_doc_chunks = PickledDataLoader(
            description="langchain docs scaped and chunking underlying text + processing",
            dependencies=['langchain_docs'],
            directory=config.DIR_DATA_PROCESSED,
            cache=False,
        )
        # call __init__() after defining properties
        super().__init__()


# create a global object that can be imported into other scripts
DATA = Datasets()

# ensure all names got set properly
assert all(getattr(DATA, x).name == x for x in DATA.datasets)
