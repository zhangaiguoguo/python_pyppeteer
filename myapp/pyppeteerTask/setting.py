import os.path

MAX_OPEN_BROWSER_COUNT = 5

SAVE_PDF_PATH = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), r'..\static\pdf'))

node_browser_page_inject_setting = {
    'pageConsoleReturnResponseRef': '__response_send__'
}

start_parm = {
    # 启动chrome的路径
    "executablePath": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    # 关闭无头浏览器 默认是无头启动的
    "headless": True,
    "args": [
        '--disable-infobars',  # 关闭自动化提示框
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--unlimited-storage',
        '--disable-dev-shm-usage',
        '--full-memory-crash-report',
        '--disable-extensions',
        '--mute-audio',
        '--no-zygote',
        '--no-first-run',
        '--start-maximized'
    ],
    "devtools": True,
    "handleSIGINT": False,
    "handleSIGTERM": False,
    "handleSIGHUP": False
}
