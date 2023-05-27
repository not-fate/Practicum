import _md5

salt = 'i wanna die'

password = '1234'
password2 = '1234'
print(_md5.md5((password + salt).encode()).hexdigest() == _md5.md5((password2 + salt).encode()).hexdigest())
