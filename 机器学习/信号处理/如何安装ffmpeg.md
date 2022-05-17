## Windows安装ffmpeg

### 有anaconda

有conda的话，最简单的方法就是。

```
conda install ffmpeg -c conda-forge
```

注意：上面的安装命令要在对应的虚拟环境下执行。

### 无anaconda

无conda的话，在官网可以找到[ffmpeg](https://ffmpeg.org/)的下载地址，它原本是只有源代码，但是有人把它安装各个平台编译好了，直接下载对应平台的安装包即可。

直接[点此下载windows平台的ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)

若要查看其他版本：[windows builds from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)

下载完成后解压并把软件放到任意路径。

例：

我点击上面的链接后，下载的是这个压缩包

```
ffmpeg-2022-03-07-git-e645a1ddb9-full_build.7z
```

解压后，文件夹名字修改为`ffmpeg`（不然太长了）

然后把文件夹放到D盘的software（放到任意地方都行，此处为举例），这样它的路径就是`D:/software/ffmpeg`

这个文件夹下有

```
|-ffmpeg
  |-bin
    |-ffmpeg.exe
    |-ffplay.exe
    |-ffprobe.exe
  |-doc
  |-presets
  ...
```

主要关注bin文件夹下的`ffmpeg.exe`。

然后[配置环境变量](https://jingyan.baidu.com/article/0eb457e5ddd37e03f1a90596.html)

把目录`D:\Software\ffmpeg\bin`加入环境变量即可。

打开cmd命令行工具，输入：

```
ffmpeg
```

如果能正确执行命令就算安装成功，比如我这里就显示

```
ffmpeg version 2022-03-07-git-e645a1ddb9-full_build-www.gyan.dev Copyright (c) 2000-2022 the FFmpeg developers
...
...
```

