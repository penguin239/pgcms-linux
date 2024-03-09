<h1 align="center">PGCMS v0.1</h1>


<p align="center">
<img src="http://42.193.96.127/static/images/default_avatar.png" width="100"><br>
<b><i>一款简洁，实用，基于 fastapi 的博客框架</i></b><br>
<b>🌐 <a href="http://www.flypenguin.cn/">www.flypenguin.cn</a></b>
</p>

---

![GitHub License](https://img.shields.io/github/license/penguin239/pgcms-linux)
![Python Version](https://img.shields.io/badge/Python-3.8-green.svg)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.109.1-green.svg)
![PGCMS Version](https://img.shields.io/badge/PGCMS-v0.1-green.svg)

## 简介

PGCMS 是一款简洁而实用的博客框架，基于 FastAPI 构建。它提供了一套简单而灵活的工具，使您能够快速搭建和部署个人博客网站。

## 特点

- **简洁易用**：PGCMS 提供了直观且易于理解的界面，使用户可以轻松管理博客内容。
- **基于 FastAPI**：利用 FastAPI 框架，PGCMS 实现了高性能和低延迟的服务端渲染，为用户提供出色的访问体验。
- **支持 Markdown**：用户可以使用 Markdown 格式撰写文章，轻松创建富有表现力的内容。
- **集成富文本编辑器**：PGCMS 内部集成了wangEditor，省去用户繁琐的配置过程。

## 快速开始

需要环境：```MySql```, ```Python3```
> PGCMS 压缩包中携带了Nginx，请自行编译使用。

### 下载程序

在release中下载压缩包后，使用此命令解压到相应目录

```bash
tar -zxvf pgcms-linux-v0.1.tar.gz -C /export/server
```

这里我解压到了 ```/export/server```目录，切换到此目录进行下一步。

### 创建虚拟环境（可选）

1. 使用此命令创建虚拟环境```python -m venv venv```，我创建的虚拟环境目录为```venv```。
2. 激活虚拟环境，使用```. venv/bin/activate```即可激活虚拟环境。

### 安装需求

> 使用虚拟环境的同学别忘记激活虚拟环境

#### 更新pip

使用此命令来更新pip，保证我们安装的软件包都处于最新版本。

```bash
python -m pip install --upgrade pip
```

#### 安装需求库

首先切换到刚才解压的```pgcms-linux-v0.1```目录下，执行此命令。

```bash
pip install -r requirements.txt
```

#### 数据库配置

进入您的mysql命令行，新建```blog```数据库。

```sql
CREATE
DATABASE blog
```

选中```blog```数据库并执行导入```blog.sql```文件。

```sql
USE blog

source /export/server/pgcms-linux-v0.1/blog.sql
```

这里换成您自己的路径。

#### 启动程序配置

进入```pgcms-linux-v0.1/api```目录，找到```config.py```文件。\
其中的数据库配置，根据您自己填写。\
图片/视频上传地址根据您Nginx的网站安装目录填写即可。

#### 启动

1. 启动Nginx\
   进入您的Nginx安装目录的```sbin```目录下输入```nginx```即可启动。\
   这里列出几条常用的Nginx命令

```
nginx 启动nginx
nginx -s stop 停止nginx
nginx -s reload 重启nginx
nginx -c nginx.conf 从 nginx.conf 配置文件启动
nginx -s reload -c nginx.conf 从 nginx.conf 配置文件重启
```

2. 启动PGCMS程序\
   进入您的PGCMS目录，输入如下命令即可启动

```bash
python startup.py
```

> 使用虚拟环境的同学别忘记激活虚拟环境

出现下列提示即为启动成功：

```
INFO:     Uvicorn running on http://host:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [5764] using StatReload
INFO:     Started server process [12072]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

3. 访问站点\
   输入```http://yourHost/``` 即可访问您的站点。\
   管理员地址在```http://yourHost/admin``` \
   登录您的管理员账户即可对站点进行管理。

## 示例站点

🌐 [www.flypenguin.cn](http://www.flypenguin.cn/)

## 贡献

如果您发现了任何问题或者有改进建议，请在 GitHub 上提出 issue 或者提交 pull request。

## 问题

如果您在使用过程中发现了任何问题，或者看过教程后仍然不理解，可以添加作者联系方式：\
QQ：309318068

## 许可证

PGCMS 使用 [MIT 许可证](https://github.com/penguin239/pgcms-linux/blob/main/LICENSE)。


<p align="center">
<i>© penguin 2024</i><br>
<img src="http://42.193.96.127/static/images/github.png"><br>
</p>
