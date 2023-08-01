现在需要配置一个什么数字签名，不然无法进去。

[fuqiuluo/unidbg-fetch-qsign: 获取QQSign通过Unidbg (github.com)](https://github.com/fuqiuluo/unidbg-fetch-qsign)

下载docker后

```
docker run -d --restart=always --name qsign -p 8080:8080 -e ANDROID_ID=c7b3e48afefb70ec xzhouqd/qsign:8.9.63
```

