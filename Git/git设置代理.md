```
git config --global http.proxy http://127.0.0.1:4780
git config --global https.proxy https://127.0.0.1:4780
```

取消代理

```
git config --global --unset http.proxy
git config --global --unset https.proxy
```

socks5代理

```
git config --global http.proxy 'socks5://127.0.0.1:4781'
git config --global https.proxy 'socks5://127.0.0.1:4781'
```

