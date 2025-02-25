# HammrahAval

A library for HammrahAval Application

```python
import HammrahAval, asyncio

# Replace with your actual phone number
PhoneNumber = "9123456789"

async def Test():
    async with HammrahAval.Client(PhoneNumber) as client:
        if hasattr(client, "NumberOfTry"): Login = await client.Login(input("Inter the 4 digit code : "))
        else: Login = True
        
        if Login:
            print(await client.GetMe())
            print(await client.GetMySIMCards())
            print(await client.GetMyBalance())
            print(await client.GetMyPackages())
            print(await client.GetMyScore())

asyncio.run(Test())
```