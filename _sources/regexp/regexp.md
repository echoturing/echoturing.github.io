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

正则表达式(regexp)
============================

## 匹配中文

> 匹配中文字符的正则表达式： [\u4e00-\u9fa5]
> 匹配双字节字符(包括汉字在内)：[^\x00-\xff]

```{code-cell} ipython3
import re
unicodeRegexp = re.compile(r'[\u4e00-\u9fa5]+')
multiByteRegexp = re.compile(r'[^\x00-\xff]+')
test1 = "xxx这是中文xxx😿"
print("中文字符匹配",unicodeRegexp.findall(test1))
print("多字节字符匹配(emoji表情是多字节,不在中文编码里面)",multiByteRegexp.findall(test1))
```

## 逻辑表达式

### 与

```{code-cell} ipython3
# 常规正则默认都是逻辑与
# 比如你有两个pattern:foo和bar
# 则这两个pattern组合在一起的时候:(foo)(bar)则必须匹配foobar这个连续的词
foobarRegexp = re.compile(r'foobar')
test1 = "prefixfoobarsuffix"
test2 = "prefixbarfoosuffix"
test3 = "prefixfoo_barsuffix"

print(test1, foobarRegexp.findall(test1))
print(test2, foobarRegexp.findall(test2))
print(test3, foobarRegexp.findall(test3))

# 所以上边的代码只有test1能匹配出结果
```

### 或

```{code-cell} ipython3
# 所有的量词都可以被解释为`或`,比如 *(0次或多次),+(1次或多次),?(0次或1次),(pattern){x,y}(至少x次,最多y次)
# 多个不同的patten中间使用`|`分割,比如 (foo|bar)代表要么匹配foo要么匹配bar
# 字符组,也叫做方括号表达式(bracketed expression),比如[1-9]匹配1~9之间的任意数字,[a-z]匹配a-z之间的任意数字
foobarRegexp = re.compile(r'(foo|bar)')
test1 = "prefixfoosuffix"
test2 = "prefixbarsuffix"
test3 = "prefixfoo_barsuffix"

print(test1,foobarRegexp.findall(test1))
print(test2,foobarRegexp.findall(test2))
print(test3,foobarRegexp.findall(test3))
```

### 非

- 非一般来说有两种方式处理,一种是方括号表达式最前边加一个`^`,比如[^a-z]表示不包含a~z的字符的其他字符
- 另一种是[环视](regexp_lookaround.md),使用反前瞻(?!pattern)和反后顾(?<!pattern)

```{code-cell} ipython3
# 现在以删除所有除去a,img的html标签,并保留所有text内容为例，一步一步的实现我们的需求
test = '''
<div>
    <a href="http://foobar.com">点击跳转</a>
    <img src="http://foo.com/bar.jpg" />
    <p class="border">这是P的内容</p>
</div>
'''
# 我们最终只保留如下内容:
# <a href="http://foobar.com">点击跳转</a>
#     <img src="http://foo.com/bar.jpg" />
#     这是P的内容
```

```{code-cell} ipython3
# html的标签目前看来是以<开头的,第二个字符可以是/用以代表一个闭合标签,中间不包含>并右边以>结尾的，所以可以用 </?[^>]+> 匹配
print("只包含html标签:", re.findall(r'</?[^>]*>', test))
```

```{code-cell} ipython3
# 如果我们的需求是删掉所有html标签,只剩text内容的话，现在只需要用空字符串替换掉这些标签就行
print("删除所有html标签后:", re.sub(r'</?[^>]*>', "", test))
```

```{code-cell} ipython3
# 那现在我们需要保留a和img标签，怎么做呢?首先，如果我们要匹配所有的a和img标签应该这样 </?(a|img)[^>]*>
# 但是由于python的findall的机制问题，所以我们默认用一个非捕获语法(?:pattern)来屏蔽到单独的a和img的输出
print("只包含a和img标签:", re.findall(r'(</?(?:a|img)[^>]*>)', test))
```

```{code-cell} ipython3
# 所以如果要删除a和img标签的话，那直接用空字符串替换掉匹配的标签就行了，但是我们实际上是需要留下这两个标签
# 那么我们就可以使用反前瞻来实现。具体的正则就是先前两个的组合
# 首先我们要匹配出所有非a和img的标签  (?!</?(?:a|img)[^>]*>) 
# 然后再去尝试匹配其他标签  </?[^>]*>
# 所以最终的正则看起来应该是这两者拼起来的 (?!</?(?:a|img)[^>]*>)(</?[^>]*>)
print("只保留a和img以及所有text",re.sub(r'(?!</?(?:a|img)[^>]*>)(</?[^>]*>)',"",test))
```

```{code-cell} ipython3

```
