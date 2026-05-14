<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>FormBoost</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
:root{
  --bg:#07050f;
  --s1:#0e0b1e;
  --s2:#160f2e;
  --border:#241a42;
  --border2:#3d2a70;
  --acc:#7c3aed;
  --acc2:#a855f7;
  --acc3:#c084fc;
  --glow:rgba(124,58,237,.3);
  --txt:#ede9ff;
  --muted:#7c6fa0;
  --green:#22c55e;
  --red:#ef4444;
  --gold:#f59e0b;
  --r:12px;--r2:8px;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%;background:var(--bg);color:var(--txt);font-family:'Inter',sans-serif;overflow-x:hidden}

/* noise */
body::after{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='.04'/%3E%3C/svg%3E");pointer-events:none;z-index:0;opacity:.5}

/* glow blobs */
body::before{content:'';position:fixed;inset:0;background:
  radial-gradient(ellipse 70% 40% at 15% 0%,rgba(124,58,237,.18) 0%,transparent 60%),
  radial-gradient(ellipse 50% 30% at 90% 100%,rgba(168,85,247,.1) 0%,transparent 55%);
  pointer-events:none;z-index:0}

.app{position:relative;z-index:1;min-height:100vh;padding-bottom:80px}

/* ── HEADER ─────────────────── */
.hdr{display:flex;align-items:center;justify-content:space-between;padding:18px 16px 10px}
.logo{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;letter-spacing:-.5px;
  background:linear-gradient(135deg,#a78bfa,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.bal-pill{display:flex;align-items:center;gap:6px;padding:6px 14px;
  background:linear-gradient(135deg,rgba(124,58,237,.25),rgba(168,85,247,.1));
  border:1px solid var(--border2);border-radius:20px;cursor:pointer;transition:.15s}
.bal-pill:active{transform:scale(.96)}
.bal-pill b{color:#a78bfa;font-weight:700}
.bal-pill span{color:var(--muted);font-size:12px}

/* ── PAGES ──────────────────── */
.page{display:none;padding:0 16px;animation:fadeIn .22s ease}
.page.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* ── BOTTOM NAV ─────────────── */
.nav{position:fixed;bottom:0;left:0;right:0;
  background:rgba(7,5,15,.9);backdrop-filter:blur(20px);
  border-top:1px solid var(--border);
  display:flex;z-index:100;padding-bottom:env(safe-area-inset-bottom)}
.nav-btn{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;
  padding:10px 4px;border:none;background:none;color:var(--muted);
  font-family:'Inter',sans-serif;font-size:10px;font-weight:500;cursor:pointer;transition:color .15s}
.nav-btn i{font-size:20px;line-height:1}
.nav-btn.on{color:#a78bfa}

/* ── SECTION LABEL ──────────── */
.lbl{font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:1.8px;
  text-transform:uppercase;color:var(--muted);margin-bottom:8px}

/* ── CARD ───────────────────── */
.card{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);
  padding:14px 16px;margin-bottom:10px}

/* ── URL INPUT ──────────────── */
.url-wrap{display:flex;align-items:center;background:var(--s1);border:1px solid var(--border);
  border-radius:var(--r);overflow:hidden;transition:border-color .2s;margin-bottom:8px}
.url-wrap:focus-within{border-color:var(--border2)}
.url-in{flex:1;background:none;border:none;outline:none;color:var(--txt);
  font-family:'Inter',sans-serif;font-size:14px;padding:13px 14px}
.url-in::placeholder{color:var(--muted)}
.paste-btn{background:none;border:none;border-left:1px solid var(--border);
  padding:0 13px;height:46px;color:var(--acc2);font-size:18px;cursor:pointer;transition:.15s}
.paste-btn:active{background:rgba(124,58,237,.15)}

.btn-main{width:100%;padding:14px;background:linear-gradient(135deg,var(--acc),#6d28d9);
  border:none;border-radius:var(--r);color:#fff;font-family:'Syne',sans-serif;
  font-weight:700;font-size:15px;cursor:pointer;transition:all .2s;
  box-shadow:0 4px 20px rgba(124,58,237,.35)}
.btn-main:active{transform:scale(.98);box-shadow:0 2px 10px rgba(124,58,237,.2)}
.btn-main:disabled{opacity:.45;cursor:default;box-shadow:none;transform:none}

/* ── QUESTION CARD ──────────── */
.q-card{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);
  padding:14px;margin-bottom:8px;animation:slideUp .3s ease both}
@keyframes slideUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.q-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:10px}
.q-text{font-size:13px;font-weight:500;line-height:1.45;flex:1}
.q-tag{font-size:9px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;
  padding:3px 8px;border-radius:20px;white-space:nowrap;flex-shrink:0}
.q-tag.open{background:rgba(168,85,247,.18);color:#c084fc;border:1px solid rgba(168,85,247,.3)}
.q-tag.sel{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.25)}

/* options */
.opt{display:flex;align-items:center;gap:8px;padding:8px 10px;
  background:rgba(255,255,255,.03);border-radius:var(--r2);margin-bottom:5px;
  cursor:pointer;transition:.15s;border:1px solid transparent}
.opt:last-child{margin-bottom:0}
.opt.on{background:rgba(124,58,237,.2);border-color:rgba(124,58,237,.4)}
.opt-dot{width:14px;height:14px;border-radius:50%;border:1.5px solid var(--border2);
  flex-shrink:0;transition:.15s;display:flex;align-items:center;justify-content:center}
.opt.on .opt-dot{background:var(--acc);border-color:var(--acc);box-shadow:0 0 6px var(--glow)}
.opt.on .opt-dot::after{content:'';width:5px;height:5px;background:#fff;border-radius:50%}
.opt-lbl{font-size:13px;flex:1}

/* slider */
.sl-row{display:flex;align-items:center;gap:10px;margin-top:10px}
.sl-lbl{font-size:11px;color:var(--muted);min-width:70px}
.sl-val{font-size:13px;font-weight:700;color:#a78bfa;min-width:34px;text-align:right}
input[type=range]{flex:1;-webkit-appearance:none;height:4px;background:var(--border);border-radius:2px;outline:none}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:17px;height:17px;
  background:linear-gradient(135deg,#a78bfa,var(--acc));border-radius:50%;cursor:pointer;
  box-shadow:0 0 7px rgba(124,58,237,.5)}

/* ai notice */
.ai-box{display:flex;align-items:center;gap:8px;padding:9px 12px;
  background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.22);
  border-radius:var(--r2);font-size:12px;color:#c084fc}

/* ── COUNT CARD ─────────────── */
.presets{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px}
.prs{padding:6px 13px;background:rgba(255,255,255,.05);border:1px solid var(--border);
  border-radius:20px;color:var(--muted);font-size:13px;cursor:pointer;transition:.15s}
.prs.on,.prs:active{background:rgba(124,58,237,.28);border-color:var(--acc);color:#a78bfa}
.cnt-in{width:100%;background:rgba(255,255,255,.05);border:1px solid var(--border);
  border-radius:var(--r2);padding:10px 14px;color:var(--txt);font-family:'Inter',sans-serif;
  font-size:17px;font-weight:700;outline:none;text-align:center;margin-bottom:6px}
.cnt-in:focus{border-color:var(--border2)}
.cost-note{font-size:11px;color:var(--muted);text-align:center}
.cost-note b{color:#a78bfa}

/* ── PROGRESS ───────────────── */
.prog-card{background:var(--s1);border:1px solid var(--border2);border-radius:var(--r);
  padding:20px 16px;text-align:center}
.prog-big{font-family:'Syne',sans-serif;font-size:52px;font-weight:800;line-height:1;
  background:linear-gradient(135deg,#a78bfa,var(--acc));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px}
.prog-sub{font-size:13px;color:var(--muted);margin-bottom:14px}
.bar-wrap{height:5px;background:var(--border);border-radius:3px;overflow:hidden;margin-bottom:12px}
.bar{height:100%;background:linear-gradient(90deg,var(--acc),var(--acc2));border-radius:3px;
  width:0%;transition:width .35s ease}
.log-box{font-size:11px;color:var(--muted);max-height:64px;overflow:hidden;text-align:left}
.log-ok{color:var(--green)}.log-err{color:var(--red)}

/* ── SHOP PAGE ──────────────── */
.shop-banner{background:linear-gradient(135deg,rgba(124,58,237,.28),rgba(168,85,247,.12));
  border:1px solid var(--border2);border-radius:var(--r);padding:18px;text-align:center;margin-bottom:14px}
.shop-banner h2{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;margin-bottom:3px}
.shop-banner p{font-size:12px;color:var(--muted)}

.pkg{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);
  padding:14px 16px;display:flex;align-items:center;justify-content:space-between;
  cursor:pointer;transition:all .2s;margin-bottom:9px;position:relative;overflow:hidden}
.pkg.hot{border-color:var(--border2);background:linear-gradient(135deg,rgba(124,58,237,.1),var(--s1))}
.pkg:active{transform:scale(.98)}
.pkg-badge{position:absolute;top:9px;right:9px;background:linear-gradient(135deg,var(--acc),var(--acc2));
  color:#fff;font-size:9px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;
  padding:2px 8px;border-radius:20px}
.pkg-votes{font-family:'Syne',sans-serif;font-size:19px;font-weight:800;margin-bottom:2px}
.pkg-hint{font-size:11px;color:var(--muted)}
.pkg-price{text-align:right}
.pkg-tenge{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:#a78bfa}
.pkg-stars{font-size:11px;color:var(--muted);margin-top:2px}

/* ── MODAL ──────────────────── */
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:200;align-items:flex-end}
.overlay.open{display:flex}
.modal{width:100%;background:var(--s1);border-radius:18px 18px 0 0;border-top:1px solid var(--border);
  padding:16px 16px 32px;animation:slideModal .28s cubic-bezier(.32,.72,0,1)}
@keyframes slideModal{from{transform:translateY(100%)}to{transform:none}}
.modal-handle{width:34px;height:4px;background:var(--border);border-radius:2px;margin:0 auto 16px}
.modal h3{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;margin-bottom:4px}
.modal-sub{font-size:12px;color:var(--muted);margin-bottom:16px}
.pay-btn{display:flex;align-items:center;gap:12px;padding:13px 16px;
  background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:var(--r);
  cursor:pointer;margin-bottom:8px;transition:.15s;width:100%}
.pay-btn:active{background:rgba(124,58,237,.2);border-color:var(--acc)}
.pay-ic{font-size:22px}
.pay-info{flex:1;text-align:left}
.pay-name{font-size:14px;font-weight:500}
.pay-desc{font-size:11px;color:var(--muted)}
.pay-amt{font-size:14px;font-weight:700;color:#a78bfa}

/* ── KASPI STEPS ────────────── */
.kaspi-box{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);padding:16px;margin-bottom:10px}
.kstep{display:flex;gap:11px;margin-bottom:14px;align-items:flex-start}
.kstep:last-child{margin-bottom:0}
.knum{width:26px;height:26px;background:linear-gradient(135deg,var(--acc),var(--acc2));
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Syne',sans-serif;font-size:11px;font-weight:800;flex-shrink:0}
.ktxt{font-size:13px;line-height:1.5}
.kcode{display:inline-block;background:rgba(124,58,237,.2);border:1px solid rgba(124,58,237,.4);
  border-radius:6px;padding:2px 9px;font-family:monospace;font-size:13px;color:#a78bfa;
  cursor:pointer;transition:.15s;margin:3px 0}
.kcode:active{background:rgba(124,58,237,.4)}

/* ── HISTORY ────────────────── */
.hist-item{background:var(--s1);border:1px solid var(--border);border-radius:var(--r);
  padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between}
.hi-title{font-size:13px;font-weight:500;margin-bottom:3px}
.hi-date{font-size:11px;color:var(--muted)}
.hi-votes{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#a78bfa;text-align:right}
.hi-status{font-size:10px;color:var(--green);text-align:right;margin-top:2px}

/* ── TOAST ───────────────────── */
.toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%) translateY(16px);
  background:rgba(22,15,46,.95);border:1px solid var(--border2);
  color:var(--txt);padding:9px 18px;border-radius:20px;font-size:13px;
  z-index:400;opacity:0;transition:all .25s;white-space:nowrap;pointer-events:none}
.toast.ok{border-color:rgba(34,197,94,.5);color:#4ade80}
.toast.err{border-color:rgba(239,68,68,.5);color:#f87171}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* ── SPINNER ─────────────────── */
.spin{display:inline-block;width:16px;height:16px;border:2px solid rgba(167,139,250,.25);
  border-top-color:#a78bfa;border-radius:50%;animation:rot .65s linear infinite;vertical-align:middle}
@keyframes rot{to{transform:rotate(360deg)}}

.hidden{display:none!important}
.mt8{margin-top:8px}
</style>
</head>
<body>
<div class="app">

<!-- ══ PAGE: RUN ══════════════════════════════════ -->
<div class="page active" id="pg-run">
  <div class="hdr">
    <div class="logo">FormBoost</div>
    <div class="bal-pill" onclick="nav('shop')">
      💎 <b id="bal1">0</b><span>гол.</span>
    </div>
  </div>

  <!-- URL -->
  <div class="lbl">Ссылка на форму</div>
  <div class="url-wrap">
    <input class="url-in" id="url-in" type="url" placeholder="https://docs.google.com/forms/...">
    <button class="paste-btn" onclick="doPaste()">📋</button>
  </div>
  <button class="btn-main" id="btn-analyze" onclick="doAnalyze()">Анализировать форму</button>

  <!-- Questions -->
  <div id="sec-q" class="hidden" style="margin-top:16px">
    <div class="lbl">Вопросы <span id="q-cnt" style="color:var(--acc2)"></span></div>
    <div id="q-list"></div>
  </div>

  <!-- Count + Run -->
  <div id="sec-run" class="hidden" style="margin-top:4px">
    <div class="lbl" style="margin-top:8px">Количество голосов</div>
    <div class="card">
      <div class="presets" id="presets">
        <button class="prs" onclick="setN(10)">10</button>
        <button class="prs" onclick="setN(25)">25</button>
        <button class="prs" onclick="setN(50)">50</button>
        <button class="prs on" onclick="setN(100)">100</button>
        <button class="prs" onclick="setN(200)">200</button>
      </div>
      <input class="cnt-in" id="cnt-in" type="number" value="100" min="1" max="1000" oninput="updCost()">
      <div class="cost-note">Спишется: <b id="cost-out">100</b> голосов</div>
    </div>
    <button class="btn-main" id="btn-run" onclick="doRun()">⚡ Запустить</button>
  </div>

  <!-- Progress -->
  <div id="sec-prog" class="hidden" style="margin-top:12px">
    <div class="prog-card">
      <div class="prog-big" id="prog-n">0</div>
      <div class="prog-sub">отправлено</div>
      <div class="bar-wrap"><div class="bar" id="prog-bar"></div></div>
      <div class="log-box" id="log-box"></div>
    </div>
  </div>
</div>

<!-- ══ PAGE: SHOP ═════════════════════════════════ -->
<div class="page" id="pg-shop">
  <div class="hdr">
    <div class="logo">Купить голоса</div>
    <div class="bal-pill"><💎 <b id="bal2">0</b><span>гол.</span></div>
  </div>
  <div class="shop-banner">
    <h2>💎 Пополни баланс</h2>
    <p>10 голосов = 100 ₸ · без подписки</p>
  </div>
  <div id="pkg-list">
    <div class="pkg" onclick="openModal(10,100,17)">
      <div><div class="pkg-votes">10 голосов</div><div class="pkg-hint">стартовый пакет</div></div>
      <div class="pkg-price"><div class="pkg-tenge">100 ₸</div><div class="pkg-stars">или 17 ⭐</div></div>
    </div>
    <div class="pkg hot" onclick="openModal(50,450,75)">
      <div class="pkg-badge">Хит</div>
      <div><div class="pkg-votes">50 голосов</div><div class="pkg-hint">скидка 10%</div></div>
      <div class="pkg-price"><div class="pkg-tenge">450 ₸</div><div class="pkg-stars">или 75 ⭐</div></div>
    </div>
    <div class="pkg" onclick="openModal(100,800,133)">
      <div><div class="pkg-votes">100 голосов</div><div class="pkg-hint">скидка 20%</div></div>
      <div class="pkg-price"><div class="pkg-tenge">800 ₸</div><div class="pkg-stars">или 133 ⭐</div></div>
    </div>
    <div class="pkg" onclick="openModal(500,3500,583)">
      <div><div class="pkg-votes">500 голосов</div><div class="pkg-hint">максимальная выгода</div></div>
      <div class="pkg-price"><div class="pkg-tenge">3 500 ₸</div><div class="pkg-stars">или 583 ⭐</div></div>
    </div>
  </div>

  <!-- Kaspi instructions (shown after choosing kaspi) -->
  <div id="kaspi-steps" class="hidden" style="margin-top:4px">
    <div class="lbl" style="margin-top:8px">Инструкция по оплате Kaspi</div>
    <div class="kaspi-box">
      <div class="kstep">
        <div class="knum">1</div>
        <div class="ktxt">Переведи <b id="k-amt">—</b> на карту Kaspi:<br>
          <span class="kcode" onclick="copyText('4400430100000000','Карта скопирована')">4400 4301 XXXX XXXX</span>
          <br>Получатель: <b>Твоё Имя</b>
        </div>
      </div>
      <div class="kstep">
        <div class="knum">2</div>
        <div class="ktxt">В комментарии к переводу напиши:<br>
          <span class="kcode" id="k-code" onclick="copyCode()">FB-XXXXX</span>
        </div>
      </div>
      <div class="kstep">
        <div class="knum">3</div>
        <div class="ktxt">Отправь скриншот чека боту — голоса придут за 15 минут 🔔</div>
      </div>
    </div>
    <button class="btn-main" onclick="openBot()">📸 Открыть бота → отправить скрин</button>
  </div>
</div>

<!-- ══ PAGE: HISTORY ══════════════════════════════ -->
<div class="page" id="pg-hist">
  <div class="hdr">
    <div class="logo">История</div>
  </div>
  <div id="hist-list"><div style="color:var(--muted);text-align:center;padding:40px 0;font-size:14px">Загрузка…</div></div>
</div>

</div><!-- .app -->

<!-- ══ NAV ════════════════════════════════════════ -->
<nav class="nav">
  <button class="nav-btn on" id="nv-run" onclick="nav('run')"><i>🚀</i>Запуск</button>
  <button class="nav-btn"    id="nv-shop" onclick="nav('shop')"><i>💎</i>Купить</button>
  <button class="nav-btn"    id="nv-hist" onclick="nav('hist')"><i>📋</i>История</button>
</nav>

<!-- ══ PAYMENT MODAL ══════════════════════════════ -->
<div class="overlay" id="pay-overlay" onclick="maybeClose(event)">
  <div class="modal">
    <div class="modal-handle"></div>
    <h3>Способ оплаты</h3>
    <div class="modal-sub" id="modal-sub">50 голосов — 450 ₸</div>
    <div class="pay-methods">
      <button class="pay-btn" onclick="payStars()">
        <span class="pay-ic">⭐</span>
        <div class="pay-info"><div class="pay-name">Telegram Stars</div><div class="pay-desc">Мгновенно · без ожидания</div></div>
        <span class="pay-amt" id="m-stars">75 ⭐</span>
      </button>
      <button class="pay-btn" onclick="payKaspi()">
        <span class="pay-ic">💳</span>
        <div class="pay-info"><div class="pay-name">Kaspi</div><div class="pay-desc">Перевод на карту · ~15 мин</div></div>
        <span class="pay-amt" id="m-tenge">450 ₸</span>
      </button>
    </div>
  </div>
</div>

<!-- ══ TOAST ══════════════════════════════════════ -->
<div class="toast" id="toast"></div>

<script>
const tg = window.Telegram?.WebApp;
if(tg){ tg.ready(); tg.expand(); }

// Get UID from URL param or Telegram
const UID = (() => {
  const p = new URLSearchParams(location.search).get('uid');
  if(p) return parseInt(p);
  try{ return tg?.initDataUnsafe?.user?.id || 0; } catch{ return 0; }
})();

const API = ''; // same origin
let formData = null;   // {fbzx, post_url, questions}
let curPkg   = null;   // {votes, tenge, stars}

// ── INIT ──────────────────────────────────────────
async function init(){
  await loadBalance();
}

async function loadBalance(){
  try{
    const r = await fetch(`${API}/api/balance/${UID}`);
    const d = await r.json();
    document.getElementById('bal1').textContent = d.balance;
    document.getElementById('bal2').textContent = d.balance;
  } catch(e){ console.warn(e); }
}

// ── NAV ───────────────────────────────────────────
function nav(page){
  ['run','shop','hist'].forEach(p=>{
    document.getElementById(`pg-${p}`).classList.toggle('active', p===page);
    document.getElementById(`nv-${p}`).classList.toggle('on', p===page);
  });
  if(page==='hist') loadHistory();
  if(page==='shop'){
    document.getElementById('kaspi-steps').classList.add('hidden');
  }
}

// ── PASTE ─────────────────────────────────────────
async function doPaste(){
  try{
    const t = await navigator.clipboard.readText();
    document.getElementById('url-in').value = t;
    toast('Ссылка вставлена');
  } catch{ toast('Вставь вручную','err'); }
}

// ── ANALYZE ───────────────────────────────────────
async function doAnalyze(){
  const url = document.getElementById('url-in').value.trim();
  if(!url){ toast('Вставь ссылку','err'); return; }
  if(!url.includes('google.com/forms')){ toast('Нужна ссылка Google Forms','err'); return; }

  const btn = document.getElementById('btn-analyze');
  btn.disabled = true;
  btn.innerHTML = '<span class="spin"></span> Анализируем…';
  document.getElementById('sec-q').classList.add('hidden');
  document.getElementById('sec-run').classList.add('hidden');
  document.getElementById('sec-prog').classList.add('hidden');

  try{
    const r = await fetch(`${API}/api/analyze`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({url, uid: UID})
    });
    const d = await r.json();
    if(!r.ok) throw new Error(d.detail || 'Ошибка');
    formData = d;
    renderQuestions(d.questions);
    document.getElementById('sec-q').classList.remove('hidden');
    document.getElementById('sec-run').classList.remove('hidden');
    const msg = d.open_count > 0
      ? `✨ ${d.questions.length} вопросов, ${d.open_count} открытых — ИИ сгенерирует ответы`
      : `✅ ${d.questions.length} вопросов`;
    toast(msg);
  } catch(e){ toast(e.message,'err'); }
  finally{
    btn.disabled = false;
    btn.innerHTML = 'Анализировать форму';
  }
}

function renderQuestions(qs){
  const list = document.getElementById('q-list');
  document.getElementById('q-cnt').textContent = `(${qs.length})`;
  list.innerHTML = '';
  qs.forEach((q,i)=>{
    const card = document.createElement('div');
    card.className = 'q-card';
    card.style.animationDelay = `${i*0.04}s`;

    if(q.is_open){
      card.innerHTML = `
        <div class="q-head">
          <div class="q-text">${esc(q.text)}</div>
          <div class="q-tag open">открытый</div>
        </div>
        <div class="ai-box">🤖 ИИ сам сгенерирует ответы для этого вопроса</div>`;
    } else {
      const opts = q.options.map((o,oi)=>`
        <div class="opt${oi===0?' on':''}" onclick="selOpt(${i},${oi},this)">
          <div class="opt-dot"></div>
          <div class="opt-lbl">${esc(o)}</div>
        </div>`).join('');
      card.innerHTML = `
        <div class="q-head">
          <div class="q-text">${esc(q.text)}</div>
          <div class="q-tag sel">выбор</div>
        </div>
        ${opts}
        <div class="sl-row">
          <span class="sl-lbl">Вероятность</span>
          <input type="range" min="1" max="99" value="70" id="sl-${i}"
            oninput="updWeight(${i},this.value)">
          <span class="sl-val" id="sv-${i}">70%</span>
        </div>`;
      q.target_idx = 0;
    }
    list.appendChild(card);
  });
}

function selOpt(qi, oi, el){
  el.closest('.q-card').querySelectorAll('.opt').forEach(o=>o.classList.remove('on'));
  el.classList.add('on');
  formData.questions[qi].target_idx = oi;
}
function updWeight(qi, v){
  document.getElementById(`sv-${qi}`).textContent = `${v}%`;
  formData.questions[qi].weight = parseInt(v);
}

// ── COUNT ─────────────────────────────────────────
function setN(n){
  document.getElementById('cnt-in').value = n;
  document.querySelectorAll('.prs').forEach(b=>
    b.classList.toggle('on', parseInt(b.textContent)===n));
  updCost();
}
function updCost(){
  const n = parseInt(document.getElementById('cnt-in').value)||0;
  document.getElementById('cost-out').textContent = n;
}

// ── RUN ───────────────────────────────────────────
async function doRun(){
  if(!formData){ toast('Сначала проанализируй форму','err'); return; }
  const count = parseInt(document.getElementById('cnt-in').value)||0;
  if(count<1){ toast('Укажи количество','err'); return; }
  const bal = parseInt(document.getElementById('bal1').textContent)||0;
  if(bal < count){
    toast(`Нужно ${count} гол., баланс ${bal}`, 'err');
    setTimeout(()=>nav('shop'), 1100);
    return;
  }

  const btn = document.getElementById('btn-run');
  btn.disabled = true;
  btn.innerHTML = '<span class="spin"></span> Запускаем…';
  document.getElementById('sec-prog').classList.remove('hidden');
  resetProgress();

  try{
    const r = await fetch(`${API}/api/run`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        uid: UID,
        form_url:  formData.post_url,
        post_url:  formData.post_url,
        fbzx:      formData.fbzx,
        questions: formData.questions,
        count
      })
    });
    const d = await r.json();
    if(!r.ok) throw new Error(d.detail || 'Ошибка');
    animProgress(d.sent, count);
    await loadBalance();
    toast(`✅ Готово! ${d.sent}/${count} отправлено`);
  } catch(e){
    toast(e.message,'err');
    document.getElementById('sec-prog').classList.add('hidden');
  } finally{
    btn.disabled = false;
    btn.innerHTML = '⚡ Запустить';
  }
}

function resetProgress(){
  document.getElementById('prog-n').textContent   = '0';
  document.getElementById('prog-bar').style.width = '0%';
  document.getElementById('log-box').innerHTML    = '';
}
function animProgress(final, total){
  const nEl  = document.getElementById('prog-n');
  const bEl  = document.getElementById('prog-bar');
  const lEl  = document.getElementById('log-box');
  let cur    = 0;
  const step = Math.max(1, Math.ceil(final/40));
  const iv   = setInterval(()=>{
    cur = Math.min(cur+step, final);
    nEl.textContent       = cur;
    bEl.style.width       = `${(cur/total*100).toFixed(1)}%`;
    if(cur % Math.max(1,Math.floor(final/8)) === 0 || cur===final){
      const ln = document.createElement('div');
      ln.className = 'log-ok';
      ln.textContent = `✓ Голос #${cur} отправлен`;
      lEl.appendChild(ln);
      lEl.scrollTop = lEl.scrollHeight;
    }
    if(cur >= final) clearInterval(iv);
  }, 50);
}

// ── SHOP / MODAL ──────────────────────────────────
function openModal(votes, tenge, stars){
  curPkg = {votes, tenge, stars};
  document.getElementById('modal-sub').textContent   = `${votes} голосов — ${tenge} ₸`;
  document.getElementById('m-stars').textContent     = `${stars} ⭐`;
  document.getElementById('m-tenge').textContent     = `${tenge} ₸`;
  document.getElementById('kaspi-steps').classList.add('hidden');
  document.getElementById('pay-overlay').classList.add('open');
}
function maybeClose(e){
  if(e.target === document.getElementById('pay-overlay'))
    document.getElementById('pay-overlay').classList.remove('open');
}

function payStars(){
  document.getElementById('pay-overlay').classList.remove('open');
  if(tg){
    // Send action to bot via sendData — bot will send invoice
    tg.sendData(JSON.stringify({action:'buy_stars', votes: curPkg.votes, stars: curPkg.stars}));
  } else {
    toast('Открой в Telegram для оплаты Stars','err');
  }
}

async function payKaspi(){
  document.getElementById('pay-overlay').classList.remove('open');
  try{
    const r = await fetch(`${API}/api/kaspi-init`,{
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({uid: UID, votes: curPkg.votes, tenge: curPkg.tenge})
    });
    const d = await r.json();
    document.getElementById('k-amt').textContent  = `${curPkg.tenge} ₸`;
    document.getElementById('k-code').textContent = `FB-${d.tx_id}`;
  } catch{
    document.getElementById('k-amt').textContent  = `${curPkg.tenge} ₸`;
    document.getElementById('k-code').textContent = `FB-${Date.now().toString().slice(-5)}`;
  }
  document.getElementById('kaspi-steps').classList.remove('hidden');
  document.getElementById('kaspi-steps').scrollIntoView({behavior:'smooth'});
}

function copyCode(){
  const code = document.getElementById('k-code').textContent;
  copyText(code, 'Код скопирован');
}
function copyText(text, msg){
  navigator.clipboard?.writeText(text).catch(()=>{});
  toast(msg || 'Скопировано');
}
function openBot(){
  if(tg) tg.close();
  else window.open('https://t.me/YOUR_BOT','_blank');
}

// ── HISTORY ───────────────────────────────────────
async function loadHistory(){
  const el = document.getElementById('hist-list');
  try{
    const r = await fetch(`${API}/api/history/${UID}`);
    const d = await r.json();
    if(!d.runs?.length){
      el.innerHTML = '<div style="color:var(--muted);text-align:center;padding:40px 0;font-size:14px">Запусков пока нет 🌱</div>';
      return;
    }
    el.innerHTML = d.runs.map(r=>`
      <div class="hist-item">
        <div>
          <div class="hi-title">${r.form_url.replace(/https?:\/\/[^/]+/,'').substring(0,30)}…</div>
          <div class="hi-date">${(r.created_at||'').substring(0,10)}</div>
        </div>
        <div>
          <div class="hi-votes">${r.votes_sent} гол.</div>
          <div class="hi-status">${r.status==='done'?'✓ Готово':'…'}</div>
        </div>
      </div>`).join('');
  } catch{
    el.innerHTML='<div style="color:var(--muted);text-align:center;padding:32px 0">Ошибка загрузки</div>';
  }
}

// ── TOAST ─────────────────────────────────────────
function toast(msg, type='ok'){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `toast ${type}`;
  void t.offsetWidth;
  t.classList.add('show');
  clearTimeout(t._t);
  t._t = setTimeout(()=>t.classList.remove('show'), 3000);
}

function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

init();
</script>
</body>
</html>
