# fingerprint

一个简单的指纹识别小工具

## 指纹识别方式

本着偷懒的原则，直接采用的ast.parse 解析之后通过eval 来进行参数转换，
这样做的好处呢就是每一条指纹规则我只需要if 判断就行。
不需要在考虑里面是否存在and or () 这种多条件判断。

```
"product": "Spring-Boot-Admin",
 "rule": "\"spring boot admin\" in body  and title==\"Spring boot admin\"",
```

就拿这条指纹来说，通过eval执行之后 就会判断，字符串 spring boot admin 是否在我们传入的html里面
和 title等于 Spring boot admin 这个字符串，如果匹配成功 就返回Spring-Boot-Admin

然后又定义了一个flag，如果识别到这个指纹flag就+1，这样常用指纹识别的效率就越来越快，同理不常用的越来越慢。

### 使用方式

python3 cms.py -u https://www.baiud.com

python3 cms.py -f url.txt
