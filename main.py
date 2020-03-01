# from src.telegram.telegram_messenger import TelegramMessenger
# from src import kernel
from src.app_config import kernel, TelegramMessenger
# from src.kernel import
import asyncio
import sys

# kernel: Kernel = Kernel()

if __name__ == "__main__":
    # sys.setrecursionlimit(10000000)

    tg = kernel.messenger
    tg.start_pooling()
