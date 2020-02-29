from src.telegram.telegram_messenger import TelegramMessenger

import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tg = TelegramMessenger(loop)
    tg.start_pooling()