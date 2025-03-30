import asyncio
import aiohttp
import schedule
import time


urls = [
    "https://youshou.ru/",
    "https://lawsartland.com/",
    "https://www.gagarin.live/",
    "https://vitalityofnature.ru/",
    "https://australeco.ru/",
    "https://ntdcosmetic.ru/",
    "https://qwertydsjfbnvs.ru/", # это заведомо неверный адрес чтобы выкинуло ошибку
    "https://ntdcosmetic.ru/iwujhef", # то верный юрл адрес, но с неверной страницей перехода
]


async def check_website(session, url):
    """Функция для проверки одного сайта"""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                print(f"Сайт {url} доступен")
            else:
                print(f"Сайт {url} доступен, но код ответа не верный: {response.status}")
    except asyncio.TimeoutError:
        print(f"Сайт {url} недоступен. Ошибка: время ожидания истекло.")
    except Exception as e:
        print(f"Сайт {url} недоступен. Ошибка: {e}")


async def run_check(urls):
    """Асинхронная проверка списка сайтов"""
    async with aiohttp.ClientSession() as session:
        tasks = [check_website(session, url) for url in urls]
        await asyncio.gather(*tasks)


def check_websites_at_fixed_time():
    """Обёртка для запуска асинхронной проверки в scheduler"""
    asyncio.run(run_check(urls))

schedule.every().day.at("10:00").do(check_websites_at_fixed_time)
print("Планировщик запущен. Проверка будет выполняться каждый день в 10:00")


while True:
    schedule.run_pending()
    time.sleep(1)
