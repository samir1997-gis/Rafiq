/* reminders.js — the daily reminder settings (issue #31), kept in Supabase's
   `reminders` table, which tools/send-reminders.js reads every hour.
   Loaded after auth.js on the Settings page.

     await RafiqReminders.load()        this account's row, or null
     await RafiqReminders.save(patch)   upsert some columns (the time zone is always refreshed)
     RafiqReminders.pushState()         'ok' | 'install' (iPhone: add to Home Screen first) | 'no'
     await RafiqReminders.subscribe()   ask for permission, return the push subscription (or throw)
     await RafiqReminders.unsubscribe() drop this device's subscription

   One device gets the notifications: turning them on elsewhere moves them there.

   In the iPhone and Android app (#35) the notifications are the phone's own, scheduled on the phone
   (Capacitor's LocalNotifications): the next 7 days at the reminder time, today's dropped once the daily
   goal is done (every time Home or Settings opens). The saved `push` is then {app:'local'}, which the
   hourly job leaves alone; email reminders work as on the website. */
(function(){
  const tz = () => { try{ return Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/London'; }catch(_){ return 'Europe/London'; } };

  async function load(){
    if(!sb) return null;
    const uid = await currentUserId(); if(!uid) return null;
    const { data, error } = await sb.from('reminders').select('enabled, hour, by_email, push, goal').eq('user_id', uid).maybeSingle();
    if(error){ console.warn('reminders load failed', error.message); return null; }
    return data;
  }
  async function save(patch){
    if(!sb) throw new Error('offline');
    const uid = await currentUserId(); if(!uid) throw new Error('signed out');
    const { error } = await sb.from('reminders')
      .upsert({ user_id: uid, ...patch, tz: tz(), updated_at: new Date().toISOString() }, { onConflict: 'user_id' });
    if(error) throw new Error(error.message);
    if(native && localHour() != null){              // the phone's own reminders follow a new time, or stop
      if(patch.enabled === false || patch.push === null) await unschedule().catch(() => {});
      else if(patch.hour != null) await schedule(patch.hour).catch(() => {});
    }
  }

  const native = !!(window.Capacitor && Capacitor.isNativePlatform && Capacitor.isNativePlatform());
  const LN = native ? (Capacitor.Plugins && Capacitor.Plugins.LocalNotifications) || Capacitor.registerPlugin('LocalNotifications') : null;
  const APP = { app: 'local' }, HOUR = 'rafiq_local_reminder';      // the hour this phone schedules for, or nothing
  async function schedule(hour){
    try{ localStorage.setItem(HOUR, String(hour)); }catch(_){}
    await unschedule(true);
    const P = window.RafiqPath, s = P ? P.streak() : 0, done = P ? P.doneToday() >= P.GOAL : false, list = [];
    for(let d = 0; d < 7; d++){
      const at = new Date(); at.setDate(at.getDate() + d); at.setHours(hour, 0, 0, 0);
      if(at <= new Date() || (d === 0 && done)) continue;
      list.push({ id: 1000 + d, title: d === 0 && s > 1 ? `Keep your ${s}-day streak going` : 'A few minutes of Arabic today',
                  body: d === 0 && s > 1 ? `You're on a ${s}-day streak. A few minutes today keeps it going.` : 'Your next step is ready. A few minutes is enough.',
                  schedule: { at } });
    }
    if(list.length) await LN.schedule({ notifications: list });
  }
  async function unschedule(keep){
    if(!keep) try{ localStorage.removeItem(HOUR); }catch(_){}
    const p = await LN.getPending(); if(p.notifications.length) await LN.cancel({ notifications: p.notifications.map(n => ({ id: n.id })) });
  }
  function localHour(){ try{ const h = localStorage.getItem(HOUR); return h == null ? null : +h; }catch(_){ return null; } }
  if(native) addEventListener('load', () => { const h = localHour(); if(h != null) schedule(h).catch(() => {}); });       // keep the week ahead filled, and today's gone once the goal is met

  const standalone = () => native || matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const ios = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  function pushState(){
    if(native) return 'ok';
    const can = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
    if(ios() && !standalone()) return 'install';     // Safari only offers push to a Home Screen app
    return can ? 'ok' : 'no';
  }
  const bytes = b64 => { const s = atob((b64 + '='.repeat((4 - b64.length % 4) % 4)).replace(/-/g, '+').replace(/_/g, '/'));
    return Uint8Array.from(s, c => c.charCodeAt(0)); };

  async function subscribe(hour){
    if(native){
      if((await LN.requestPermissions()).display !== 'granted') throw new Error('blocked');
      const row = hour == null ? await load() : null;
      await schedule(hour != null ? hour : row && row.hour != null ? row.hour : 19);
      return APP;
    }
    if(Notification.permission !== 'granted'){
      const p = await Notification.requestPermission();
      if(p !== 'granted') throw new Error('blocked');
    }
    const { data: key, error } = await sb.rpc('vapid_public_key');
    if(error || !key) throw new Error('not set up');
    const reg = await navigator.serviceWorker.ready;
    const old = await reg.pushManager.getSubscription();
    if(old) await old.unsubscribe().catch(() => {});
    const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: bytes(key) });
    return sub.toJSON();
  }
  async function unsubscribe(){
    if(native) return unschedule().catch(() => {});
    try{ const reg = await navigator.serviceWorker.ready; const s = await reg.pushManager.getSubscription(); if(s) await s.unsubscribe(); }catch(_){}
  }

  const goal = () => { try{ return parseInt(localStorage.getItem('rafiq_goal'), 10) || 2; }catch(_){ return 2; } };
  const TIMES = [[8,'8:00'],[13,'13:00'],[19,'19:00'],[21,'21:00']];

  /* Turn on the daily reminder at `hour`: by email always, and as a notification
     too when this device can (asks permission; call it from a tap). → {push:bool} */
  async function enable(hour){
    await save({ hour, goal: goal(), by_email: true, enabled: true });
    let push = false;
    if(pushState() === 'ok'){
      try{ const sub = await subscribe(hour); await save({ push: sub }); push = true; }catch(_){}
    }
    return { push };
  }

  /* Home, opened from the home-screen icon: once per account, ask for a time
     (or, if one was picked at sign-up, offer notifications for it). */
  const css = document.createElement('style');
  css.textContent = `
    .rem-card{background:var(--card);border:1px solid var(--verdigris);border-radius:12px;padding:16px;margin:14px 0 0}
    .rem-card .t{font-weight:700;font-size:16px}
    .rem-card p{margin:4px 0 12px;font-size:14px;line-height:1.5;color:var(--ink-soft)}
    .rem-card .times{display:flex;flex-wrap:wrap;gap:8px}
    .rem-card .times button,.rem-card .go{border:1px solid var(--rule);background:var(--paper);color:var(--ink);border-radius:999px;padding:9px 15px;min-height:40px;
      font:600 14px var(--la);cursor:pointer;touch-action:manipulation;transition:transform var(--press,.12s) var(--ease-out,ease-out)}
    .rem-card .times button:active,.rem-card .go:active{transform:scale(.95)}
    .rem-card .go{background:var(--verdigris);border-color:var(--verdigris);color:#fff}
    .rem-card .no{border:0;background:none;color:var(--ink-soft);font:13px var(--la);text-decoration:underline;cursor:pointer;padding:10px 4px}`;
  document.head.appendChild(css);
  const ASKED = 'rafiq_reminder_asked';
  async function prompt(el){
    if(!el || !standalone() || !sb) return;
    const uid = await currentUserId(); if(!uid) return;
    let asked = []; try{ asked = (localStorage.getItem(ASKED) || '').split(','); }catch(_){}
    if(asked.includes(uid)) return;
    const row = await load();
    const can = pushState() === 'ok';
    if(row && row.enabled && (row.push || !can)) return;          // nothing to offer
    const done = () => { try{ localStorage.setItem(ASKED, asked.filter(Boolean).concat(uid).slice(-5).join(',')); }catch(_){} };
    const thanks = (h, push) => { el.innerHTML = `<div class="rem-card" role="status"><div class="t">Reminder set for ${h}:00</div>
      <p>${push ? 'You’ll get a notification' : 'You’ll get an email'} on days you haven’t done your goal yet. Change it any time in Settings.</p></div>`;
      setTimeout(() => { el.innerHTML = ''; }, 6000); };
    if(row && row.enabled && row.hour != null){
      el.innerHTML = `<div class="rem-card"><div class="t">Get your reminder as a notification?</div>
        <p>You chose ${row.hour}:00. We can send it to this phone as well as by email.</p>
        <button type="button" class="go">Turn on notifications</button> <button type="button" class="no">Not now</button></div>`;
      el.querySelector('.go').onclick = async () => { done(); try{ const sub = await subscribe(row.hour); await save({ push: sub }); thanks(row.hour, true); }
        catch(_){ el.innerHTML = '<div class="rem-card"><p>Notifications are off for Rafiq. You can allow them in your phone’s Settings, then turn them on in Rafiq’s Settings.</p></div>'; } };
    } else {
      el.innerHTML = `<div class="rem-card"><div class="t">Want a daily reminder?</div>
        <p>Pick a time. We’ll only remind you on days you haven’t done your goal yet.</p>
        <div class="times">${TIMES.map(([h, t]) => `<button type="button" data-h="${h}">${t}</button>`).join('')}</div>
        <button type="button" class="no">Not now</button></div>`;
      el.querySelectorAll('[data-h]').forEach(b => b.onclick = async () => {
        done(); b.textContent = '…';
        try{ const r = await enable(+b.dataset.h); thanks(+b.dataset.h, r.push); }
        catch(_){ el.innerHTML = '<div class="rem-card"><p>Couldn’t save that. You can set a reminder in Settings.</p></div>'; }
      });
    }
    el.querySelector('.no').onclick = () => { done(); el.innerHTML = ''; };
  }

  window.RafiqReminders = { load, save, pushState, subscribe, unsubscribe, enable, prompt, TIMES };
})();
