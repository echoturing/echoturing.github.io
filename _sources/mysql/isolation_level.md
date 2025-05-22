# MySQL innodb 事务隔离级别以及幻读详解

## MySQL 提供了四种标准的事务隔离级别，每种级别解决了不同的并发问题

### 以下是常规四种隔离级别的介绍(注意: mysql 的 repeated read 是可以部分解决幻读的)

1. READ UNCOMMITTED（读未提交）
    - 最低隔离级别
    - 事务可以读取其他事务未提交的修改（"脏读"）
2. READ COMMITTED（读已提交）
    - 事务只能读取其他事务已提交的修改
    - 解决了脏读问题
3. REPEATABLE READ（可重复读）
    - MySQL 默认隔离级别
    - 确保在同一事务中多次读取相同数据结果一致
    - 解决了脏读和不可重复读问题
4. SERIALIZABLE（串行化）
    - 最高隔离级别
    - 完全串行执行事务
    - 解决了脏读、不可重复读和幻读问题

### 解决的问题

| 隔离级别             | 脏读 | 不可重复读 | 幻读 |
|------------------|:--:|:-----:|:--:|
| READ UNCOMMITTED | ❌  |   ❌   | ❌  |
| READ COMMITTED   | ✅  |   ❌   | ❌  |
| REPEATABLE READ  | ✅  |   ✅   | ❌  |
| SERIALIZABLE     | ✅  |   ✅   | ✅  |

具体问题解释：

1. 脏读（Dirty Read）：一个事务读取了另一个未提交事务修改过的数据
2. 不可重复读（Non-repeatable Read）：同一事务内，多次读取同一数据返回不同结果（因为其他事务修改了数据）
3. 幻读（Phantom Read) ：同一事务内，多次查询返回不同的行集（因为其他事务插入了新数据）

## 为什么说 Mysql 的 REPEATABLE READ 隔离级别可以部分解决幻读问题

先建个表(以下都是在 REPEATABLE READ 隔离级别下的)

```sql
CREATE TABLE user
(
    id   INT PRIMARY KEY,
    name VARCHAR(100)
);
```

### 1. mvcc 的快照读防止幻读

| trasactionA                                                               | trasactionB                                  |
|---------------------------------------------------------------------------|----------------------------------------------|
| begin;                                                                    |                                              |
| select * from user; # 快照读(生成 read view)                                   |                                              |
|                                                                           | begin;                                       |
|                                                                           | insert into user (id,name) values (10,"xx"); |
|                                                                           | commit;                                      |
| select * from user; # 这时候是查不到 id=10 这条记录的,因为 mysql 的 mvcc 且常规 select 是快照读 |                                              |
| commit                                                                    |                                              |

### 2. 但是也有例外

| trasactionA                                                           | trasactionB                                  |
|-----------------------------------------------------------------------|----------------------------------------------|
| begin;                                                                |                                              |
| select * from user; # 快照读(生成 read view)                               |                                              |
|                                                                       | begin;                                       |
|                                                                       | insert into user (id,name) values (10,"xx"); |
|                                                                       | commit;                                      |
| select * from user for update; #for update 是当前读,所以会查出 id=10 的,这时候又幻读了 |                                              |
| commit                                                                |                                              |
