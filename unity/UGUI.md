### 新建GUI物体

右键在Hierarchy新建一个UGUI的物体，会自动创建一个Canvas附带你选的物体

<img src="./images/image-20230808225542814.png" alt="image-20230808225542814" style="zoom: 80%;" />

在新项目第一次创建UGUI物体时，会弹出下面的提示框

<img src="./images/image-20230808225048141.png" alt="image-20230808225048141" style="zoom:80%;" />

>This appears to be the first time you access TextMesh Pro, as such we need to add resources to your project that are essential for using TextMesh Pro. These new resources will be placed at the root of your project in the "TextMesh Pro" folder.
>
>这似乎是您首次使用TextMesh Pro，因此我们需要向您的项目添加一些使用TextMesh Pro所必需的资源。这些新资源将被放置在项目的根目录下的"TextMesh Pro"文件夹中。

点击 **Import TMP Essentials** 即可

导入后，可以选择是否导入示例

> The Examples & Extras package contains addition resources and examples that will make discovering and learning about TextMesh Pro's powerful features easier. These additional resources will be placed in the same folder as the TMP essential resources.
>
> 除了基本的TextMesh Pro资源外，Unity还提供了一个额外的资源和示例包。这个包含了一些展示TextMesh Pro功能的示例场景、项目或其他资源。通过这些示例，您可以更快速地了解和掌握TMP的各种特性和用法。

为了学习，可以导入。

### 设置字体

这里选择[得意黑 Smiley Sans](https://atelier-anchor.com/typefaces/smiley-sans)

下载下来是一个压缩包 `smiley-sans-v1.1.1.zip`

解压后

```
|- smiley-sans-v1.1.1/
  |- SmileySans-Oblique.otf
  |- SmileySans-Oblique.otf.woff2
  |- SmileySans-Oblique.ttf
  |- SmileySans-Oblique.ttf.woff2
```

> 💡提示
>
> 下载的字体文件中包含了几种不同的文件格式，每种格式都有其特定的用途和特点：
>
> 1. **.otf (OpenType Font)**
>    - **用途**：OpenType 是一种开放的字体格式，支持很多先进的排版功能，如连字、替代字符等。
>    - **特点**：它基于 PostScript 的字符描述，常用于专业的图形设计和排版工作。
>
> 2. **.ttf (TrueType Font)**
>    - **用途**：TrueType 是另一种常见的字体格式。
>    - **特点**：它基于曲线技术来描述字符形状，且兼容性很好，是Windows和Mac操作系统中常见的字体格式。
>
> 3. **.woff2 (Web Open Font Format 2)**
>    - **用途**：WOFF2 是一种专为网页设计的字体格式。它是 WOFF 的继任者，用于在网页上嵌入字体。
>    - **特点**：WOFF2 提供了更高的压缩效率，从而更快地加载页面。
>
> 您下载的目录中包含了两种基本的字体格式（OTF和TTF）以及它们对应的Web字体格式（WOFF2）。如果您要在桌面应用程序或图形设计软件中使用此字体，那么您可能需要使用 `.otf` 或 `.ttf` 文件。如果您计划在网页中使用此字体，则可能需要使用 `.woff2` 文件。

可以在项目目录创建一个 `Asset/Fonts`文件夹，专门用于存放字体文件。

将**后缀为 ttf 的文件**放到该文件夹下。

右键该文件，create → TextMeshPro → FontAsset