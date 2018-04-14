# Novels-Site
## 用Flask搭建小说网站

## 结构
    server/
    |--app/
        |--api_v1_0/    # api目录，对于REST访问返回数据
            |--users.py
            |--novels.py
        |--main/
            |--__init__.py  #初始化配置
            |--forms.py  #表单
            |--views.py  # 路由文件，SPA里，只需要返回"/"根路由
        |--static/      # js, css
        |--templates/    # SPA里，只需要index.html  
        |--__init__.py  # flask app初始化
        |--models.py    # model数据库定义
    |--config.py  # Flask配置
    |--manage.py  # Flask启动文件，包含命令行