# -*- coding: utf-8 -*-

class GuestUserException(Exception):
    pass


class GuestUser:
    uid = None
    username = ''
    division = ''
    first_name = ''
    last_name = ''
    email = ''

    def __init__(self, uid):
        if len(uid) == 8 and uid.rstrip('0123456789').lower() == 'guest':
            self.uid = uid.lower()
            self.uername = uid.lower()
            self.division = 'ゲスト部'
            self.first_name = 'ゲスト'
            self.last_name = uid[5:]
            self.email = uid.lower() + '@example.jp'
        else:
            raise GuestUserException('No such user: ' + uid)

    def copyto(self, obj):
        obj.uid = self.uid
        obj.username = self.uid
        obj.division = self.division
        obj.first_name = self.first_name
        obj.last_name = self.last_name
        obj.email = self.email

    def __str__(self):
        return f'{self.uid}/{self.division}/{self.first_name}/{self.email}'


if __name__ == '__main__':
    try:
        a = GuestUser('f8317610')
        print(a)
    except Exception as e:
        print(e)

    try:
        a = GuestUser('guest999')
        print(a)
    except Exception as e:
        print(e)
