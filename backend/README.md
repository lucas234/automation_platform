
#### 开发环境的设置
在项目目录下使用virtulenv:
`virtualenv --no-site-packages venv`,将会自动创建venv目录，
参数`--no-site-packages`强制不将已经安装到Python系统内的任何第三方包复制过来，使得新的venv完全纯净。

然后安装依赖包 `pip install -r requirements.txt`

最有运行 `python app.py`



SQLAlchemy indicates the source of an Engine as a URI combined with optional keyword arguments to specify options for the Engine. The form of the URI is:

dialect+driver://username:password@host:port/database
Many of the parts in the string are optional. If no driver is specified the default one is selected (make sure to not include the + in that case).

Postgres:

postgresql://scott:tiger@localhost/mydatabase
MySQL:

mysql://scott:tiger@localhost/mydatabase
Oracle:

oracle://scott:tiger@127.0.0.1:1521/sidname
SQLite (note that platform path conventions apply):

#Unix/Mac (note the four leading slashes)
sqlite:////absolute/path/to/foo.db
#Windows (note 3 leading forward slashes and backslash escapes)
sqlite:///C:\\absolute\\path\\to\\foo.db
#Windows (alternative using raw string)
r'sqlite:///C:\absolute\path\to\foo.db'
#### 参考
- https://www.scienjus.com/my-restful-api-best-practices/


这篇文章会介绍Python的四个用于产生fake data的module

lipsum - is a simple Lorem Ipsum generator library which can be used in your Python applications
- https://github.com/thanethomson/lipsum
radar - Random date generation
- https://pypi.org/project/radar/
mimesis - is a fast and easy to use library for Python programming language, which helps generate mock data for a variety of purposes in a variety of languages
- https://lk-geimfari.github.io/mimesis/
Faker - is a Python package that generates fake data for you
- https://faker.readthedocs.io/en/master/
