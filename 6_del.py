
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner



class MyException(Exception):
    """MyException"""


# Generator delegation simple example

# def subgen():
#     for i in 'world':
#         yield i

# def delegator(g):
#     for i in g:
#         yield i

# sg = subgen()
# g = delegator(sg)
# print(list(g))


# example 2 (with send)

# @coroutine
# def subgen():
#     while True:
#         message = yield
#         print('.......', message)

# @coroutine
# def delegator(g):
#     while True:
#         data = yield
#         g.send(data)

# sg = subgen()
# g = delegator(sg)



# example 3 (with send and try-except)

# @coroutine
# def subgen():
#     while True:
#         try:
#             message = yield
#         except MyException:
#             print('subgen exception MyException')
#         else:
#             print('.......', message)

# @coroutine
# def delegator(g):
#     while True:
#         try:
#             data = yield
#             g.send(data)
#         except MyException as e:
#             print('delegator exception MyException')
#             g.throw(e)


# sg = subgen()
# g = delegator(sg)

# g.send('OK')


# example 4 (with yield from)

def subgen():
    while True:
        try:
            message = yield
        except MyException:
            print('subgen exception MyException')
        except StopIteration:
            print('subgen StopIteration')
            break
        else:
            print('.......', message)
    return 'Returning from subgen'

@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except MyException as e:
    #         print('delegator exception MyException')
    #         g.throw(e)
    result = yield from g
    print(result)


sg = subgen()
g = delegator(sg)

g.send('OK')



