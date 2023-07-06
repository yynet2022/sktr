# -*- coding: utf-8 -*-

class CompException(Exception):
    pass


_DB = {
    'a001001': {
        'uid': 'a001001',
        'division': '総務部',
        'first_name': '山田',
        'last_name': '太郎',
        'email': 'yamada.taro@example.jp'},
    'b002002': {
        'uid': 'b002002',
        'division': '人事部',
        'first_name': '市川',
        'last_name': '花子',
        'email': 'ichikawa.hanako@example.jp'},
    'c003003': {
        'uid': 'c003003',
        'division': '営業部',
        'first_name': '鈴木',
        'last_name': '一郎',
        'email': 'suzuki.ichiro@example.jp'},
    'd004004': {
        'uid': 'd004004',
        'division': '開発部',
        'first_name': '林',
        'last_name': '京子',
        'email': 'hayashi.kyoko@example.jp'},
}


class COMPUser:
    uid = None
    username = ""
    division = ""
    first_name = ""
    last_name = ""
    email = ""

    def __init__(self, uid):
        z = None
        for x in _DB:
            if x == uid:
                z = _DB[x]
                self.uid = z['uid']
                self.uername = z['uid']
                self.division = z['division']
                self.first_name = z['first_name']
                self.last_name = z['last_name']
                self.email = z['email']
                break
        if z is None:
            raise CompException('No such user: ' + uid)

    def copyto(self, obj):
        obj.uid = self.uid
        obj.username = self.uid
        obj.division = self.division
        obj.first_name = self.first_name
        obj.last_name = self.last_name
        obj.email = self.email

    def __str__(self):
        return f'{self.uid}/{self.division}/{self.first_name}/{self.email}'


if __name__ == "__main__":
    try:
        a = COMPUser("c003003")
        print(a)
    except Exception as e:
        print(e)

    try:
        a = COMPUser("c003113")
        print(a)
    except Exception as e:
        print(e)
