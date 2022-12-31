空值传播运算符

```c#
//c# 5
var handler = Event;
if (handler != null)
{
    handler(source, e);
}

//C# 6
var handler = Event;
handler?.Invoke(source, e);
```

