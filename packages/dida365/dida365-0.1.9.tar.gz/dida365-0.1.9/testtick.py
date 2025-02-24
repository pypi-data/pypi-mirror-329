from dida365 import * 
import asyncio



async def main():
    client = Dida365Client()
    print(f"client service type {client.service_type}")
    await client.authenticate()

if __name__ == "__main__":
    asyncio.run(main())