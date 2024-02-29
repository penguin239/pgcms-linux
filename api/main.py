from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from api import models
from api import config
from api import security

import time
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/api/v1/all_article_list")
async def all_article_func(page: int = 1):
    page_size = 8
    all_article = []

    try:
        models.session.commit()
        all_article_list = models.session.query(models.Article).all()
    except:
        models.session.rollback()
        return -1
    else:
        if not all_article_list:
            # 没有任何文章
            return None

        for article in all_article_list:
            data = {
                'article_id': article.article_id,
                'title': article.title,
                'article_date': article.article_date,
                'details': article.detail
            }
            # all_article.append(data)
            all_article.insert(0, data)

        # 共有多少页
        page_number = int(len(all_article) / (page_size + 1)) + 1

        split_page_list = [all_article[i:i + page_size] for i in range(0, len(all_article), page_size)]

        return {
            'articles': split_page_list[page - 1],
            'all_page_number': page_number
        }
    finally:
        models.session.close()


@app.get('/api/v1/articleDetail')
async def article_detail_func(article_id: int):
    models.session.commit()

    result = models.session.query(models.Article).filter(models.Article.article_id == article_id).first()
    models.session.close()

    return {
        'article_id': result.article_id,
        'title': result.title,
        'details': result.detail,
        'content': result.content,
        'article_date': result.article_date
    }


@app.post('/api/v1/uploadImage')
async def upload_image(image: UploadFile):
    try:
        filename = image.filename
        new_file_name_t = str(int(time.time() * 1000))

        upload_path = config.image_upload_path
        with open(f'{upload_path}{new_file_name_t}.jpg', 'wb') as file:
            file.write(await image.read())
        return {
            'errno': 0,
            'data': {
                # 给前端的路径，前端代码中包含的
                'url': f'{config.front_image_path}{new_file_name_t}.jpg',
                'alt': filename,
            }
        }
    except:
        return {
            'errno': 1,
            'message': 'upload error.'
        }


@app.post('/api/v1/uploadVideo')
async def upload_video(video: UploadFile):
    try:
        filename = video.filename
        new_file_name_t = str(int(time.time() * 1000))

        upload_path = config.video_upload_path

        with open(f'{upload_path}{new_file_name_t}.mp4', 'wb') as file:
            file.write(await video.read())
        return {
            'errno': 0,
            'data': {
                'url': f'{config.front_video_path}{new_file_name_t}.mp4',
                'alt': filename
            }
        }
    except:
        return {
            'errno': 1,
            'message': 'upload error.'
        }


@app.post('/v1/login/checkUser')
async def login_user_check_func(request: dict):
    sign = hashlib.md5((request['username'] + str(request['t']) + request['password']).encode())
    if sign.hexdigest() != request['sign']:
        return HTTPException(status_code=500, detail='invalid sign.')
    # 对比数据库后，返回token
    models.session.commit()

    db_password = models.session.query(models.Admin).filter(models.Admin.username == request['username']).first()
    if (not db_password) or (db_password.password != request['password']):
        return HTTPException(status_code=500, detail='invalid username or password.')
    access_token = security.create_access_token(username=request['username'])

    return {'status_code': 200, 'token': access_token}


@app.get('/v1/login/checkLogin')
async def login_check_func(access_token: str):
    return security.decode_access_token(access_token)


def get_current_date() -> str:
    now = datetime.now()
    formatted_time = now.strftime('%d/%m/%Y')
    return formatted_time


def get_article_id() -> int:
    try:
        models.session.commit()

        last_record = models.session.query(models.Article).order_by(models.Article.id.desc()).first()
        return last_record.article_id
    except:
        models.session.rollback()
        return -1
    finally:
        models.session.close()


@app.post('/api/v1/postArticle')
async def post_article_func(request: dict):
    current_date = get_current_date()
    article_id = get_article_id() + 1

    try:
        models.session.commit()

        article = models.Article(article_id=article_id, title=request['title'], content=request['content'],
                                 article_date=current_date, detail=request['detail'])
        models.session.add(article)
        models.session.commit()
        return 1
    except:
        models.session.rollback()
        return -1
    finally:
        models.session.close()


@app.get('/api/v1/get_all_article')
async def get_all_article_func():
    try:
        models.session.commit()
        all_article = models.session.query(models.Article).all()
    except:
        models.session.rollback()
        return -1
    else:
        if not all_article:
            return None

        return all_article[::-1]


@app.post('/api/v1/updateArticle')
async def update_article_func(request: dict):
    article = (models.session.query(models.Article)
               .filter_by(article_id=request.get('article_id')))
    article.update({
        'title': request.get('new_title'),
        'detail': request.get('new_detail'),
        'content': request.get('new_content')
    })

    try:
        models.session.commit()
        return 1
    except:
        models.session.rollback()
        return -1
    finally:
        models.session.close()


@app.get('/api/v1/deleteArticle')
async def delete_article_func(article_id: int):
    try:
        models.session.query(models.Article).filter_by(article_id=article_id).delete()
        models.session.commit()
        return 1
    except:
        models.session.rollback()
        return -1
    finally:
        models.session.close()


@app.get('/api/v1/getBlogSetting')
async def get_blog_settings_func():
    result = models.session.query(models.Settings).first()

    return {
        'blog_title': result.blog_title,
        'contact_information1': result.contact_information1,
        'contact_information2': result.contact_information2,
        'contact_name1': result.contact_name1,
        'contact_name2': result.contact_name2,
        'blog_icon': result.blog_icon,
        'index_title': result.index_title,
        'contact_link1': result.contact_link1,
        'contact_link2': result.contact_link2
    }


@app.post('/api/v1/setBlogSetting')
async def set_blog_settings_func(request: dict):
    models.session.query(models.Settings).update({
        'blog_title': request.get('set_site_title'),
        'index_title': request.get('set_index_title'),
        'contact_information1': request.get('contact_info1'),
        'contact_information2': request.get('contact_info2'),
        'contact_name1': request.get('contact_name1'),
        'contact_name2': request.get('contact_name2'),
        'contact_link1': request.get('contact_link1'),
        'contact_link2': request.get('contact_link2'),
    })
    try:
        models.session.commit()
        return 1
    except:
        models.session.rollback()
        return -1
    finally:
        models.session.close()


@app.post('/api/v1/setIconSetting')
async def set_icon_settings_func(blog_icon: UploadFile = File(None)):
    # 501: 图片类型不支持, 502: 文件过大(超过1MB)
    img_suffix = ['jpg', 'jpeg', 'png']
    file_object = blog_icon.file
    file_object.seek(0, 2)
    file_size = file_object.tell()
    file_object.seek(0)

    if blog_icon:
        blog_icon_suffix = blog_icon.filename.split('.')[-1]
        if blog_icon_suffix not in img_suffix:
            return HTTPException(status_code=501, detail='invalid file format.')
        if int(file_size / 1024) > 1024:
            return HTTPException(status_code=502, detail='too large file.')
        with open(f'{config.icon_upload_path}{blog_icon.filename}', 'wb') as f:
            f.write(await blog_icon.read())

    models.session.query(models.Settings).update({
        'blog_icon': f'{config.icon_front_path}{blog_icon.filename}',
    })
    try:
        models.session.commit()
        return HTTPException(status_code=200, detail='success.')
    except:
        models.session.rollback()
        return HTTPException(status_code=500, detail='database error.')
    finally:
        models.session.close()
