import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

class DoblestTikTokAnalyzer:
    def __init__(self, username):
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner()
        self.username = username.lower()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.tiktok.com/',
            'DNT': '1'
        }

    def _print_banner(self):
        print(Fore.CYAN + r"""
   ____       _     _      _   
  |  _ \ ___ | |__ | | ___| |_ 
  | | | / _ \| '_ \| |/ _ \ __|
  | |_| | (_) | |_) | |  __/ |_ 
  |____/ \___/|_.__/|_|\___|\__|
        """)
        print(Fore.YELLOW + "TikTok Account Analyzer v5.0")
        print(Fore.GREEN + "="*50 + "\n")

    def get_user_data(self):
        try:
            url = f"https://www.tiktok.com/@{self.username}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                print(Fore.RED + "[!] Ошибка: Не удалось получить данные (код {})".format(response.status_code))
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            script = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            
            if not script:
                print(Fore.RED + "[!] Не найдены данные пользователя")
                return None

            data = json.loads(script.string)
            user_info = data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {}).get('userInfo', {})
            stats = user_info.get('stats', {})

            return {
                'nickname': user_info.get('user', {}).get('nickname'),
                'username': user_info.get('user', {}).get('uniqueId'),
                'signature': user_info.get('user', {}).get('signature'),
                'verified': user_info.get('user', {}).get('verified'),
                'private': user_info.get('user', {}).get('privateAccount'),
                'create_time': self._convert_timestamp(user_info.get('user', {}).get('createTime')),
                'followers': stats.get('followerCount'),
                'following': stats.get('followingCount'),
                'likes': stats.get('heartCount'),
                'videos': stats.get('videoCount'),
                'digg_count': stats.get('diggCount')
            }

        except Exception as e:
            print(Fore.RED + f"[!] Ошибка: {str(e)}")
            return None

    def _convert_timestamp(self, timestamp):
        if not timestamp:
            return None
        try:
            return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return None

    def _format_number(self, num):
        if num is None:
            return "N/A"
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        if num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)

    def analyze(self):
        user_data = self.get_user_data()
        
        if not user_data:
            print(Fore.RED + "\n[!] Анализ не удался. Возможные причины:")
            print(Fore.YELLOW + "- Аккаунт приватный")
            print(Fore.YELLOW + "- Неверное имя пользователя")
            print(Fore.YELLOW + "- Ограничения TikTok")
            return

        print(Fore.CYAN + "\n[+] Основная информация:")
        print(Fore.GREEN + "="*50)
        print(Fore.YELLOW + f"👤 Имя: {user_data.get('nickname', 'N/A')}")
        print(Fore.YELLOW + f"📛 Ник: @{user_data.get('username', 'N/A')}")
        print(Fore.YELLOW + f"📅 Создан: {user_data.get('create_time', 'N/A')}")
        print(Fore.YELLOW + f"✅ Верифицирован: {'Да' if user_data.get('verified') else 'Нет'}")
        print(Fore.YELLOW + f"🔒 Приватный: {'Да' if user_data.get('private') else 'Нет'}")
        print(Fore.YELLOW + f"📝 Описание: {user_data.get('signature', 'N/A')}")

        print(Fore.CYAN + "\n[+] Статистика:")
        print(Fore.GREEN + "="*50)
        print(Fore.YELLOW + f"👥 Подписчики: {self._format_number(user_data.get('followers'))}")
        print(Fore.YELLOW + f"🤝 Подписки: {self._format_number(user_data.get('following'))}")
        print(Fore.YELLOW + f"❤️ Лайки: {self._format_number(user_data.get('likes'))}")
        print(Fore.YELLOW + f"🎥 Видео: {self._format_number(user_data.get('videos'))}")
        print(Fore.YELLOW + f"👍 Всего лайков: {self._format_number(user_data.get('digg_count'))}")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + "Doblest TikTok Analyzer")
    print(Fore.GREEN + "="*50)
    
    username = input(Fore.YELLOW + "[?] Введите username TikTok (без @): ").strip()
    analyzer = DoblestTikTokAnalyzer(username)
    analyzer.analyze()
