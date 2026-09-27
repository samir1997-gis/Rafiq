/* auth.js — shared login/logout/guard for every page.
   Loaded on each page via:
     <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
     <script src="auth.js?v=1"></script>
   Safe public values only. The publishable key is meant to be public. */

const SUPABASE_URL = 'https://gaajfahtrbdybjuunfhe.supabase.co';
const SUPABASE_KEY = 'sb_publishable_nFs-UJyKpTsCtHRn4WZJGg_c14-cM4e';

// create one shared client the whole page can use
const sb = (window.supabase && window.supabase.createClient)
  ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY)
  : null;

/* Log the user out: end the Supabase session, clear the cached name,
   then send them to the login page. Works from any page. */
/* ---------- Idle auto-logout (shared-computer safety) ----------
   If the app hasn't been used for this long, the next time a page loads
   the person is logged out. Protects a session left open on a shared PC.
   Note: this can only act when a page is opened/reloaded — it can't log
   someone out while the tab is closed. */
const IDLE_LIMIT_MS = 24 * 60 * 60 * 1000;   // 24 hours
const LAST_ACTIVE_KEY = 'bay_last_active';

function markActive(){
  try { localStorage.setItem(LAST_ACTIVE_KEY, String(Date.now())); } catch(_) {}
}
// has the idle limit been exceeded since last activity?
/* The app added to the home screen is on the person's own phone, so it keeps
   them signed in (iPhone often won't offer saved passwords there). */
function installedApp(){
  try { return matchMedia('(display-mode: standalone)').matches || navigator.standalone === true; } catch(_) { return false; }
}
function idleExpired(){
  if (installedApp()) return false;
  try {
    const last = parseInt(localStorage.getItem(LAST_ACTIVE_KEY), 10);
    if (!last) return false;                  // never recorded -> don't lock out
    return (Date.now() - last) > IDLE_LIMIT_MS;
  } catch(_) { return false; }
}

async function logout(){
  try { if (sb) await sb.auth.signOut(); } catch(_) {}
  try { localStorage.removeItem('bay_name'); } catch(_) {}
  try { localStorage.removeItem(LAST_ACTIVE_KEY); } catch(_) {}
  window.location.href = 'index.html';
}

// Sign out of EVERY device (Supabase global sign-out) — for the "left it on a
// shared computer" case. Ends all sessions for this account, everywhere.
async function logoutEverywhere(){
  try { if (sb) await sb.auth.signOut({ scope: 'global' }); } catch(_) {}
  try { localStorage.removeItem('bay_name'); } catch(_) {}
  try { localStorage.removeItem(LAST_ACTIVE_KEY); } catch(_) {}
  window.location.href = 'index.html';
}

/* Sessions from sign-ins before this moment are ended on the next page load, so
   everyone signs in again (and meets the new password rule and questions).
   Set on 26 Sep 2026 for the beta reset; move it forward to sign everyone out again. */
const SIGN_IN_AGAIN_BEFORE = '2026-09-26T18:13:00Z';
function staleSession(session){
  const at = session && session.user && session.user.last_sign_in_at;
  return !!(at && new Date(at) < new Date(SIGN_IN_AGAIN_BEFORE));
}

/* Guard a page: if nobody is logged in, bounce to the login page.
   Also enforces the idle timeout. Call near the top of a protected page. */
async function requireLogin(){
  if (!sb) return null;                       // library failed to load; don't lock people out
  try {
    const { data } = await sb.auth.getSession();
    if (!data || !data.session) {
      window.location.href = 'login.html';
      return null;
    }
    if (staleSession(data.session)) {
      try { await sb.auth.signOut({ scope: 'local' }); } catch(_) {}
      window.location.href = 'login.html?again=1';
      return null;
    }
    // logged in — but has it been idle too long? (shared-computer safety)
    if (idleExpired()) {
      await logout();
      return null;
    }
    markActive();                             // fresh activity: reset the idle clock
    return data.session;
  } catch(_) {
    return null;                              // on error, fail open rather than trap the user
  }
}

// keep the "last active" time fresh while the person is actually using the app
['click','keydown','touchstart'].forEach(evt=>{
  document.addEventListener(evt, ()=>{ if (sb) markActive(); }, { passive:true });
});

// let any "Log out" link work just by adding onclick="logout()" OR class="logout-link"
document.addEventListener('click', function(e){
  const t = e.target.closest('.logout-link, [data-logout]');
  if (t){ e.preventDefault(); logout(); }
});

/* ---------- Cloud vocab progress (Stage 2) ----------
   These let a page store per-user progress in Supabase instead of the browser.
   Shapes:
     progress row  = { word_id, box, due_date }   (due_date is 'YYYY-MM-DD' or null)
     in-app record = { box, due }                 (due is a day-number or null)
   We translate between them here so the vocab page barely changes. */

// day-number <-> ISO date helpers (matches vocab.html's `today()` = days since epoch)
function _dayToISO(dayNum){
  if (dayNum === null || dayNum === undefined) return null;
  return new Date(dayNum * 86400000).toISOString().slice(0,10);
}
function _isoToDay(iso){
  if (!iso) return null;
  return Math.floor(new Date(iso + 'T00:00:00Z').getTime() / 86400000);
}

// current user's id, or null if not logged in
async function currentUserId(){
  if (!sb) return null;
  try { const { data } = await sb.auth.getUser(); return data && data.user ? data.user.id : null; }
  catch(_) { return null; }
}

// Load this user's whole progress map: { [word_id]: {box, due} }
async function cloudLoadProgress(){
  if (!sb) return null;
  const uid = await currentUserId(); if (!uid) return null;
  const { data, error } = await sb.from('progress').select('word_id, box, due_date').eq('user_id', uid);
  if (error) { console.warn('progress load failed', error.message); return null; }
  const map = {};
  (data || []).forEach(r => { map[r.word_id] = { box: r.box, due: _isoToDay(r.due_date) }; });
  return map;
}

// Save ONE word's progress immediately (called after each answer)
async function cloudSaveWord(wordId, rec){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const row = { user_id: uid, word_id: Number(wordId), box: rec.box,
                due_date: _dayToISO(rec.due), last_seen: new Date().toISOString() };
  const { error } = await sb.from('progress').upsert(row, { onConflict: 'user_id,word_id' });
  if (error) console.warn('progress save failed', error.message);
}

// Save many words at once (used by the one-time migration)
async function cloudSaveMany(progressMap){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const rows = Object.keys(progressMap).map(id => ({
    user_id: uid, word_id: Number(id), box: progressMap[id].box,
    due_date: _dayToISO(progressMap[id].due), last_seen: new Date().toISOString()
  }));
  if (!rows.length) return;
  const { error } = await sb.from('progress').upsert(rows, { onConflict: 'user_id,word_id' });
  if (error) console.warn('bulk progress save failed', error.message);
}

// Settings: new-words-per-day
async function cloudLoadNewPerDay(){
  if (!sb) return null;
  const uid = await currentUserId(); if (!uid) return null;
  const { data, error } = await sb.from('settings').select('new_per_day').eq('user_id', uid).maybeSingle();
  if (error) { console.warn('settings load failed', error.message); return null; }
  return data ? data.new_per_day : null;
}
async function cloudSaveNewPerDay(n){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const { error } = await sb.from('settings')
    .upsert({ user_id: uid, new_per_day: n, updated_at: new Date().toISOString() }, { onConflict: 'user_id' });
  if (error) console.warn('settings save failed', error.message);
}

// Daily status: whether test/practise were finished today, and today's test score.
async function cloudLoadDaily(){
  if (!sb) return null;
  const uid = await currentUserId(); if (!uid) return null;
  const { data, error } = await sb.from('settings')
    .select('test_done_date, practise_done_date, test_score_correct, test_score_total, study_days, study_last')
    .eq('user_id', uid).maybeSingle();
  if (error) { console.warn('daily load failed', error.message); return null; }
  return data || {};
}
async function cloudSaveStudyDays(count, dateISO){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const { error } = await sb.from('settings').upsert(
    { user_id: uid, study_days: count, study_last: dateISO, updated_at: new Date().toISOString() },
    { onConflict: 'user_id' });
  if (error) console.warn('study days save failed', error.message);
}

// --- Profile (onboarding details: level, study method, duration) ---
async function cloudLoadProfile(){
  if (!sb) return null;
  const uid = await currentUserId(); if (!uid) return null;
  const { data, error } = await sb.from('profiles')
    .select('level, study_method, duration, onboarded, age_range, first_language, second_language, reason, ethnicity')
    .eq('user_id', uid).maybeSingle();
  if (error) { console.warn('profile load failed', error.message); return null; }
  return data;   // null if no row yet (i.e. not onboarded)
}
async function cloudSaveProfile(p){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  // Every field here is optional — undefined just leaves the column untouched
  // on this upsert rather than overwriting it with null, so partial saves
  // (onboarding "Skip", or editing one field in Settings) can't wipe others.
  const row = { user_id: uid, onboarded: true, updated_at: new Date().toISOString() };
  ['level','study_method','duration','age_range','first_language','second_language','reason','ethnicity']
    .forEach(k => { if (p[k] !== undefined) row[k] = p[k]; });
  const { error } = await sb.from('profiles').upsert(row, { onConflict: 'user_id' });
  if (error) console.warn('profile save failed', error.message);
}
async function cloudMarkTestDone(dateISO, correct, total){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const { error } = await sb.from('settings').upsert(
    { user_id: uid, test_done_date: dateISO, test_score_correct: correct, test_score_total: total,
      updated_at: new Date().toISOString() }, { onConflict: 'user_id' });
  if (error) console.warn('mark test done failed', error.message);
}
async function cloudMarkPractiseDone(dateISO){
  if (!sb) return;
  const uid = await currentUserId(); if (!uid) return;
  const { error } = await sb.from('settings').upsert(
    { user_id: uid, practise_done_date: dateISO, updated_at: new Date().toISOString() },
    { onConflict: 'user_id' });
  if (error) console.warn('mark practise done failed', error.message);
}
