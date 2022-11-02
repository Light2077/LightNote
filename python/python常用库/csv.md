在python中创建并保存csv文件

```python
import csv

lines = [["lily", 16, "girl"],
         ["alex", 15, "boy"],
         ["jack", 13, "boy"]]

with open("demo.csv", mode='w', encoding='utf8', newline="") as f:
    for line in lines:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(line)
```

文件内容

```
lily,16,girl
alex,15,boy
jack,13,boy

```





同时打开两个文件

```python
with open(filename1, 'rb') as fp1, open(filename2, 'rb') as fp2, open(filename3, 'rb') as fp3:
    for i in fp1:
        j = fp2.readline()
        k = fp3.readline()
        print(i, j, k)
```

