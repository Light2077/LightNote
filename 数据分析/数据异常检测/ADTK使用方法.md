https://adtk.readthedocs.io/en/stable/notebooks/demo.html#LevelShiftAD

阶梯型误差（阶跃）

```python
from adtk.detector import LevelShiftAD
from adtk.visualization import plot
level_shift_ad = LevelShiftAD(window=120, side='both')
anomalies = level_shift_ad.fit_detect(s)
# 


plot(s, anomaly=anomalies, anomaly_color='red')
```

