/* reminders.js — the daily reminder settings (issue #31), kept in Supabase's
   `reminders` table, which tools/send-reminders.js reads every hour.
   Loaded after auth.js on the Settings page.

     await RafiqReminders.load()        this account's row, or null
     await RafiqReminders.save(patch)   upsert some columns (the time zone is always refreshed)
     RafiqReminders.pushState()         'ok' | 'install' (iPhone: add to Home Screen first) | 'no'
     await RafiqReminders.subscribe()   ask for permission, return the push subscription (or throw)
     await RafiqReminders.unsubscribe() drop this device's subscription

   One device gets the notifications: turning them on elsewhere moves them there. */
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
  }

  const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const ios = () => /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  function pushState(){
    const can = 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
    if(ios() && !standalone()) return 'install';     // Safari only offers push to a Home Screen app
    return can ? 'ok' : 'no';
  }
  const bytes = b64 => { const s = atob((b64 + '='.repeat((4 - b64.length % 4) % 4)).replace(/-/g, '+').replace(/_/g, '/'));
    return Uint8Array.from(s, c => c.charCodeAt(0)); };

  async function subscribe(){
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
    try{ const reg = await navigator.serviceWorker.ready; const s = await reg.pushManager.getSubscription(); if(s) await s.unsubscribe(); }catch(_){}
  }

  window.RafiqReminders = { load, save, pushState, subscribe, unsubscribe };
})();
