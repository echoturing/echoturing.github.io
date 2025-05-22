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

MySQL Redo Log , Undo Log 以及 Binlog 的区别
=========================

MySQL 中的 redo log、undo log 和 binlog（binary log）是三种不同用途的日志机制，它们在保证数据库的事务性、持久性、可恢复性以及复制功能方面发挥着重要作用。以下是它们的详细对比：


## Redo Log（重做日志）

目的：保证事务的 持久性（Durability），实现 崩溃恢复（Crash Recovery）。

- 记录内容：物理修改后的 页的数据（Page changes），如对表中某行数据的插入、更新、删除所导致的页变更。
- 工作机制：先写 redo log，再写内存页，最后异步刷新到磁盘（WAL：Write-Ahead Logging）。
- 作用时机：数据库崩溃后，用于 重做已提交事务 的修改。
- 所属模块：InnoDB 存储引擎专属。

## Undo Log（回滚日志）

目的：用于事务的 原子性（Atomicity） 和支持 MVCC（多版本并发控制）。

- 记录内容：事务对数据的 原始值（旧值）。
- 工作机制：在修改数据前先写入 undo log，若事务失败或被回滚，就用该日志恢复到原始状态。
- 作用时机：
- 回滚时：撤销尚未提交事务的操作。
- 查询时：用于 MVCC 提供一致性读（如快照读）。
- 所属模块：InnoDB 存储引擎专属。

## Binlog（归档日志 / 二进制日志）

目的：

- 用于 主从复制（Replication）
- Point-in-time Recovery（基于时间点的恢复）
- 提供 审计 和 数据同步 功能
- 记录内容：逻辑上的 SQL 语句或行级变更（依据格式）。
- 工作机制：在事务提交时记录整个事务的修改操作。
- 作用时机：用于恢复、主从同步、数据审计。
- 所属模块：Server 层，所有存储引擎都能使用。

## 场景示例

我们有一个用户表：

```sql
CREATE TABLE users
(
    id   INT PRIMARY KEY,
    name VARCHAR(100)
);
```

执行一个事务：

```sql
BEGIN;
UPDATE users
SET name = 'Alice' WHERE id = 1;
COMMIT;
```

这条语句修改了 id=1 的用户的名字为 'Alice'。

## 三种日志的记录过程

以下是各个日志的记录过程，我们用流程图解展示：

- Redo Log：写入物理页变更（保障持久性）

- Undo Log：写入旧值（支持回滚与一致性读）

- Binlog：写入逻辑 SQL（用于复制与恢复）

```text
  +-------------------------------------------+
  |           SQL 执行 (更新 id=1)           |
  +-------------------------------------------+
                      |
                      v
            +----------------------+
            |   写入 Undo Log      |  <- 记录旧值 name = "Bob"
            +----------------------+
                      |
                      v
            +----------------------+
            |   修改 Buffer Pool   |  <- 内存中修改数据页
            +----------------------+
                      |
                      v
            +----------------------+
            | 写入 Redo Log (Prepare) |  <- 记录物理修改
            +----------------------+
                      |
                      v
            +----------------------+
            |     写入 Binlog     |  <- 记录 UPDATE SQL
            +----------------------+
                      |
                      v
            +----------------------+
            |  Redo Log Commit 标记 |  <- 两阶段提交完成
            +----------------------+
                      |
                      v
           +------------------------------+
           | 最终刷盘 (数据页 & redo log) |
           +------------------------------+
```