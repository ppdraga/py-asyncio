import asyncio

async def main():
    print('hello')
    await asyncio.sleep(2)
    print('world')



cm = main()
print(cm)
asyncio.run(cm)
