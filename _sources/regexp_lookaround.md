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

环视(regexp)
============================

## 环视

```text
环视是一种非捕获分组，它根据某个模式之前或之后的内容匹配其他模式。环视也 称为零宽度断言。
同样是零宽度断言的还有有`\b`(匹配单词边界),`^`(匹配一行的开头),`$`(匹配一行的结尾)
```

```{code-cell} ipython3
import re
```

### 正前瞻(?=pattern)

```{code-cell} ipython3
import re
test = "prefix123suffix"
# 现在我们的需求是在prefix和123之间加一个_分隔一下
# 正前瞻(?=pattern)的意思是:和普通的pattern一样,但是它只是匹配出pattern的前边的一个位置,但是并不消耗掉任何字符
# 所以我们首先要找到123这个pattern,然后直接用正前瞻找到123前边的那个位置,然后直接用_替换掉那个位置就完成了需求
pattern = r'(?=123)'
print(re.sub(pattern,"_",test))
```

### 正后顾(?<=pattern)

```{code-cell} ipython3
import re
# 后顾和前瞻其实差别就是前瞻匹配的是pattern前边的位置，后顾是pattern后边的位置
# 所以如果我们的需求是在123和suffix之间加一个_分割一下
# 那我们只需要把前瞻语法改为后顾语法就行
test = "prefix123suffix"
pattern = r'(?<=123)'
print(re.sub(pattern,"_",test))
```

### 反前瞻(?!pattern)

```{code-cell} ipython3
import re
# 反前瞻就是正前瞻的否定
# 比如我们之前的(?=123)匹配的是123前边的那个位置
# (?!123)则匹配的是非123前边的位置,对于prefix123suffix这个case来说，位置就比较多了。
# 简单起见，我们这里把case改为a123b,那么(?!(123))则匹配了不是123这个pattern的前边的位置,如果在这些位置用_填充的话，结果为_a1_2_3_b_
test = "a123b"
pattern = r'(?!123)'
print(re.sub(pattern,"_",test))
```

### 反后顾(?<!pattern)

```{code-cell} ipython3
import re
# 反后顾就是正后顾的否定
# 同样的，我们这里case为a123b,那么(?<!(123))则匹配了不是123这个pattern的后边的位置,如果在这些位置用_填充的话，结果为_a_1_2_3b_
test = "a123b"
pattern = r'(?<!123)'
print(re.sub(pattern,"_",test))
```

## 总结
```text
正前瞻和正后顾因为是对pattern的肯定,所以用的时候和一般的pattern差不太多。
反前瞻和反后顾由于是对pattern的否定,所以一般会在前边或者后边搭配其他一些pattern使用。不然匹配的位置就太多了一些
```