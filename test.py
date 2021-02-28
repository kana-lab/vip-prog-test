import argparse
import urllib.parse
import re
import requests


BOARD_URL = 'https://hebi.5ch.net/news4vip/'
READ_URL = 'https://hebi.5ch.net/test/read.cgi/news4vip/'
CHARSET = 'MS932'


parser = argparse.ArgumentParser(
    description='VIP のスレ一覧を検索するすごいやつだよ',
)
parser.add_argument('keyword', help='キーワード', type=str)
args = parser.parse_args()


response = requests.get(urllib.parse.urljoin(BOARD_URL, 'subject.txt'))
response.raise_for_status()

subjects_raw = response.content.decode(CHARSET)
threads = []

for line in subjects_raw.split('\n'):
    m = re.match(r'(?P<id>\d+)\.dat<>(?P<subject>.+)  \(\d+\)', line)

    if m:
        threads.append((int(m.group('id')), m.group('subject')))


for thread in threads:
    if args.keyword in thread[1]:
        print(f'Found: {thread[1]}')
        print(f'{READ_URL}{thread[0]}')
