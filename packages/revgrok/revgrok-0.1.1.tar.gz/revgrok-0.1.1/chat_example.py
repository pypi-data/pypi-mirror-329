import asyncio

from revgrok import GrokClient


async def main():
    cookie = "sso=eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiNmM4ZDQyMDgtMmYzNy00MTA4LTljNGQtZmRmOGVhNWI0ZDNjIn0.X-H6U-KxMnBT1xnU0Jm905VyhMx8u5QEHbIqhb1t1AM; sso-rw=eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiNmM4ZDQyMDgtMmYzNy00MTA4LTljNGQtZmRmOGVhNWI0ZDNjIn0.X-H6U-KxMnBT1xnU0Jm905VyhMx8u5QEHbIqhb1t1AM; x-anonuserid=3e899a87-c42c-467e-9429-07d797f59d69; x-challenge=LzKyLiGsDyNAALOU2dm0LxNCUNX5aA1gb6uWkrw6mf0iJDg8oIxyz%2BUz%2FK7vMTHrRCuDbbC5WiT1x7vPiwN0tbp66%2FVgSsFz7wGpoGu9g7vildJVe1r8AGUvA10Wn3uRd2GYfRwgPh5JdTb88F59588CLmChy3hqYVZNKuyZcaaqD1d9SM4%3D; x-signature=4MWnJ2Xah3o5AzE1MI%2F56mBf7MAzzujbQ%2BHcLVNWCewrYIWKfyOAFSwKmnHlymVyePWZZ%2F0b5BE5vLKCrokpOg%3D%3D"
    model = "grok-3"  # base model
    prompt = "9.8 and 9.11 which is bigger?"
    client = GrokClient(cookie=cookie)
    async for response in client.chat(prompt=prompt, model=model, reasoning=True):
        print(response, end="")


if __name__ == "__main__":
    asyncio.run(main())
