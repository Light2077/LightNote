行锁定

```python
user = (
    await cls.query.where(
        (cls.user_qq == user_qq) & (cls.group_id == group_id)
    )
    .with_for_update()
    .gino.first()
)
```

