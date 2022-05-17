https://zhuanlan.zhihu.com/p/351634228

```python
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt

# sampling frequency
fs = 100
# 窗函数
window = 'hann'
# frame长度
n = 256

# 构建signal
# 前一段频率为2，后一段频率为10
signal = np.cos(2*np.pi*200*np.arange(10000)/10000)
signal = np.append(signal, np.cos(2*np.pi*1000*np.arange(10000)/10000))

# STFT
f, t, Z = stft(singal, fs=fs, window=window, nperseg=n)
# 求幅值
Z = np.abs(Z)
# 如下图所示
plt.pcolormesh(t, f, Z, vmin = 0, vmax = Z.mean()*10)
```



## librosa

```python
librosa.stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, pad_mode='reflect')
```



```python
S = np.abs(librosa.stft(y))
S_left = librosa.stft(y, center=False)
```



```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

img = librosa.display.specshow(
    librosa.amplitude_to_db(S, ref=np.max), 
    y_axis='log', 
    x_axis='time', 
    ax=ax
)

ax.set_title('Power spectrogram')

fig.colorbar(img, ax=ax, format="%+2.0f dB")
```

### matplotlib

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 3))
Pxx, freqs, bins, im = ax.specgram(y, Fs = sr, scale_by_freq = True, sides = 'default')
```

