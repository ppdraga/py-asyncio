

def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner

@coroutine
def subgen():
    print('Before yield')
    x = 'Ready to accept message'
    message = yield x
    print('Subgen received:', message)



class MyException(Exception):
    """MyException"""

@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done!')
            break
        except MyException:
            print('........')
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
    return average


g = average()
av = g.send(6)
print(av)
av = g.send(4)
print(av)
av = g.send(16)
print(av)
av = g.send(26)
print(av)

try:
    g.throw(MyException)
except StopIteration as e:
    print(e.value)

# g = average()
# g.throw(MyException)
