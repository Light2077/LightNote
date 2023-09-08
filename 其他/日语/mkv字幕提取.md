## 动漫资源下载

诸神字幕组：https://subs.kamigami.org/

字幕库：https://zimuku.org/

字幕搜索网：https://subhd.tv/

微博搜索：甜饼字幕组



下载地址：https://www.fosshub.com/MKVToolNix.html

官网：https://mkvtoolnix.download/downloads.html

文档

```
mkvextract <source-filename> <mode1> [选项] <extraction-spec1> [<mode2> [选项]
<extraction-spec2>…]

 模式:
tracks [选项] [TID1:输出1 [TID2:输出2...]]
tags [选项] 输出.xml
attachments [选项] [AID1:输出1 [AID2:输出2...]]
chapters [选项] 输出.xml
cuesheet [选项] 输出.cue
timestamps_v2 [TID1:输出1 [TID2:输出2...]]
cues [选项] [TID1:输出1 [TID2:输出2...]]

 其他选项:
mkvextract <-h|--help|-V|--version>
第一个参数必须为输入文件名。其他参数可切换到特定的提取模式，更改当前活动模式
的选项，或指定将哪些内容提取到哪些文件中。对 mkvextract 的同一次调用可以使用多
种模式，这样可以只读取一遍就提取多种内容。大部分选项只能在特定模式下使用，只
有少数选项可在所有模式下使用。

 全局选项:
  -f, --parse-fully           解析整个文件，而不是仅依照索引。
  -v, --verbose               启用更详细的输出消息。
  -q, --quiet                 禁止输出状态消息。
  --ui-language <code>        强制使用 'code' 语言的翻译。
  --command-line-charset <charset>
                              命令行字符的字符集
  --output-charset <cset>     用指定的字符集输出消息
  -r, --redirect-output <file>
                              将所有消息重定向至此文件。
  --flush-on-close            关闭以写入模式打开的文件时，强制将所有已缓存的
                              数据写入到存储设备。
  --abort-on-warnings         出现警告时即中止程序。
  @option-file.json           从指定的 json 文件中读取其他命令行选项（参见帮助
                              文档）。
  -h, --help                  显示本帮助。
  -V, --version               显示版本信息。

 轨道提取:
第一种模式用于将指定轨道提取到外部文件。
  -c charset                  将文本字幕转换为指定字符集 (默认: UTF-8)。
  --cuesheet                  同时尝试提取此轨道的章节信息和标签为 cue 表单。
  --blockadd level            仅保留不高于此层级的附加区块 (默认: 保留所有层级)
  --raw                       将数据提取为原始文件。
  --fullraw                   将数据提取为原始文件，并以 CodecPrivate 编码格式
                              私有数据作为文件头。
  TID:out                     将 ID 为 TID 的轨道写入到文件 'out'。

 示例:
mkvextract "一部影片.mkv" tracks 2:音频.ogg -c ISO8859-1 3:字幕.srt

 标签提取:
第二种模式用于提取标签，并将其转换为 XML，写入到输出文件中。

 示例:
mkvextract "一部影片.mkv" tags 影片标签.xml

 附件提取:
第三种模式用于从输入文件中提取附件。
  AID:outname                 将 ID 为 'AID' 的附件写入到 'outname'。

 示例:
mkvextract "一部影片.mkv" attachments 4:封面.jpg

 章节提取:
第四种模式用于提取章节，并将其转换为 XML，写入到输出文件中。
  -s, --simple                以 OGM tools 所用的简易格式导出章节信息 (内容类似
                              CHAPTER01=... CHAPTER01NAME=...)。
  --simple-language language  使用指定语言的章节名称，而非发现的第一个章节名
                              称。

 示例:
mkvextract "一部影片.mkv" chapters 影片章节.xml

 cue 表单提取:
第五种模式尝试提取章节信息和标签，并将其输出为 cue 表单。这是使用 mkvmerge 的“
--chapters”选项搭配 cue 表单的逆操作。

 示例:
mkvextract "音频文件.mka" cuesheet 音频文件.cue

 时间戳提取:
第六种模式用于查找指定轨道所有区块的时间戳，并将其输出为时间戳 v2 文件。

 示例:
mkvextract "一部影片.mkv" timestamps_v2 1:时间戳_轨道1.txt

 cue 提取:
该模式用于将某些轨道的索引信息抽取到外部文本文件中。

 示例:
mkvextract "一部影片.mkv" cues 0:cues_轨道0.txt

 同时提取多个项目:
对 mkvextract 的同一次调用可以使用多种模式，这样可以只读取一遍就提取多种内容。

 示例:
mkvextract "一部影片.mkv" tracks 0:视频.h264 1:音频.aac timestamps_v2 0:时间
戳.视频.txt chapters 章节.xml tags 标签.xml
```







```
mkvextract "D:\\download\\BaiduNetdiskDownload\\之\\之.第一季.01.中日双语.BluRay.1080P.甜饼字幕组.mp4" tracks 3:"D:\\download\\BaiduNetdiskDownload\\之\\tmp2.ass"
```



python

https://blog.csdn.net/weixin_43667077/article/details/119353223

```python

import os


# 设置
video_dir = '.\Modern.Family'  # 请替换为你的视频文件目录
track_id = 2  # 请替换为你的 track_id, 默认: 视频=0, 音频=1, 文本(字幕)=2.


# 收集所有 mkv 视频文件路径
src_video_paths = []
for root, dirs, files in os.walk(video_dir):
    for file in files:
        if file.endswith('mkv'):
            src_video_paths.append(os.path.join(root, file))

# 通过 mkvextract 提取 srt 格式字幕
for src_video_path in src_video_paths:
    dst_srt_path = src_video_path.replace('.mkv', '.srt')
    os.system('mkvextract {} tracks {}:{}\n'.format(src_video_path, track_id, dst_srt_path))

```

