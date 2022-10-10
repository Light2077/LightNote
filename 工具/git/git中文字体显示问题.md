git 乱码解决方案参考文章：

https://www.jianshu.com/p/10213b5ab890

1.配置git-bash

  打开git-bash，右击窗口进入options，分别将text选项的Locale改为zh-CN，character-set改为UTF-8

2.解决git中文字体不转义问题

```
git config --global core.quotepath false
```



