# py-asset-loader

Override the provided classes and implement your assets folder.

## Examples:

* You have multiple Python classes deriving from another python class that extend it, but aren't directly referenced by your code.

```
/project
|- task.py
|- task_list.py
/assets
  /tasks
  |- write_hello_world_every_minute.py # is descendant of a class from task.py
  |- daily_plan_for_world_dominance.py # is descendant of a class from task.py
  |- monthly_defeat_the_demon_king.py # is descendant of a class from task.py
```

* You have multiple yaml/json-Files that describe a workflow or a class in your code

```
/project
|- table.py
/assets
  /db_tables
  |- customer.yaml
  |- article.yaml
  |- shop.yaml
```

## Usage 1 - use the existing templates for Yaml/JSON/Py Files

### Yaml/JSON

* Override `YamlAsset`/`JSONAsset`.
    * you can access the `self.source` object for information retrieval.
    * I recommend you to make @properties for retrieving the information for cleaner code.
* Override `YamlAssetLoader[T]`/`JSONAssetLoader[T]` with your `YamlAsset`/`JSONAsset` derivative
    * define the `asset_folder_name()` and `asset_class()` methods.
* Create your yaml/json files inside the folder */assets/<asset_folder_name()>/
```py
class MyTable(YamlAsset):
    @property
    def some_field(self):
        return self.source.get("some_field")

class MyTables(YamlAssetLoader[MyTable]):
    @override
    def asset_class(self) -> Type[MyTable]: return MyTable
    @override
    def asset_folder_name(self) -> str: return 'db_tables'
```

### Python

* Override `PythonAsset` with your base Python class.
    * define the classmethod `base_asset_class_name` to return the class name of your main derivative.
    * define your properties and methods that you want to override in your asseted classes.
* Override `PythonAssetLoader[T]` with your `PythonAsset` derivative and define the `asset_folder_name()` method.
* Create your python files inside the folder */assets/<asset_folder_name()>/
    * These modules will only be loaded regardless of wheter they contain a derivative of your `PythonAsset` derivative or not.
    * The derivatives are automatically instantiated and added into your Loader's `loaded_assets`.

```py
class Task(PythonAsset):
    @abstractmethod
    def type(self) -> Enum: ...
    @abstractmethod
    async def execute(self) -> any:

class Tasks(PythonAssetLoader[Task]):
    @override
    def asset_folder_name(self) -> str: return 'tasks'

    def get_task(self, type: Enum) -> Task:
        return next([task for task in self.loaded_assets if task.type() == type])

assets/tasks/daily_plan_for_world_dominance.py
...

class PlanForWorldDominance(Task):
    @override
    def type(self) -> Enum: return ...
    @override
    async def execute(self) -> any: print('veni vidi vici')
```

## Usage 2 - implement your own loader

* Simply override the `LoadedAsset` and the `AssetLoader` in a similar manner to the existing derivatives.