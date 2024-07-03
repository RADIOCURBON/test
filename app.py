import requests
from bs4 import BeautifulSoup
import schedule
import time
import sqlite3
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Список URL каналов в Telegram
channel_urls = [
    'https://t.me/hamster_kombat',
    'https://t.me/blumcrypto',
    'https://t.me/beetongamechat',
    'https://t.me/fueljetton',
    'https://t.me/orbitonxru',
    'https://t.me/tonarbuz',
    'https://t.me/CatizenAnn',
    'https://t.me/punkcitymain',
    'https://t.me/icebergen',
    'https://t.me/pixelverse_xyz',
    'https://t.me/drophunter_games',
    'https://t.me/memeficlub',
    'https://t.me/wateronbsc',
    'https://t.me/dotcoincommunity',
    'https://t.me/the_vertus',
    'https://t.me/HoldBull',
    'https://t.me/topcoinme',
    'https://t.me/tonstationgames',
    'https://t.me/diamoremarket',
    'https://t.me/TimeFarmChannel',
]

channel_names = [
    'Hamster',
    'Blum',
    'BeeTon',
    'Fuel',
    'OrbitonX',
    'Arbuz',
    'Catizen',
    'Cubes',
    'Iceberg',
    'Pixelverse',
    'DropHunter',
    'MemeFi',
    'Water',
    'Dotcoin',
    'Vertus',
    'BullRun',
    'Topcoin',
    'TONStation',
    'Diamore',
    'TimeFarm'
]

def create_database():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                 (channel_url TEXT PRIMARY KEY, timestamp TEXT, subscriber_count INTEGER)''')
    conn.commit()
    conn.close()

def get_subscribers_count(channel_url):
    try:
        response = requests.get(channel_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        subscribers_info = soup.find('div', class_='tgme_page_extra')
        if subscribers_info:
            subscribers_text = subscribers_info.text.strip()
            if 'members' in subscribers_text:
                subscribers_text = subscribers_text.split(' members')[0].replace(',', '')
            elif 'subscribers' in subscribers_text:
                subscribers_text = subscribers_text.split(' subscribers')[0].replace(',', '')
            elif 'online' in subscribers_text:
                subscribers_text = subscribers_text.split(' online')[0].replace(',', '')
            if ' ' in subscribers_text and all(c.isdigit() or c == ' ' for c in subscribers_text):
                subscribers_text = subscribers_text.replace(' ', '')
            return int(subscribers_text)
        else:
            print(f"Информация о подписчиках для канала {channel_url} не найдена.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса для канала {channel_url}: {e}")
        return None

def save_to_database(data):
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    for entry in data:
        c.execute('''INSERT OR REPLACE INTO subscribers (channel_url, timestamp, subscriber_count)
                     VALUES (?, ?, ?)''', (entry['channel_url'], entry['timestamp'], entry['subscriber_count']))
    conn.commit()
    conn.close()

def job():
    subscribers_counts = []
    for url in channel_urls:
        count = get_subscribers_count(url)
        if count is not None:
            subscribers_counts.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'channel_url': url,
                'subscriber_count': count
            })
        time.sleep(1)
    save_to_database(subscribers_counts)
    print(subscribers_counts)

schedule.every(1).minutes.do(job)

def get_subscribers():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute("SELECT channel_url, subscriber_count FROM subscribers")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    subscribers = get_subscribers()
    data = {url: count for url, count in subscribers}
    return render_template('index.html', data=data, channel_names=zip(channel_urls, channel_names))

if __name__ == '__main__':
    create_database()
    import threading
    data_thread = threading.Thread(target=lambda: schedule.run_all())
    data_thread.start()
    app.run(debug=True)
