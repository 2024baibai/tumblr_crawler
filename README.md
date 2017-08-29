# Tumblr解析网站搭建教程
1. 首先安装Python。linux自带了python，windows请自行下载python。推荐Centos7/Python2.7
2. 这时候，pip应该可以用了。如果不行，linux请按下面的命令安装pip：
    `wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py`
3. 安装依赖库：`pip install -r requirememt.txt`
4. 创建数据库：`python rebuildDB.py`
5. 运行：`python run.py runserver`

------

## 以上都是基本的安装。
### 如果你需要使用MySQL
修改`config.py`：注释第六行 --> 第五行开头#去掉，修改`user`、`passwd`、'database'

### 其他需求请加[qq群](https://jq.qq.com/?_wv=1027&k=5G8OtPx)

------
示例网站：http://t.v4s0.us

