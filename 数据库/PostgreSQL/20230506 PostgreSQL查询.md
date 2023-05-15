假设我们有一个电商网站，现在我们需要分析每个产品在不同阶段（例如：发货、送货、退货）的最新状态。我们可以创建一个名为 `order_status` 的表来存储这些数据。表的列为：`order_id`，`product_id`，`status`，`status_sequence` 和 `status_timestamp`。`status_sequence` 是一个整数，表示当前状态在订单处理过程中的顺序。

建表语句：

```sql
CREATE TABLE order_status (
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    status_sequence INT NOT NULL,
    status_timestamp TIMESTAMP NOT NULL
);

```

插入虚拟数据

```sql
INSERT INTO order_status (order_id, product_id, status, status_sequence, status_timestamp) VALUES
    ('O1', 'P1', 'Shipped', 1, '2023-05-01 10:00:00'),
    ('O1', 'P1', 'Delivered', 2, '2023-05-03 14:30:00'),
    ('O1', 'P1', 'Returned', 3, '2023-05-05 17:45:00'),

    ('O2', 'P2', 'Shipped', 1, '2023-05-02 09:00:00'),
    ('O2', 'P2', 'Delivered', 2, '2023-05-04 15:00:00'),

    ('O3', 'P3', 'Shipped', 1, '2023-05-01 11:00:00'),
    ('O3', 'P3', 'Delivered', 2, '2023-05-03 13:30:00'),
    ('O3', 'P3', 'Returned', 3, '2023-05-04 16:00:00'),

    ('O4', 'P1', 'Shipped', 1, '2023-05-01 14:00:00'),
    ('O4', 'P1', 'Delivered', 2, '2023-05-03 10:30:00');

```

构建 SQL 以查找特定产品在特定状态下的最新记录

```sql
SELECT
    order_id, product_id, status, status_sequence, status_timestamp
FROM
    (
        SELECT
            order_id, product_id, status, status_sequence, status_timestamp,
            ROW_NUMBER() OVER (PARTITION BY product_id, status ORDER BY status_sequence DESC, status_timestamp DESC) AS rn
        FROM
            order_status
        WHERE
            product_id = 'your_desired_product_id'
            AND status = 'your_desired_status'
    ) subquery
WHERE
    rn = 1;

```

将 `your_desired_product_id` 和 `your_desired_status` 替换为想要查询的实际产品 ID 和状态。

此查询使用了窗口函数 `ROW_NUMBER()`，将 `order_status` 表中的记录按照 `product_id` 和 `status` 分组，并为每个组内的行分配一个唯一序号，根据 `status_sequence` 降序排列。外层查询中，我们仅选择序号为 1的行，即具有最大 `status_sequence`（最新状态顺序）值的行。在存在多个具有相同最大 `status_sequence` 的行的情况下，我们还按照 `status_timestamp` 降序排列，以确保选择最新的记录。

假设我们要查询产品 'P1' 在 'Delivered' 状态下的最新记录，可以使用以下查询：

```sql
SELECT
    order_id, product_id, status, status_sequence, status_timestamp
FROM
    (
        SELECT
            order_id, product_id, status, status_sequence, status_timestamp,
            ROW_NUMBER() OVER (PARTITION BY product_id, status ORDER BY status_sequence DESC, status_timestamp DESC) AS rn
        FROM
            order_status
        WHERE
            product_id = 'P1'
            AND status = 'Delivered'
    ) subquery
WHERE
    rn = 1;

```

