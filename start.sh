"""
FormBoost API Server — server.py
Run: uvicorn server:app --host 0.0.0.0 --port 8000
"""
import os, re, json, random, asyncio, logging, aiosqlite
from typing import List, Dict, Optional
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)

DB_PATH        = "formboost.db"
GROK_API_KEY   = "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"
GEMINI_API_KEY = "AIzaSyABjxop020nlvRc9sgZln8OVJWzCDSUiSo"
GROK_URL       = "https://api.x.ai/v1/chat/completions"
GEMINI_URL     = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

app = FastAPI(title="FormBoost API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─── DB HELPERS ───────────────────────────────────────────────────────────────
async def get_balance(uid: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute("SELECT balance FROM users WHERE user_id=?", (uid,))).fetchone()
        return row["balance"] if row else 0

async def deduct(uid: int, amount: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await (await db.execute("SELECT balance FROM users WHERE user_id=?", (uid,))).fetchone()
        if not row or row["balance"] < amount:
            return False
        await db.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (amount, uid))
        await db.commit()
        return True

async def refund(uid: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (amount, uid))
        await db.commit()

async def save_run(uid, url, requested, sent, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO runs (user_id,form_url,votes_requested,votes_sent,status) VALUES (?,?,?,?,?)",
            (uid, url, requested, sent, status)
        )
        await db.commit()

async def get_runs(uid: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await (await db.execute(
            "SELECT * FROM runs WHERE user_id=? ORDER BY created_at DESC LIMIT 20", (uid,)
        )).fetchall()
        return [dict(r) for r in rows]

async def create_kaspi_tx(uid, votes, tenge) -> int:
    pkg_map = {10: "p10", 50: "p50", 100: "p100", 500: "p500"}
    pkg = pkg_map.get(votes, "p10")
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO transactions (user_id,type,package,votes,tenge,stars,status) VALUES (?,?,?,?,?,?,?)",
            (uid, "kaspi", pkg, votes, tenge, 0, "pending")
        )
        await db.commit()
        return cur.lastrowid

# ─── AI GENERATION ────────────────────────────────────────────────────────────
async def generate_with_grok(question: str, count: int) -> List[str]:
    prompt = (
        f"Сгенерируй {count} разных реалистичных коротких ответов (1–2 предложения) студента "
        f"на вопрос анкеты: \"{question}\"\n"
        "Каждый ответ на новой строке. Без нумерации, без кавычек, без пояснений. "
        "Ответы разнообразные, живые, естественные. На том же языке что вопрос."
    )
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(GROK_URL,
            headers={"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"},
            json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 1500, "temperature": 0.92}
        )
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    while len(lines) < count:
        lines += lines[:count - len(lines)]
    return lines[:count]

async def generate_with_gemini(question: str, count: int) -> List[str]:
    prompt = (
        f"Сгенерируй {count} разных реалистичных коротких ответов (1–2 предложения) студента "
        f"на вопрос анкеты: \"{question}\"\n"
        "Каждый ответ на новой строке. Без нумерации, без кавычек, без пояснений. "
        "Ответы разнообразные, живые, естественные. На том же языке что вопрос."
    )
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.92, "maxOutputTokens": 1500}}
        )
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    while len(lines) < count:
        lines += lines[:count - len(lines)]
    return lines[:count]

async def generate_answers(question: str, count: int) -> List[str]:
    """Try Grok first, fall back to Gemini"""
    try:
        return await generate_with_grok(question, count)
    except Exception as e:
        logger.warning(f"Grok failed ({e}), trying Gemini...")
        try:
            return await generate_with_gemini(question, count)
        except Exception as e2:
            logger.error(f"Gemini also failed: {e2}")
            # Last resort: return placeholder
            return [f"Ответ на вопрос {i+1}" for i in range(count)]

# ─── FORM ANALYSIS ────────────────────────────────────────────────────────────
async def analyze_form(url: str) -> dict:
    clean = re.sub(r"\?.*", "", url).replace("/formResponse", "/viewform")
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
        r = await c.get(clean, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        r.raise_for_status()

    m = re.search(r"FB_PUBLIC_LOAD_DATA_ = (.*?);", r.text, re.DOTALL)
    if not m:
        raise ValueError("Форма не найдена. Убедись что форма публичная.")

    data = json.loads(m.group(1))
    fbzx = data[1][10]

    m1 = re.search(r"/d/e/([^/?#]+)", url)
    m2 = re.search(r"/forms/d/([^/?#]+)", url)
    if m1:
        post_url = f"https://docs.google.com/forms/d/e/{m1.group(1)}/formResponse"
    elif m2:
        post_url = f"https://docs.google.com/forms/d/{m2.group(1)}/formResponse"
    else:
        raise ValueError("Не удалось распознать ссылку Google Form")

    questions = []
    for q in data[1][1]:
        try:
            entry_id = f"entry.{q[4][0][0]}"
            q_type   = q[3]  # 0/1=текст, 2=radio, 4=checkbox, 5=dropdown
            options  = []
            if len(q[4][0]) > 1 and q[4][0][1]:
                options = [o[0] for o in q[4][0][1] if o and o[0]]
            is_open = q_type in (0, 1) or not options
            questions.append({
                "text":       q[1],
                "entry_id":   entry_id,
                "type":       q_type,
                "options":    options,
                "is_open":    is_open,
                "target_idx": 0,
                "weight":     70,
            })
        except Exception:
            continue

    return {
        "fbzx":       fbzx,
        "post_url":   post_url,
        "questions":  questions,
        "open_count": sum(1 for q in questions if q["is_open"]),
    }

# ─── FORM SUBMISSION ──────────────────────────────────────────────────────────
# Логика портирована 1-в-1 из FormBoost.py (run_process)
# Отличие: открытые вопросы → ИИ-генерация вместо ручного custom_answers_list
async def submit_forms(post_url: str, fbzx: str, questions: List[Dict],
                       count: int, ai_cache: Dict[str, List[str]]) -> int:

    # Строим weights_map — точно как в FormBoost.py
    # target — выбранный вариант, prob — вероятность из слайдера (0–100 → 0.0–1.0)
    weights_map = {}
    for q in questions:
        if q.get("options") and not q.get("is_open"):
            opts   = q["options"]
            # target_idx — индекс выбранного варианта (из Mini App)
            target = opts[q.get("target_idx", 0)] if opts else None
            prob   = q.get("weight", 70) / 100.0
            if len(opts) > 1:
                rem = (1.0 - prob) / (len(opts) - 1)
                w   = [prob if o == target else rem for o in opts]
            else:
                w = [1.0]
            weights_map[q["entry_id"]] = {"opts": opts, "w": w}

    success = 0
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as c:
        for i in range(count):
            # payload — точно как в FormBoost.py
            payload = {"fvv": "1", "pageHistory": "0", "fbzx": fbzx}

            for q in questions:
                eid = q["entry_id"]

                if eid in weights_map:
                    # Вопрос с вариантами — random.choices с весами (из FormBoost.py)
                    wm = weights_map[eid]
                    payload[eid] = random.choices(wm["opts"], weights=wm["w"])[0]

                elif q.get("options"):
                    # Варианты есть, но веса не заданы — просто random.choice
                    payload[eid] = random.choice(q["options"])

                else:
                    # Открытый вопрос — берём из пула ИИ-ответов (цикличный пул)
                    # В оригинале: random.choice(custom_answers_list)
                    # Здесь: пул сгенерирован заранее через Grok/Gemini
                    pool = ai_cache.get(eid)
                    if pool:
                        payload[eid] = pool[i % len(pool)]
                    else:
                        payload[eid] = "—"

            try:
                resp = await c.post(post_url, data=payload)
                # В FormBoost.py нет проверки статуса — просто отправляет
                # Добавляем проверку 200/302 для счётчика
                if resp.status_code in (200, 302):
                    success += 1
                    logger.info(f"Sent #{i+1}/{count} → {resp.status_code}")
                else:
                    logger.warning(f"Sent #{i+1} → unexpected {resp.status_code}")
            except Exception as e:
                logger.warning(f"Submit #{i+1} error: {e}")

            # Задержка как в FormBoost.py: random.uniform(2, 5)
            await asyncio.sleep(random.uniform(2.0, 5.0))

    return success

# ─── MODELS ───────────────────────────────────────────────────────────────────
class AnalyzeReq(BaseModel):
    url: str
    uid: int

class RunReq(BaseModel):
    uid:       int
    form_url:  str
    post_url:  str
    fbzx:      str
    questions: List[Dict]
    count:     int

class GenReq(BaseModel):
    uid:      int
    question: str
    count:    int

class KaspiInitReq(BaseModel):
    uid:   int
    votes: int
    tenge: int

# ─── ROUTES ───────────────────────────────────────────────────────────────────
@app.get("/api/balance/{uid}")
async def api_balance(uid: int):
    return {"balance": await get_balance(uid)}

@app.get("/api/history/{uid}")
async def api_history(uid: int):
    return {"runs": await get_runs(uid)}

@app.post("/api/analyze")
async def api_analyze(req: AnalyzeReq):
    try:
        result = await analyze_form(req.url)
        return {"ok": True, **result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"analyze: {e}")
        raise HTTPException(500, f"Ошибка анализа формы: {e}")

@app.post("/api/generate")
async def api_generate(req: GenReq):
    bal = await get_balance(req.uid)
    if bal <= 0:
        raise HTTPException(402, "Нет голосов на балансе")
    answers = await generate_answers(req.question, req.count)
    return {"ok": True, "answers": answers}

@app.post("/api/run")
async def api_run(req: RunReq):
    bal = await get_balance(req.uid)
    if bal < req.count:
        raise HTTPException(402, f"Недостаточно голосов. Баланс: {bal}, нужно: {req.count}")
    if not await deduct(req.uid, req.count):
        raise HTTPException(402, "Ошибка списания баланса")

    # Генерируем ответы для открытых вопросов
    ai_cache: Dict[str, List[str]] = {}
    for q in req.questions:
        if q.get("is_open"):
            ai_cache[q["entry_id"]] = await generate_answers(q["text"], min(req.count, 50))

    try:
        sent = await submit_forms(req.post_url, req.fbzx, req.questions, req.count, ai_cache)
        await save_run(req.uid, req.form_url, req.count, sent, "done")
        return {"ok": True, "sent": sent, "total": req.count,
                "balance": await get_balance(req.uid)}
    except Exception as e:
        await refund(req.uid, req.count)
        raise HTTPException(500, str(e))

@app.post("/api/kaspi-init")
async def api_kaspi_init(req: KaspiInitReq):
    tx_id = await create_kaspi_tx(req.uid, req.votes, req.tenge)
    return {"tx_id": tx_id}

# Фронтенд Mini App
app.mount("/", StaticFiles(directory="miniapp", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
