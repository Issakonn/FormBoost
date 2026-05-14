import asyncio
import threading
import uvicorn
from server import app
import bot  # запустит бота

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=10000)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()

asyncio.run(bot.main())
