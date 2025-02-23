# 引用py文件
from . import log
from . import config

import platform
if platform.system() == "Windows":
    from . import regEdit
