# cattrs_basemodel
BaseModel for cattrs package which provide (un)structure methods to your models


# Usages:

```python
from cattrs_basemodel import BaseModel, define, field
# or import from attrs:
# from attrs import define, field


@define
class Point(BaseModel):
    x: int = field(default=0)
    y: int = field(default=0)


p = Point(1, 2)

json_ = p.unstructure()
print(json_)
p2 = Point.structure(json_)
print(p2)
```

## or define your own BaseModel:

```python
from cattrs_basemodel import BaseModelFactory, define, field
# or import from attrs:
# from attrs import define, field

MyBaseModel = BaseModelFactory("MyBaseModel", 
                               reg_alias=True,  # this and next fields are True by default 
                               reg_datetime=True)

@define
class Point(MyBaseModel):
    x: int = field(default=0)
    y: int = field(default=0)
```

# Converter and hooks:

```python
from cattrs_basemodel import BaseModel
print(BaseModel.converter)  # use like cattrs.Converter
```