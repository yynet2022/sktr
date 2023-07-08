#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import datetime

if os.path.dirname(__file__).endswith('contrib'):
    sys.path.append(os.path.dirname(__file__)[:-7])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

from main.models import Seat, Reserve

def main():
    # Seat.objects.all().delete()
    if not Seat.objects.exists():
        make_seats(20)

    seats = []
    for s in Seat.objects.filter(is_active=True):
        seats.append(s)

    # User.objects.all().delete()
    if not User.objects.exists():
        make_users(20)

    users = []
    for u in User.objects.filter(is_active=True):
        users.append(u)

    Reserve.objects.all().delete()
    if not Reserve.objects.exists():
        make_reserves(users, seats, 100)


def make_reserves(users, seats, n):
    for i in range(n):
        s = seats[int(random.random()*len(seats))]
        u = users[int(random.random()*len(users))]
        t = datetime.date.today() + \
            datetime.timedelta(days=int(random.random()*40))
        try:
            r = Reserve.objects.create(user=u, seat=s, date=t)
        except django.db.utils.IntegrityError as e:
            print("Skip", str(t), s.name, u.get_full_name(), str(e))


def make_seats(n):
    for i in range(n):
        n = f'座席-{i:02d}'
        c = '27型FHDモニター'
        try:
            s = Seat.objects.create(name=n, comments=c)
            print('created', s)
        except django.db.utils.IntegrityError as e:
            pass

def make_users(n):
    divisions =['総務部','人事部','営業部','開発部','研究室']
    first_names = ['山本', '西岡', '上杉', '横田', '西田', '麻生', '宮野',
                   '小林', '坂本', '市川', '安倍', '木村', '山口', '伊藤',
                   '谷本', '吉田', '須藤', '大木', '東', '藤崎', '徳川',
                   '佐藤', '上野', '渡辺', '林', '織田', '野上', '井上',
                   '岸本', '藤原', '中村', '佐々木', '青木', '岡野', '鈴木',
                   '山田', '神崎', '三原', '楠木', '松本', '河島', '清水',
                   '足立', '加藤', '陸奥', '島田', '田中']
    last_names = ['太郎', '大和', '義徳', '澪', '結翔', '幸太郎', '風音',
                  '紗奈', '秀樹', '義経', '弥生', '志織', '芽依', '京介',
                  '愛子', '琥太郎', '琢磨', '樹', '莉子', '大雅', '舞子',
                  '京子', '莉緒', '悠真', '慎太郎', '葉月', '一郎', '凛',
                  '俊雄', '竜馬', '武志', '結月', '皐月', '陽葵', '大翔',
                  '治郎', '和真', '孝雄', '裕介', '美紀', '陽翔', '花子',
                  '湊', '幹雄', '勇気', '宗介', '碧', '蓮', '天音', '葵']
    sc = ord('a')
    nc = ord('z') - sc + 1
    for i in range(n):
        kd = int(random.random()*len(divisions))
        kf = int(random.random()*len(first_names))
        kl = int(random.random()*len(last_names))
        ki = int(random.random()*1000000)
        kc = chr(sc + int(random.random()*nc))
        try:
            user = User.objects.create_user(
                uid=f'{kc}{ki:06d}0',
                division=divisions[kd],
                first_name=first_names[kf],
                last_name=last_names[kl],
                email=f'a{ki:06d}0'+'@example.jp',
                is_staff=True,
                is_active=True,
                password='pswd'+f'a{ki:06d}0',
            )
            print('created', user)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
