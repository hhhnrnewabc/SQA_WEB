from setuptools import setup, find_packages
import SQA_Project

setup(
    name='sqa_project_web',
    version=SQA_Project.__version__,
    keywords=('simple', 'test'),
    description='SQA Project WEB with Django',
    long_description = open('README.md').read(),
    license='GPLv3',
    platforms = 'any',
    install_requires=['Django>=1.6.5',
                      'pillow',
                      'pymysql',
                      'djangorestframework',
                      'markdown',
                      'django-filter',
                      'django-bootstrap-form',
                      'pytz',
                      'django-taggit',
                      'django-grappelli',
                      'south',
                      ],

    author='swim-fish',
    author_email='hhhnrnew82@gmail.com',
    url='https://github.com/hhhnrnewabc/SQA_WEB',

    packages=find_packages(),

    package_data={"": ['*.html', '*.css', '*.rst', '*.png', '*.ico',
                       '*.jpeg', '*.jpg', '*.ttf', '*.svg', '*.eot',
                       '*.woff', '*.text', '*.js', '*.po'
                       ]}



)
