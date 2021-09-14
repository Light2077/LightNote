# shapelets

原论文：https://www.cs.ucr.edu/~eamonn/shaplet.pdf





# shapelets transform

参考论文：

>J. Lines, L. M. Davis, J. Hills and A. Bagnall, “A Shapelet Transform for Time Series Classification”. Data Mining and Knowledge Discovery, 289-297 (2012).



代码参考文档：https://pyts.readthedocs.io/en/stable/generated/pyts.transformation.ShapeletTransform.html

> A shapelet is a time series subsequence that is identified as being representative of class membership.

起初是在决策树中寻找shapelets（原来这篇论文不是第一篇）

提取shapelets的过程与分类算法分割开，提出了**shapelet transformation**

> 就是说，不用分类就来找shaplets

这是一种从数据集一次性提取k个最好的shapelets的方法，然后用这些shapelets转换原始数据，通过计算每个系列到shapelet的距离。

