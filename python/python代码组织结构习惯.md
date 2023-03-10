写代码有一段时间了，逐步感受到规范的重要性，先初步制定一套我个人的代码组织结构，如果以后觉得不好用，或者有更好的方案再改。（2023.03.03）

```
|=project_name
  |=src  # 代码文件夹
    |-__init__.py
    |-main.py
  |=pkgs  # 环境依赖包
    |=windows  # 不同环境应该区分开
    |=linux
  |=data  # 分析中用到的数据
  |=docs  # 说明文档，分析报告等
  |=output  # 程序输出的文件
  |=.venv  # 虚拟环境目录
  |=.config  # 配置文件夹
    |-config.json  # 配置文件
  |-README.md
  |-.gitignore
  |-.env  # 环境变量
```

