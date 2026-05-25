import os, asyncio
from dotenv import load_dotenv
load_dotenv()
from services.ai_service import call_llama

# make sure model env is set
os.environ.setdefault('MODEL','meta-llama/llama-3-8b-instruct')

async def main():
    result = await call_llama('Say something interesting about chennai institute of technology.')
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
