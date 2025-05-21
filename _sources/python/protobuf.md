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

protobuf生成的文件IDE不能自动补全
=========================

# 前言

我们使用python的protobuf的时候,经常发现问题，就是生成的pb2 python的属性不能被ide识别从而自动补全，这样其实很容易造成typo. 但是毕竟python不是亲儿子,所以目前官方也没有想要优化这个体验的想法。那怎么办呢？目前开源社区还有两款能解决这个问题的package

## [1.betterproto](https://pypi.org/project/betterproto/)

betterproto是使用python的[dataclass](dataclass.md)生成的可读性良好的新的python文件，相当于是把protobuf给重新实现了一把。

## [2.mypy-protobuf](https://github.com/dropbox/mypy-protobuf)

mypy-protobuf则是使用mypy的stub方式[(pep-0561)](https://www.python.org/dev/peps/pep-0561/) 。这种方式不改变官方protoc生成的代码，只是额外生成一个*.pyi的stub描述文件而已。

