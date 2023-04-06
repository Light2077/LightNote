```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# generate random data
np.random.seed(0)
n = 1000
# y_true = np.random.randint(0, 2, n)
# 调这个
y_true = np.concatenate([np.ones(480), np.zeros(500), np.ones(20)])

# generate scores with normal distribution
positive_scores = np.random.normal(loc=2, scale=1, size=int(n/2))
negative_scores = np.random.normal(loc=0.2, scale=1, size=int(n/2))
y_score = np.concatenate([positive_scores, negative_scores])

# calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_true, y_score)
roc_auc = auc(fpr, tpr)

# plot the ROC curve
plt.figure(figsize=(4, 3), dpi=100)
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (ROC) curve')
plt.legend(loc="lower right")
plt.show()

```

多条ROC曲线绘制在一起

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# generate random data
np.random.seed(0)
n = 1000
# y_true = np.random.randint(0, 2, n)
y_true1 = np.concatenate([np.ones(500), np.zeros(500), np.ones(0)])
y_true2 = np.concatenate([np.ones(480), np.zeros(500), np.ones(20)])
y_true3 = np.concatenate([np.ones(460), np.zeros(500), np.ones(40)])
y_true4 = np.concatenate([np.ones(440), np.zeros(500), np.ones(60)])
def get_roc(y_true):
# 调这个

    # generate scores with normal distribution
    positive_scores = np.random.normal(loc=2, scale=1, size=int(n/2))
    negative_scores = np.random.normal(loc=0.2, scale=1, size=int(n/2))
    y_score = np.concatenate([positive_scores, negative_scores])

    # calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    return fpr, tpr, roc_auc


# plot the ROC curve
plt.figure(figsize=(5, 4), dpi=100)
colors = ["r", "g", "b", "purple"]
labels = ['多源信息融合模型', '混合推荐算法', '关联规则算法', '协同过滤推荐']
markers = ['o', 's', '^', '*']
for y_true, color, label, m in zip([y_true1, y_true2, y_true3, y_true4], colors, labels, markers):
    fpr, tpr, roc_auc = get_roc(y_true)
    plt.plot(fpr, tpr, color=color, lw=2, label=f'{label} ({roc_auc:.2f})', alpha=.5, marker=m, markevery=15)

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('假阳率（误报率=FP/(FP+TN)）')
plt.ylabel('真阳率（TP/(TP+FN)）')
plt.title('不同算法实验结果对比')
plt.legend(loc="lower right")
plt.show()

```

