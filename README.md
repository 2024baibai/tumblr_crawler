# Tumblr解析网站搭建教程
1. 首先安装Python。linux自带了python，windows请自行下载python。推荐Centos7/Python2.7
2. 这时候，pip应该可以用了。如果不行，linux请按下面的命令安装pip：
    `wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py`
3. 安装依赖库：`pip install -r requirement.txt`
4. 创建数据库：`python rebuildDB.py`
5. 运行：`gunicorn -w4 -b 0.0.0.0:5000 run:app`

然后访问 ip:5000 试试
如果不能访问，看看防火墙是否开了5000端口？

------

## 以上都是基本的安装。
### 如果你需要使用MySQL
修改`config.py`：注释第六行 --> 第五行开头#去掉，修改`user`、`passwd`、`database`

### 配置自启动
1. 修改`supervisord.conf`，将`directory`修改为脚本根目录
2. echo "supervisord -c 网站根目录/supervisord.conf" >> /etc/rc.d/rc.local
3. chmod +x /etc/rc.d/rc.local

### 配置nginx
修改nginx配置文件，添加`server`
```
server {
        listen       80;
        server_name t.v4s0.us; #域名
        charset utf-8;

        access_log  /www/wwwlogs/t.v4s0.us.log;

        location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_redirect off;
        proxy_set_header Host $host:80;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        location /(images|javascript|js|css|flash|media|static)/ {
                root /root/tumblr_clawer/app/static; #目录修改好
                expires 1d;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
   }
   
  }
```

### 其他需求请加[qq群](https://jq.qq.com/?_wv=1027&k=5G8OtPx)

------
示例网站：http://t.3kk.me

