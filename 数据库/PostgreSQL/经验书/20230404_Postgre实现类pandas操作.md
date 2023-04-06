```postgresql
WITH diff_table AS (
    SELECT
        id,
        value,
        value - LAG(value) OVER (ORDER BY id) AS diff
    FROM
        my_table
),
cumsum_table AS (
    SELECT
        id,
        value,
        diff,
        SUM(CASE WHEN diff < 0 THEN 1 ELSE 0 END) OVER (ORDER BY id) AS cumsum
    FROM
        diff_table
)
SELECT
    id,
    value,
    diff,
    cumsum
FROM
    cumsum_table;
```

