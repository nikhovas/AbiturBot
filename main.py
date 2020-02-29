# from src.telegram.telegram_messenger import TelegramMessenger
# from src import kernel
from src.app_config import kernel, TelegramMessenger
# from src.kernel import
import asyncio

# kernel: Kernel = Kernel()

if __name__ == "__main__":
    tg = TelegramMessenger(kernel)
    tg.start_pooling()
