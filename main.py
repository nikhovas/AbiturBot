from src.telegram.telegram_messenger import TelegramMessenger
from src import kernel
import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    kernel = kernel.Kernel()
    tg = TelegramMessenger(loop, kernel)
    tg.start_pooling()