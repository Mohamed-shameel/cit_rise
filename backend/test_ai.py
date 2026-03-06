import os, asyncio
from services.ai_service import call_gemini

# make sure model env is set
os.environ.setdefault('GEMINI_MODEL','gemini-2.5-flash')

async def main():
    result = await call_gemini('Say something interesting about AI.', '')
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
