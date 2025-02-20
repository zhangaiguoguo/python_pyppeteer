import os
import shutil
from datetime import datetime, timedelta
import time

import schedule

SCHEDULED_TIME_TASK_OPTIONS = {
    'days_not_accessed': 1,
    'directory_to_clean': os.path.normpath(os.path.join(os.path.dirname(__file__), r'./myapp/static/pdf'))
}


def find_and_delete_old_pdfs(directory, days_threshold):
    data_format = "%Y-%m-%d"
    # 转换天数阈值为秒
    threshold_time = datetime.strptime(
        datetime.fromtimestamp(time.time() - days_threshold * 86400).strftime(data_format), data_format).timestamp()

    # 遍历目录中的文件
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if (datetime.strptime(dir, data_format).timestamp()) < threshold_time:
                dir_path = os.path.join(root, dir)
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"remove dir({dir_path}) error: ", e)


def job():
    # 调用函数进行清理
    find_and_delete_old_pdfs(SCHEDULED_TIME_TASK_OPTIONS['directory_to_clean'],
                             SCHEDULED_TIME_TASK_OPTIONS['days_not_accessed'])


def run():
    # 安排任务在每天的23:00执行
    schedule.every().day.at("23:00").do(job)
    while True:
        # 运行所有可运行的任务
        schedule.run_pending()

        # 计算到下一个23:00的时间差
        now = datetime.now()
        # 获取今天的23:00
        today_2300 = now.replace(hour=23, minute=0, second=0, microsecond=0)
        # 如果现在已经是明天的凌晨或之后，则获取明天的23:00
        if now > today_2300:
            next_run = today_2300 + timedelta(days=1)
        else:
            next_run = today_2300

        # 计算时间差并转换为秒
        time_to_sleep = (next_run - now).total_seconds()

        # 如果时间差超过一小时（为了避免过于频繁的检查），则至少睡眠一小时
        if time_to_sleep > 3600:
            time_to_sleep = 3600 - (now.second + now.microsecond / 1e6) % 3600  # 精确到下一个整点（或更短时间）

        # 睡眠直到下一个检查点
        time.sleep(time_to_sleep)


# job()
run()
