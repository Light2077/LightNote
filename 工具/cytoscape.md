安装指南：https://zhuanlan.zhihu.com/p/408302114

Cytoscape教程：https://blog.csdn.net/weixin_42191440/article/details/112926258

https://cloud.tencent.com/developer/inventory/9725



目标

- 结点用特定的图片表示
- 边带箭头，且可以显示标签 √
- 边和结点基于权重调整大小和透明度 √

### 导入数据

创建一个csv文件`mydata.csv`

```csv
source,target,value
a,b,5
a,c,7
b,d,4
c,e,4
b,e,8
d,f,3
e,f,9
```

导入数据File>Import>Network From File...

### 布局调整

在上方的Layout菜单可以调整布局

可以使用自动布局功能，Apply Preferred Layout，快捷键F5

## 边的格式

| 名称                          | 说明                                     |
| ----------------------------- | ---------------------------------------- |
| Label                         | 边的标签，标注在边上                     |
| Label Color                   | 边标签的颜色                             |
| Label Font Size               | 边标签的字体大小                         |
| Line Type                     | 边的类型，可以选择实线、虚线、双线等类型 |
| Source Arrow Shape            | 起始箭头类型                             |
| Source Arrow Unselected Paint | 边未选中时起始箭头的颜色                 |
| Stroke Color(Unselected)      | 边未选中时边的颜色                       |
| Target Arrow Shape            | 末端箭头类型                             |
| Target Arrow Unselected Paint | 边未选中时末端箭头的颜色                 |
| Transparency                  | 透明度                                   |
| Width                         | 边的粗细                                 |

下面举两个例子

### 边的标签

在右侧的Style选项卡，一开始默认是结点Node的格式，可以在选项框下方切换到边Edge的格式

找到Label这一行，点击右侧的小箭头“`<`”展开。

column选择value

### 边的粗细

边的粗细可以通过width来修改

Column选择边的值，然后Mapping Type选择Continuous Mapping

> Mapping Type 是什么？
>
> Mapping Type表示如何映射将所选列的值
>
> 比如某一列表示两人同行的次数，次数范围是2~10次。
>
> 就可以通过Continuous Mapping（连续值映射），将2-10映射为线条的宽度，比如5-20。

其余设置类似边的粗细。

## 节点的格式

### 结点用自定义图片

首先在View>Open Image Editor 可以打开图片管理器，在这里上传自定义的图片。

然后打开style选项卡，Node页面，展开Image/Chart 1。

可以选择一列，列的内容填图片的名称。

