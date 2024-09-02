# -*- coding: UTF-8 -*-
# @Date    :2023/10/13 14:53
# @Author  :高猛
# @Project :CSVC_PSO 
# @File    :test_all.py
# @IDE     :PyCharm

import os
from datetime import datetime

# 格式化日期时间为字符串，例如：2023-10-13_143025 (年-月-日_时分秒)
formatted_date_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
print(formatted_date_time)