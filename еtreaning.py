def some_func(a, b, c, d, **kwargs):
    print(a, b, c, d, kwargs)


some_func(4,5,6, **dict(a='hello', b='Andy', c='vorzkla', d='age27', f='123'))