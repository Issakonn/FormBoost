"""
FormBoost Telegram Bot
Run: python bot.py
"""
import asyncio
import logging
import os
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, LabeledPrice, PreCheckoutQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN    = "8311955431:AAHNZ2_4Db0VZZNFUYGQMaS7NzNaNjhgaxY"   # ← замени
MINI_APP_URL = "https://formboost.onrender.com"                             # ← замени
ADMIN_ID     = 123456789                                              # ← замени свой telegram id
KASPI_CARD   = "4400 4303 4396 2079"                                 # ← замени
KASPI_NAME   = "Ислам И"                                            # ← замени
DB_PATH      = "formboost.db"

PACKAGES = {
    "p10":  {"votes": 10,  "tenge": 100,  "stars": 17,  "label": "10 голосов"},
    "p50":  {"votes": 50,  "tenge": 450,  "stars": 75,  "label": "50 голосов"},
    "p100": {"votes": 100, "tenge": 800,  "stars": 133, "label": "100 голосов"},
    "p500": {"votes": 500, "tenge": 3500, "stars": 583, "label": "500 голосов"},
}

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ─── FSM ─────────────────────────────────────────────────────────────────────
class KaspiState(StatesGroup):
    waiting = State()

pending_kaspi: dict[int, int] = {}  # user_id -> tx_id

# ─── DB ──────────────────────────────────────────────────────────────────────
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT, full_name TEXT,
                balance INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, type TEXT, package TEXT,
                votes INTEGER, tenge INTEGER, stars INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now')),
                confirmed_at TEXT
            );
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, form_url TEXT,
                votes_requested INTEGER, votes_sent INTEGER,
                status TEXT, created_at TEXT DEFAULT (datetime('now'))
            );
        """)
        await db.commit()

async def ensure_user(user: types.User):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id,username,full_name) VALUES (?,?,?)",
            (user.id, user.username or "", user.full_name or "")
        )
        await db.commit()

async def get_balance(uid: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute("SELECT balance FROM users WHERE user_id=?", (uid,))).fetchone()
        return row["balance"] if row else 0

async def add_votes(uid: int, votes: int, tenge: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET balance=balance+?, total_spent=total_spent+? WHERE user_id=?",
            (votes, tenge, uid)
        )
        await db.commit()

async def create_tx(uid, type_, pkg, votes, tenge, stars, status="pending") -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO transactions (user_id,type,package,votes,tenge,stars,status) VALUES (?,?,?,?,?,?,?)",
            (uid, type_, pkg, votes, tenge, stars, status)
        )
        await db.commit()
        return cur.lastrowid

async def confirm_tx(tx_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        tx = await (await db.execute("SELECT * FROM transactions WHERE id=?", (tx_id,))).fetchone()
        if not tx or tx["status"] != "pending":
            return None
        await db.execute(
            "UPDATE transactions SET status='confirmed', confirmed_at=datetime('now') WHERE id=?",
            (tx_id,)
        )
        await db.execute(
            "UPDATE users SET balance=balance+?, total_spent=total_spent+? WHERE user_id=?",
            (tx["votes"], tx["tenge"], tx["user_id"])
        )
        await db.commit()
        return dict(tx)

async def reject_tx(tx_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE transactions SET status='rejected' WHERE id=?", (tx_id,))
        await db.commit()

async def get_runs(uid: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM runs WHERE user_id=? ORDER BY created_at DESC LIMIT 15", (uid,)
        )).fetchall()
        return [dict(r) for r in rows]

# ─── KEYBOARDS ───────────────────────────────────────────────────────────────
def kb_main(balance: int, uid: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 Открыть приложение", web_app=WebAppInfo(url=f"{MINI_APP_URL}?uid={uid}"))
    kb.button(text=f"💎 Баланс: {balance} гол.", callback_data="cb_balance")
    kb.button(text="💳 Купить голоса",          callback_data="cb_shop")
    kb.button(text="📋 История запусков",        callback_data="cb_history")
    kb.button(text="❓ Помощь",                  callback_data="cb_help")
    kb.adjust(1, 2, 2)
    return kb.as_markup()

def kb_shop() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, p in PACKAGES.items():
        kb.button(text=f"{p['label']} — {p['tenge']} ₸", callback_data=f"pkg_{key}")
    kb.button(text="◀️ Назад", callback_data="cb_main")
    kb.adjust(1)
    return kb.as_markup()

def kb_pay_method(pkg_key: str) -> InlineKeyboardMarkup:
    p = PACKAGES[pkg_key]
    kb = InlineKeyboardBuilder()
    kb.button(text=f"⭐ Stars ({p['stars']} ⭐)",  callback_data=f"stars_{pkg_key}")
    kb.button(text=f"💳 Kaspi ({p['tenge']} ₸)",   callback_data=f"kaspi_{pkg_key}")
    kb.button(text="◀️ Назад",                      callback_data="cb_shop")
    kb.adjust(1)
    return kb.as_markup()

# ─── HANDLERS: START / MAIN ───────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    await ensure_user(msg.from_user)
    bal = await get_balance(msg.from_user.id)
    await msg.answer(
        f"👋 Привет, *{msg.from_user.first_name}*\\!\n\n"
        f"FormBoost — генерация ответов для Google Forms\n\n"
        f"💎 Твой баланс: *{bal} голосов*\n"
        f"📦 10 голосов = 100 ₸",
        parse_mode="MarkdownV2",
        reply_markup=kb_main(bal, msg.from_user.id)
    )

@dp.callback_query(F.data == "cb_main")
async def cb_main(call: types.CallbackQuery):
    bal = await get_balance(call.from_user.id)
    await call.message.edit_text(
        f"🏠 *Главное меню*\n💎 Баланс: *{bal} голосов*",
        parse_mode="Markdown",
        reply_markup=kb_main(bal, call.from_user.id)
    )
    await call.answer()

@dp.callback_query(F.data == "cb_balance")
async def cb_balance(call: types.CallbackQuery):
    bal = await get_balance(call.from_user.id)
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        txs = await (await db.execute(
            "SELECT * FROM transactions WHERE user_id=? AND status='confirmed' ORDER BY confirmed_at DESC LIMIT 5",
            (call.from_user.id,)
        )).fetchall()
    hist = ""
    for t in txs:
        hist += f"\n  \\+{t['votes']} гол\\. ({t['type']}, {t['tenge']}₸)"
    await call.message.edit_text(
        f"💎 *Баланс: {bal} голосов*\n"
        + (f"\n*Последние покупки:*{hist}" if hist else "\n_Покупок ещё нет_"),
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="💳 Купить", callback_data="cb_shop"),
            InlineKeyboardButton(text="◀️ Назад",  callback_data="cb_main"),
        ]])
    )
    await call.answer()

@dp.callback_query(F.data == "cb_history")
async def cb_history(call: types.CallbackQuery):
    runs = await get_runs(call.from_user.id)
    if not runs:
        text = "📋 *История запусков*\n\n_Запусков ещё не было_"
    else:
        text = "📋 *История запусков*\n\n"
        for r in runs:
            date = r["created_at"][:10]
            text += f"• {date} — {r['votes_sent']}/{r['votes_requested']} гол, {r['status']}\n"
    await call.message.edit_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="◀️ Назад", callback_data="cb_main")
        ]])
    )
    await call.answer()

@dp.callback_query(F.data == "cb_help")
async def cb_help(call: types.CallbackQuery):
    await call.message.edit_text(
        "❓ *Как пользоваться*\n\n"
        "1\\. Купи голоса \\(💳 Купить голоса\\)\n"
        "2\\. Нажми *Открыть приложение*\n"
        "3\\. Вставь ссылку Google Form\n"
        "4\\. Приложение найдёт все вопросы\n"
        "5\\. Настрой распределение ответов\n"
        "6\\. Для открытых вопросов — ИИ сам придумает ответы\n"
        "7\\. Укажи количество и запускай\\!\n\n"
        "💬 Поддержка: @your\\_support",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="◀️ Назад", callback_data="cb_main")
        ]])
    )
    await call.answer()

# ─── SHOP ─────────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "cb_shop")
async def cb_shop(call: types.CallbackQuery):
    await call.message.edit_text(
        "💳 *Купить голоса*\n\n"
        "Выбери пакет\\. Голоса зачисляются мгновенно\\.",
        parse_mode="MarkdownV2",
        reply_markup=kb_shop()
    )
    await call.answer()

@dp.callback_query(F.data.startswith("pkg_"))
async def cb_pkg(call: types.CallbackQuery):
    key = call.data[4:]
    p   = PACKAGES[key]
    await call.message.edit_text(
        f"📦 *{p['label']}*\n\n"
        f"Стоимость: *{p['tenge']} ₸* или *{p['stars']} ⭐ Stars*\n\n"
        f"Выбери способ оплаты:",
        parse_mode="Markdown",
        reply_markup=kb_pay_method(key)
    )
    await call.answer()

# ─── STARS ────────────────────────────────────────────────────────────────────
@dp.callback_query(F.data.startswith("stars_"))
async def cb_stars(call: types.CallbackQuery):
    key = call.data[6:]
    p   = PACKAGES[key]
    await call.answer()
    await bot.send_invoice(
        chat_id    = call.from_user.id,
        title      = f"FormBoost — {p['label']}",
        description= f"Пополнение баланса на {p['votes']} голосов",
        payload    = f"{key}:{call.from_user.id}",
        currency   = "XTR",
        prices     = [LabeledPrice(label=p["label"], amount=p["stars"])],
    )

@dp.pre_checkout_query()
async def pre_checkout(q: PreCheckoutQuery):
    await q.answer(ok=True)

@dp.message(F.successful_payment)
async def on_stars_paid(msg: types.Message):
    key, uid_str = msg.successful_payment.invoice_payload.split(":")
    uid = int(uid_str)
    p   = PACKAGES[key]
    await create_tx(uid, "stars", key, p["votes"], p["tenge"], p["stars"], status="confirmed")
    await add_votes(uid, p["votes"], p["tenge"])
    bal = await get_balance(uid)
    await msg.answer(
        f"✅ *Оплата прошла\\!*\n\n"
        f"\\+{p['votes']} голосов добавлено\n"
        f"💎 Баланс: *{bal} голосов*",
        parse_mode="MarkdownV2",
        reply_markup=kb_main(bal, uid)
    )

# ─── KASPI ────────────────────────────────────────────────────────────────────
@dp.callback_query(F.data.startswith("kaspi_"))
async def cb_kaspi(call: types.CallbackQuery, state: FSMContext):
    key = call.data[6:]
    p   = PACKAGES[key]
    tx_id = await create_tx(
        call.from_user.id, "kaspi", key,
        p["votes"], p["tenge"], 0, status="pending"
    )
    pending_kaspi[call.from_user.id] = tx_id
    await state.set_state(KaspiState.waiting)
    await call.message.edit_text(
        f"💳 *Оплата через Kaspi*\n\n"
        f"Сумма: *{p['tenge']} ₸*\n\n"
        f"1️⃣ Переведи *{p['tenge']} ₸* на карту:\n"
        f"`{KASPI_CARD}`\n"
        f"Получатель: *{KASPI_NAME}*\n\n"
        f"2️⃣ В комментарии укажи:\n"
        f"`FB\\-{tx_id}`\n\n"
        f"3️⃣ Отправь скриншот сюда ↓\n\n"
        f"_Голоса придут в течение 15 минут_",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="❌ Отмена", callback_data="kaspi_cancel")
        ]])
    )
    await call.answer()

@dp.callback_query(F.data == "kaspi_cancel")
async def cb_kaspi_cancel(call: types.CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    tx_id = pending_kaspi.pop(uid, None)
    if tx_id:
        await reject_tx(tx_id)
    await state.clear()
    bal = await get_balance(uid)
    await call.message.edit_text(
        "Оплата отменена.",
        reply_markup=kb_main(bal, uid)
    )
    await call.answer()

@dp.message(KaspiState.waiting, F.photo)
async def on_kaspi_screenshot(msg: types.Message, state: FSMContext):
    uid   = msg.from_user.id
    tx_id = pending_kaspi.get(uid)
    if not tx_id:
        await state.clear()
        return

    # Пересылаем скрин + кнопки подтвердить/отклонить — админу
    await bot.forward_message(ADMIN_ID, uid, msg.message_id)
    await bot.send_message(
        ADMIN_ID,
        f"💳 *Новая заявка Kaspi*\n\n"
        f"TX: `{tx_id}`\n"
        f"Пользователь: @{msg.from_user.username or '—'} \\(id: `{uid}`\\)\n"
        f"Код: `FB\\-{tx_id}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"adm_ok_{tx_id}_{uid}"),
            InlineKeyboardButton(text="❌ Отклонить",   callback_data=f"adm_no_{tx_id}_{uid}"),
        ]])
    )
    await state.clear()
    pending_kaspi.pop(uid, None)
    await msg.answer(
        "📨 *Скриншот получен\\!*\n\n"
        f"Заявка \\#{tx_id} на проверке\\.\n"
        "Уведомление придёт автоматически 🔔",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🏠 Меню", callback_data="cb_main")
        ]])
    )

@dp.message(KaspiState.waiting)
async def on_kaspi_wrong(msg: types.Message):
    await msg.answer("📸 Нужен скриншот (фото). Отправь фото чека Kaspi.")

# ─── ADMIN ────────────────────────────────────────────────────────────────────
@dp.callback_query(F.data.startswith("adm_ok_"))
async def adm_confirm(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return await call.answer("Нет доступа", show_alert=True)
    _, _, tx_str, uid_str = call.data.split("_", 3)
    tx_id = int(tx_str); uid = int(uid_str)
    tx = await confirm_tx(tx_id)
    if not tx:
        return await call.answer("Уже обработано", show_alert=True)
    bal = await get_balance(uid)
    await call.message.edit_text(f"✅ Подтверждено TX#{tx_id} → +{tx['votes']} гол. юзеру {uid}")
    await bot.send_message(
        uid,
        f"🎉 *Оплата подтверждена\\!*\n\n"
        f"\\+{tx['votes']} голосов добавлено\n"
        f"💎 Баланс: *{bal} голосов*",
        parse_mode="MarkdownV2",
        reply_markup=kb_main(bal, uid)
    )
    await call.answer("Подтверждено ✅")

@dp.callback_query(F.data.startswith("adm_no_"))
async def adm_reject(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return await call.answer("Нет доступа", show_alert=True)
    _, _, tx_str, uid_str = call.data.split("_", 3)
    tx_id = int(tx_str); uid = int(uid_str)
    await reject_tx(tx_id)
    await call.message.edit_text(f"❌ Отклонено TX#{tx_id}")
    await bot.send_message(
        uid,
        f"❌ *Оплата не подтверждена*\n\nЗаявка \\#{tx_id} отклонена\\.\n"
        f"Вопросы — @your\\_support",
        parse_mode="MarkdownV2",
        reply_markup=kb_main(await get_balance(uid), uid)
    )
    await call.answer("Отклонено ❌")

@dp.message(Command("stats"))
async def cmd_stats(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        users  = (await (await db.execute("SELECT COUNT(*) as c FROM users")).fetchone())["c"]
        income = (await (await db.execute("SELECT COALESCE(SUM(tenge),0) as s FROM transactions WHERE status='confirmed'")).fetchone())["s"]
        runs   = (await (await db.execute("SELECT COUNT(*) as c FROM runs")).fetchone())["c"]
    await msg.answer(
        f"📊 *Статистика*\n\n"
        f"👤 Пользователей: {users}\n"
        f"💰 Доход: {income} ₸\n"
        f"🚀 Запусков: {runs}",
        parse_mode="Markdown"
    )

# ─── MAIN ─────────────────────────────────────────────────────────────────────
async def main():
    await init_db()
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
