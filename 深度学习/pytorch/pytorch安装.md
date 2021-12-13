创建环境

```
conda create --name pytorch python==3.7
```

激活环境

```
conda activate pytorch
```

安装pytorch

```
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

检查pytorch是否安装成功

```python
import torch

print(torch.__version__)
print('gpu:', torch.cuda.is_available())
```

