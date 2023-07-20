# vuepress

[yarn和npm的区别](https://www.jianshu.com/p/254794d5e741)

```
---
lang: zh-CN
title: 页面的标题
description: 页面的描述
---
```


使用vuepress 搭建博客

https://www.cnblogs.com/softidea/p/10084946.html



按照官方文档配置环境就能初步搭建一个本地的服务

https://v2.vuepress.vuejs.org/zh/guide/getting-started.html

node.js 相当于javascript版本的后端语言

npm —— JavaScript的包管理工具

yarn 暂时没用到

## 配置

需要创建如下项目结构

```
├─ docs
│  ├─ .vuepress
│  │  └─ config.js
│  └─ README.md
├─ .gitignore
└─ package.json
```

然后在config.js里配置你的页面



## 页面

每个markdown文件在vuepress中都是一个单独的页面

### 跳转设置

当前文件目录

```
└─ docs
   └─ zh
      ├─ guide
      │  ├─ getting-started.md
      │  ├─ markdown.md    # <- 我们在这里
      │  └─ README.md
      ├─ reference
      │  └─ config.md
      └─ README.md
```

```
<!-- 相对路径 -->
[首页](../README.md)  
[配置参考](../reference/config.md)  
[快速上手](./getting-started.md)  
<!-- 绝对路径 -->
[指南](/zh/guide/README.md)  
[配置参考 > markdown.links](/zh/reference/config.md#links)  
<!-- URL -->
[GitHub](https://github.com) 
```

## 导航栏与侧边栏

[navbar](https://v2.vuepress.vuejs.org/zh/reference/default-theme/config.html#navbar)

[sidebar](https://v2.vuepress.vuejs.org/zh/reference/default-theme/config.html#sidebar)

配置错误的话显示会异常

必须要手动配置sidebar，才会显示文件夹下的所有文件。

```js
module.exports = {
  lang: 'zh-CN',
  title: '你好， VuePress ！',
  description: '这是我的第一个 VuePress 站点',

  themeConfig: {
    logo: 'https://vuejs.org/images/logo.png',
    sidebarDepth: 3,
    navbar: [
      { 
        text: 'Home', 
        link: '/'
      },
      {
        text: 'apple',
        link: '/apple/'
      },
      // {
      //   text: 'banana',
      //   link: '/banana/'
      // },
      {
        text: 'group',
        children: ['/group/foo.md', '/group/bar.md']
      },
    ],
    sidebar: {
      '/apple/': [
        'README.md',
        '1',
        '2'
      ]
    }
  },
}
```

## 图片居中

> 很简单的一个问题我折腾了好久，主要是不熟悉css。
>
> 搜索思路：
>
> - 在vuepress官网搜文档，无果。
> - 百度谷歌搜 vuepress 图片居中 无果。但是大概知道了可以通过style文件修改样式
> - 但是我没死心，又在vuepress文档里找了半天，发现可以修改styles文件，但是我把这个文件后缀命名成了`index.styl`这是旧版的后缀
> - 经过多次尝试，发现问题，终于修改成功了。

创建一个 `.vuepress/styles/index.scss	`文件

在里边填入

```css
img {
  display: block;
  margin: auto;
}
```

参考：https://v2.vuepress.vuejs.org/zh/reference/default-theme/styles.html#style-%E6%96%87%E4%BB%B6

https://www.runoob.com/css/css-align.html
