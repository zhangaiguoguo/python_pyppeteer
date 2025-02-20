#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys
from multiprocessing import Process


def run_scheduled_tasks():
    # 注意：这里我们不再需要指定完整的 Python 解释器路径，因为
    # 我们假设这个脚本是在与 Django 项目相同的 Python 环境中运行的。
    script_path = os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scheduled_time_tasks.py'))
    subprocess.run([sys.executable, script_path, '--multiprocessing-fork'])  # 使用当前 Python 解释器


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    task_process = Process(target=run_scheduled_tasks)
    task_process.start()
    # task_process.join()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
