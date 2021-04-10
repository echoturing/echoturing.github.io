---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

Python的Dataclasses
==================

## 前言

如果你经常通过使用`class`的方式抽象的话，就会发现一个问题，你会经常写一些冗余的代码块。
比如`__init__`,`__repr__`等等。  
`Dataclasses`在Python3.7被引入，提供了一个更简单的方式来创建`class`。



## Python Dataclass example

```{code-cell} python3
class Book:
    def __init__(self, name: str, weight: float, shelf_id: int = 0):
        self.name = name
        self.weight = weight
        self.shelf_id = shelf_id

    def __repr__(self):
        return f"Book(name={self.name!r},weight={self.weight!r}, shelf_id={self.shelf_id!r})"

print(Book('name book', 10))
```

如果你只写这一个的话，好像没什么不妥，但是如果你要写好多个class，你就会发现每一个`__init__`方法你都需要把参数挨个的赋值给自己的属性  
但是如果你用`Dataclass`,那么代码就变成下边的样子了

```{code-cell} python3
from dataclasses import dataclass

@dataclass
class Book:
    name: str
    weight: float 
    shelf_id: int = 0
    
print("`注意`:当你在dataclass里面添加属性定义的时候，`@dataclass`装饰器会自动生成对应的`__init__`方法，并且该方法还保留了类型注解。")
print(Book('name book', 10))

```

### field
上边的例子在大部分情况下就够用了，但是有时候你想自定义一下默认值，这时候你可以使用`field`

```{code-cell} python3

from dataclasses import dataclass, field
from typing import List

@dataclass
class Book:
    name: str     
    condition: str = field(compare=False) 
    weight: float = field(default=0.0, repr=False)
    shelf_id: int = 0
    chapters: List[str] = field(default_factory=list) # 这里保证每个Book实例的chapters字段都是一个新的list

```

### __post_init__
如果你有更复杂的定制，那你可以使用 `__post_init__`

```{code-cell} python
from dataclasses import dataclass, field, InitVar
from typing import List

@dataclass
class Book:
    name: str     
    condition: InitVar[str] = None
    weight: float = field(default=0.0, repr=False)
    shelf_id: int = field(init=False)
    chapters: List[str] = field(default_factory=list)

    def __post_init__(self, condition):
        if condition == "Discarded": 
            self.shelf_id = None
        else:
            self.shelf_id = 0

print(Book("book"))
```

## FAQ

### 1.什么时候使用dataclass?

`dataclass`的一个常用方式就是替换 `namedtuple`，它们都可以创建不可变对象，`@dataclass(frozen=True)`。

另一个用途就是用来替换嵌套的`dict`

