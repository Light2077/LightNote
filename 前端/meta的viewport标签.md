关于下面这行代码的具体含义可以参考

https://www.runoob.com/w3cnote/viewport-deep-understanding.html

```html
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
```



viewport就是设备的屏幕上能用来显示网页的区域。

有时候viewport比网页大，有时候比网页小。比网页小的时候就需要滑动滚动条去查看网页。

`<meta name="viewport">`标签的目的是对viewport进行控制。

比如，不希望viewport比网页窄，因为viewport比网页窄的话就得左右拖动页面了，也就是不希望出现横向滚动条。

meta viewport 标签首先是由苹果公司在其safari浏览器中引入的，目的就是解决移动设备的viewport问题。

在苹果的规范中，meta viewport 有6个属性（content内的内容）

| 属性          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| width         | 设置***layout viewport*** 的宽度，为一个正整数，或字符串`"width-device"` |
| initial-scale | 设置页面的初始缩放值，为一个数字，可以带小数                 |
| minimum-scale | 允许用户的最小缩放值，为一个数字，可以带小数                 |
| maximum-scale | 允许用户的最大缩放值，为一个数字，可以带小数                 |
| height        | 设置***layout viewport*** 的高度，这个属性对我们并不重要，很少使用 |
| user-scalable | 是否允许用户进行缩放，值为"no"或"yes", no 代表不允许，yes代表允许 |

