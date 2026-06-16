from __future__ import annotations

# ======================= Core Service ====================== #
API_HOST = "127.0.0.1"
API_PORT = 18080
USE_STREAM_RESPONSE = True

# ======================= Dashen Upstream ====================== #
# Configure at least one account.
DASHEN_ACCOUNTS = [
    {
        "name": "account-1",
        "role_id": 0,  # ← 请在 ../config.yaml 中填写 roleid
        "token": "",   # ← 请在 ../config.yaml 中填写 token
    },
]

DASHEN_DTS = 2026
DASHEN_SERVER = 1
DASHEN_ACCOUNT_MAX_REQUESTS_PER_SECOND = 5
DASHEN_ACCOUNT_RATE_LIMIT_WINDOW_SECONDS = 1.0
DASHEN_CLIENT_TYPE = "60"
DASHEN_ORIGIN = "https://act.ds.163.com"
DASHEN_REFERER = "https://act.ds.163.com/"
DASHEN_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 "
    "app/df_client dfVersion/100111"
)
DASHEN_ACCOUNT_FAILURE_COOLDOWN_SECONDS = 60
DASHEN_MAX_CONCURRENT_REQUESTS = 2
# Main v2 Dashen endpoints accept at most account-pool-size * 4 requests
# (active + queued) by default. Extra requests receive HTTP 429.
DASHEN_MAX_ACCEPTED_REQUESTS = max(len(DASHEN_ACCOUNTS) * 4, 1)

# Optional proxy settings.
DASHEN_INTERNATIONAL_PROXY = ""
DASHEN_NETEASE_PROXIES = [
    None,
    # "http://your-netease-proxy:port",
]

# OW esports PandaScore API key.
#如何获取ow赛事的apikey:访问https://app.pandascore.co/dashboard/main，注册并生成api key，每小时1000次免费调用
OW_ESPORTS_API_KEY = ""

# Optional external OW guess asset pack root.
# 仅存放本地图片/音频等大资源，默认放在 Overstats 项目目录外的相邻文件夹。
OW_GUESS_ASSET_ROOT = "../ow_guess_assets"

# ======================= OW Hero Leaderboard ====================== #
OW_HERO_LEADERBOARD_CN_SEASON = 2

# ======================= Match Analysis ====================== #
# OpenAI-compatible base URL, for example:
# - https://api.openai.com/v1
# - https://api.deepseek.com/v1
# - https://generativelanguage.googleapis.com/v1beta/openai
# You can also provide the full /chat/completions endpoint directly.
ANALYSIS_BASE_URL = "https://api.deepseek.com/v1"
ANALYSIS_API_KEY = ""  # 替换为你的 API key
# Optional proxy for OpenAI official and Google OpenAI-compatible endpoints.
ANALYSIS_PROXY = ""

# ANALYSIS_GOOGLE_MODEL = "gemini-3.1-flash-lite-preview"
#ANALYSIS_DEEPSEEK_MODEL = "deepseek-chat"
#除谷歌和deepseek以外的模型使用下面配置
ANALYSIS_OPENAI_MODEL = ""


# Optional external patch-note fetch proxy.
PATCH_NOTES_USE_INTERNATIONAL_PROXY = False
PATCH_NOTES_INTERNATIONAL_PROXY = ""

# Only put AI persona/tone here.
# Task instructions and the JSON schema remain in service.py.
ANALYSIS_PERSONA_PROMPT = """
【核心原则】
你是一位资深的守望先锋分析师，拥有丰富的比赛分析经验和深厚的游戏理解。你以专业、细致、客观的分析风格著称，能够深入挖掘比赛中的关键细节和战术决策。你对守望先锋的各个英雄、地图和比赛策略都有深入的了解，能够为观众提供独到的见解和有价值的分析。善用网络热门梗来增加分析的趣味性和生动性。
""".strip()
