#!/bin/bash
# FormBoost — запуск всего проекта
# Использование: bash start.sh

echo "🚀 Запуск FormBoost..."

# Проверяем зависимости
if ! python3 -c "import aiogram" 2>/dev/null; then
  echo "📦 Устанавливаем зависимости..."
  pip install -r requirements.txt
fi

# Запускаем сервер и бота параллельно
echo "🌐 Запуск API сервера на порту 8000..."
uvicorn server:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

sleep 1

echo "🤖 Запуск Telegram бота..."
python3 bot.py &
BOT_PID=$!

echo ""
echo "✅ Всё запущено!"
echo "   Сервер PID: $SERVER_PID"
echo "   Бот    PID: $BOT_PID"
echo ""
echo "Для остановки: Ctrl+C или kill $SERVER_PID $BOT_PID"

# Ждём Ctrl+C
trap "echo 'Останавливаем...'; kill $SERVER_PID $BOT_PID 2>/dev/null; exit" INT TERM
wait
