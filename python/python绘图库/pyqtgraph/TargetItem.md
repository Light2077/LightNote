TargetItem

在画布上可以拖动的点

```python
targetItem1 = pg.TargetItem()

targetItem2 = pg.TargetItem(
    pos=(30, 5),
    size=20,
    symbol="star",
    pen="#F4511E",
    label="vert={1:0.2f}",
    labelOpts={
        "offset": QtCore.QPoint(15, 15)
    }
)
targetItem2.label().setAngle(45)

targetItem3 = pg.TargetItem(
    pos=(10, 10),
    size=10,
    symbol="x",
        pen="#00ACC1",
)
targetItem3.setLabel(
    "Third Label",
    {
        "anchor": QtCore.QPointF(0.5, 0.5),
        "offset": QtCore.QPointF(30, 0),
        "color": "#558B2F",
        "rotateAxis": (0, 1)
    }
)
q

def callableFunction(x, y):
    return f"Square Values:\n({x**2:.4f}, {y**2:.4f})"

targetItem4 = pg.TargetItem(
    pos=(10, -10),
    label=callableFunction,
	labelOpts={
        'fill': (200,200,200,50)
    }
)

p1.addItem(targetItem1)
p1.addItem(targetItem2)
p1.addItem(targetItem3)
p1.addItem(targetItem4)
```

