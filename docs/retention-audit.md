# Retention audit: where new learners drop off

**Status:** diagnosis only. No app behaviour, drills, audio or data files were changed.
**Checked:** the `wip` branch (repo `samir1997-gis/Rafiq`, the copy this session can reach), 14 October 2026.
**Ask:** why about 70% of sign-ups never come back for a second session.

---

## Summary

- **The biggest suspected leak is the return visit.** A learner who doesn't install the app is signed out after 24 hours without a tap, and is then sent to the landing page with no message. Every "come back tomorrow" that lands more than a day after the last tap hits this. The database can't show how often it happens yet. The counter in section 5 will.
- **The first session is long.** From "Create account" to the first vocabulary words there are about 7 screens, around 20 taps and typing, a 5-question survey whose Continue button sits about 1,500 px down a phone screen, and 17 lesson steps before the first words step.
- **We track very little inside the app.** There is no event log. We have daily page visits, three sign-up button counts, and a funnel worked out from saved progress. We can't see where someone stops inside the survey or a lesson.
- **Real numbers from the last check:** 20 people signed up since 3 October and 3 of them have come back, about 15%. That's about 85% who haven't returned, a little above the roughly 70% you estimated. It's a small sample, so treat it as a direction, not a measurement.

---

## 1. Funnel map

Step by step, with the file and what the user does. Counts are taps, fields and screens.

| # | Step | Where | What the person does | Notes |
|---|---|---|---|---|
| 0 | Land on the site | `index.html` | Reads the hero. "Start your free week" at lines 294 and 383, a sticky bar at 420 (phones), "Sign in" at 282 | Good: the main button is visible without scrolling on a 390 px phone (checked) |
| 1 | Try four words | `index.html` 298–301, `taster.js` | Picks a meaning for each of four words, then taps "Start your free week" (`taster.js` 120) | About a minute. The answers are saved only if they sign up (`taster.js` 32–33) |
| 2 | Open the sign-up form | `login.html` 203, 232, 467 | Taps the button, or "Create an account" | Counted as tap `signup_page` (467) |
| 3 | Create the account | `login.html` 644–669 | Email, password (minimum length), optional name, taps Create | Counted as tap `create` (660). Email confirmation is off, so the session starts at once and goes to onboarding (669) |
| 4 | Survey | `onboarding.html` 86–137 | Five questions: reads Arabic (90), level (98), time a day (106), reminder (114), reason (125). Then Continue (136) or Skip (135) | One tap per question, plus Continue. Continue is 1,507 px down a 390 px screen (measured), so the person scrolls past all five |
| 5 | Placement (only some people) | `onboarding.html` 263–296 | Only if level is "basics" or "intermediate" and reads isn't "no". Types up to six Arabic sentences, checked by the judge | Typing Arabic on a phone before any lesson. "I don't know yet" skips it |
| 6 | Tour card (once per account) | `onboarding.html` 156–172, 227–241 | Watch the 79-second tour, or tap "Start my first lesson" (171) | An extra screen just before Home |
| 7 | Home | `dashboard.html` 216–230 | First card: "Start here" with a Continue button. Skip link for readers (230) | Works for a brand-new account (checked) |
| 8 | First lesson | `learn.html`, `path.js` 46–51 | Opens the reading starter: 7 letter groups, vowels, reading rules, listening test | 10 steps of about 5 minutes each. The first letter group shows example words with meanings, so the first real reward comes within about 5 minutes |
| 9 | First vocabulary words | `path.js` 52–53, 66–75 | Basics (6 lessons and a check), then unit 1's "Meet 10 new words" | Roughly 17 steps (about 1.5 hours) before the first vocabulary step. Word rows start only when a words step is finished (`learn.html` 394, 1206) |

**Time to first value:**
- Taps and fields from landing to the first letter: about 20, across 6–7 screens (landing, taster, sign-up, survey, tour, Home, lesson).
- Time to the first vocabulary step: about 1.5 hours of lessons.
- Biggest single delay before any learning: the survey, then placement for some people.

**Readers skip faster.** A person who answers "Yes, comfortably" to reading (survey step 4) skips the reading starter (`onboarding.html` 252, `path.js` `skipReading`). Beginners can't skip it.

---

## 2. Friction and bugs

Ordered by how much each could cost a return visit. Severity is my estimate from reading the code. I haven't tested most of these with real people.

### A. High: the 24-hour idle sign-out sends returners to the landing page

- `auth.js` 22: `IDLE_LIMIT_MS` is 24 hours.
- `auth.js` 113–115: only clicks, key presses and touches reset the clock. **Scrolling doesn't.** A lesson read by scrolling can run out the clock.
- `auth.js` 31–36: the installed app (home-screen icon) is exempt. Browser users aren't.
- `auth.js` 88–90: when the limit passes, `requireLogin()` calls `logout()`.
- `auth.js` 43–47: `logout()` sends the person to `index.html`, the landing page, with no explanation.

**Why it matters:** someone who studies at 9 am, taps for ten minutes, and comes back at 10 am the next day has been idle for 24 hours and is signed out. They land on the marketing page, see "Sign in" in the header, and can reasonably think the app has gone. The reason for the limit is shared computers, which is a fair concern, but the way it fails is what loses people.

### B. High: the survey and tour sit before the first lesson

- Five questions, and Continue is about 1,500 px down a phone screen (measured at 390 × 844).
- Only level, time and reading affect the first lesson (`onboarding.html` `save()` 209–221, `path.js`). The reminder and reason can wait.
- The reason answer is only shown back in Settings (`settings.html` 333). It doesn't change anything in the app.
- The tour adds an extra screen before Home.

### C. Medium: the taster doesn't carry into the first lesson

- The taster teaches four words (house, water, book, door, pen, plus prayer words). The first screen after sign-up is the letter chart.
- The overlap is real but late: the basics lesson 1 uses house, book and door (`basics-data.js` line 16). That's after seven steps.

### D. Medium: placement asks for typing before any lesson

- For "basics" and "intermediate" people (`onboarding.html` 263–296), six Arabic sentences must be typed and checked by the judge. The judge needs the network. If it is unavailable, the person starts at that unit (`onboarding.html` 288).
- "I don't know yet" is available, but it's an underlined link, not a button.

### E. Medium: the first vocabulary is far away for beginners

- Ten reading-starter steps and the basics come first (`path.js` 47–53). A beginner who answered "Not yet" to reading can't skip them.

### F. Low: study days count only lessons, sessions and scenes

- Study days come from `learn.html`, `session.html` and `path.js` 213 (`markDay`). `vocab.html` and `drills.html` never mark a study day.
- So someone who only drills vocabulary has no `s:` row. Their streak, and the funnel's "day after" and "7 days after" steps, don't count them. The "active on two days" step does count them, because it uses `updated_at`.
- This is a measurement gap, not a crash.

### G. Low: a skipped survey looks like a finished one

- `cloudSaveProfile` sets `onboarded: true` on every save (`auth.js` 229–238), and "Skip" calls it with no answers (`onboarding.html` 243–247). The data can't tell skipping from finishing. The SQL in section 4 separates them by whether level or time is set.

### H. Low: study method is never asked

- Your brief mentioned three questions including "study method". The code asks five, and "study method" isn't one of them. `auth.js` 223–224 reads a `study_method` column, but nothing writes it.

### I. Mobile layout: checked, no overflow

- At 390 px wide, the landing page, the sign-up form and the survey have no horizontal overflow and no JavaScript errors. Buttons are 46 px tall, which is comfortable for a thumb.
- The problem on phones is length, not width: see B.

### J. Start-up and offline

- The start-up test passed today (`tests/startup_speed.py`): Home, lesson, progress and practise show within 600 ms, online and offline.
- Sign-in still needs the network. A learner with no signal who has been signed out can't get back in.

### K. Empty or stale local storage: no defect found by reading

- `progress.js` 60–70 keeps each account's local copy separate (the owner check), so a different account on the same device doesn't see the last one's progress.
- `onboarding.html` 204 stores the "onboarded" flag per user id.
- `auth.js` 46–55 clears the activity clock on logout.
- Not tested on a real device.

### L. Info: sign-up counts can be inflated

- With email confirmation off, anyone can create an account with any email address (`login.html` 661). Test accounts or mistyped emails count as sign-ups. Section 4's Q3 shows whether confirmation timestamps are being set.

### M. Info: reminders are the only scheduled way back

- The reminder is opt-in in the survey (`onboarding.html` 114–122) and defaults to "No reminders".
- The reminder workflow ran successfully today (09:19 and 01:16 UTC). A returner-rate check on people who picked a time needs the `reminders` table's columns, which aren't in this repo. That's a follow-up query.

---

## 3. What's tracked

**Honest answer: there is no event tracking.** Nothing records an in-app step as it happens.

What does exist:

| What | Where | What it gives | Personal data? |
|---|---|---|---|
| Visits, referrers, countries, pages | Cloudflare Web Analytics (`privacy.html` 100, 114; `admin.html` 89) | Page views, no cookies | No personal data |
| Sign-up button taps, per day | `private.taps` (`supabase/sql/backend.sql` 252–266), called from `login.html` 316–318, 399, 467, 660 | Daily counts of `signup_page`, `create`, `google` | No: step and day only |
| Funnel from saved state | `private.funnel_people` and `private.funnel()` (`backend.sql` 171–207), plus by source and taster (213–233) | Signed up, first lesson, back next day, back after a week, plan, paying | Aggregated |
| Where people came from | Saved at sign-up (`auth.js` 103–109, `taster.js` 32–33) | Source and whether they did the taster | Stored on the account |
| Owner dashboard | `admin.html` | Reads the above | Owner only |

**What isn't tracked at all:**
- Survey started but not finished, and which question people leave on.
- Tour opened or abandoned.
- Placement outcomes beyond a "placed" row (`p:<unit>|placed`).
- Sessions: start, length, screens visited.
- Idle sign-outs. We don't know how many learners are being sent to the landing page.
- Errors. There's no client error reporting to the server.
- Taster starts and finishes from people who don't sign up.

So the funnel shows what people have saved, not what they did on the way.

---

## 4. Reconstructing the funnel from existing data

Run these in the Supabase SQL editor. Nothing new is needed.

**Start with what's already there.** `select * from private.funnel();` (`backend.sql` 195–207) already gives signed up, first lesson, back next day, back after a week, chose a plan and paying, by week. The queries below add the survey steps, the lesson and word steps separately, and "active on two different days". They also count people who did the step after joining, not just the day after.

**Assumptions.** Check these if a query errors.
- `auth.users` is the standard Supabase table, with `raw_app_meta_data` and `email_confirmed_at`.
- `public.profiles` has `user_id`, `onboarded`, `level`, `duration`, `reason` (`auth.js` 221–239).
- `public.item_progress` has `user_id`, `item_id`, `box`, `due`, `seen`, `updated_at` (`progress.js` 77–79), plus `fsrs` (`backend.sql` 148).
- These three tables aren't defined in this repo. If a column name differs, run:
  `select table_name, column_name from information_schema.columns where table_schema = 'public' and table_name in ('profiles', 'item_progress') order by 1, 2;`
- Dates are UTC throughout: sign-up dates, and the `s:YYYY-MM-DD` study-day rows (`path.js` 213 uses `toISOString`).
- Team accounts are excluded, as in `private.funnel_people`: `raw_app_meta_data->>'admin' = 'true'`.
- `pct_lost_from_step_above` can be negative. Steps aren't strictly nested: someone can learn a word without a lesson step being recorded. Read the counts, not only the percentages.

**Tested.** I ran these on a throwaway Postgres 16 with nine made-up accounts, one for each case (signed up only, skipped survey, answered survey, lesson only, placed only, studied the next day, studied after a week, recent sign-up, admin). The counts matched the ones I worked out by hand.

### Q1. The funnel, one row per step (counts and % lost)

```sql
-- Q1. The funnel, one row per step.
with accounts as (
  select u.id as user_id, u.created_at::date as joined
  from auth.users u
  where coalesce(u.raw_app_meta_data->>'admin', '') <> 'true'
),
profile as (
  select user_id,
         bool_or(onboarded) as survey_saved,
         bool_or(level is not null or duration is not null) as answered_one
  from public.profiles
  group by user_id
),
progress as (
  select user_id,
         bool_or(item_id like 'v:%') as learned_a_word,
         bool_or(item_id like 'p:%' and item_id not like '%|placed') as finished_a_lesson,
         count(distinct (updated_at at time zone 'UTC')::date) as active_days
  from public.item_progress
  group by user_id
),
steps as (
  select 1 as n, 'Signed up' as step, count(*) as people, count(*) as eligible from accounts
  union all
  select 2, 'Saved the survey (answered or skipped)',
         count(*) filter (where p.survey_saved), count(*) from accounts a left join profile p using (user_id)
  union all
  select 3, 'Answered at least one survey question',
         count(*) filter (where p.answered_one), count(*) from accounts a left join profile p using (user_id)
  union all
  select 4, 'Finished a lesson step',
         count(*) filter (where g.finished_a_lesson), count(*) from accounts a left join progress g using (user_id)
  union all
  select 5, 'Learned a word',
         count(*) filter (where g.learned_a_word), count(*) from accounts a left join progress g using (user_id)
  union all
  select 6, 'Active on 2 or more different days',
         count(*) filter (where g.active_days >= 2), count(*) from accounts a left join progress g using (user_id)
  union all
  select 7, 'Studied the day after joining',
         count(*) filter (where exists (select 1 from public.item_progress i
                where i.user_id = a.user_id and i.item_id = 's:' || to_char(a.joined + 1, 'YYYY-MM-DD'))),
         count(*) filter (where a.joined <= current_date - 1)
  from accounts a
  union all
  select 8, 'Studied 7 or more days after joining',
         count(*) filter (where exists (select 1 from public.item_progress i
                where i.user_id = a.user_id and i.item_id like 's:%' and i.item_id >= 's:' || to_char(a.joined + 7, 'YYYY-MM-DD'))),
         count(*) filter (where a.joined <= current_date - 7)
  from accounts a
)
select n, step, people, eligible,
       round(100.0 * people / nullif(eligible, 0), 1) as pct_of_eligible,
       round(100.0 * (lag(people) over (order by n) - people) / nullif(lag(people) over (order by n), 0), 1) as pct_lost_from_step_above
from steps
order by n;
```

### Q2. The same steps by week of joining

Newest week at the top. Use it to see whether a change helps.

```sql
-- Q2. The same steps by week of joining, to see whether a change helps (newer weeks at the top).
with accounts as (
  select u.id as user_id, u.created_at::date as joined
  from auth.users u
  where coalesce(u.raw_app_meta_data->>'admin', '') <> 'true'
),
profile as (
  select user_id, bool_or(onboarded) as survey_saved from public.profiles group by user_id
),
progress as (
  select user_id,
         bool_or(item_id like 'p:%' and item_id not like '%|placed') as finished_a_lesson,
         bool_or(item_id like 'v:%') as learned_a_word,
         count(distinct (updated_at at time zone 'UTC')::date) as active_days
  from public.item_progress
  group by user_id
)
select date_trunc('week', a.joined)::date as week_of,
       count(*) as signed_up,
       count(*) filter (where p.survey_saved) as saved_survey,
       count(*) filter (where g.finished_a_lesson) as finished_a_lesson,
       count(*) filter (where g.learned_a_word) as learned_a_word,
       count(*) filter (where g.active_days >= 2) as active_2_days,
       count(*) filter (where a.joined <= current_date - 1) as could_be_back_next_day,
       count(*) filter (where a.joined <= current_date - 1 and exists (
             select 1 from public.item_progress i
             where i.user_id = a.user_id and i.item_id = 's:' || to_char(a.joined + 1, 'YYYY-MM-DD'))) as back_next_day
from accounts a
left join profile p using (user_id)
left join progress g using (user_id)
group by 1
order by 1 desc;
```

### Q3. Survey and confirmation checks

```sql
-- Q3.Survey and confirmation checks.
select
  (select count(*) from public.profiles where onboarded and level is null and duration is null) as skipped_survey,
  (select count(*) from public.profiles where onboarded and (level is not null or duration is not null)) as answered_survey,
  (select count(*) from auth.users where coalesce(raw_app_meta_data->>'admin', '') <> 'true') as accounts,
  (select count(email_confirmed_at) from auth.users where coalesce(raw_app_meta_data->>'admin', '') <> 'true') as confirmed_at_set;
```

---

## 5. Recommendations (proposed, not built)

Ranked by how much they could matter for return visits, and how cheaply we can measure them first.

1. **Stop sending expired sessions to the landing page.** Send them to sign-in with a line such as "You were signed out after a day away. Sign in to carry on." Progress is already queued and kept on the device (`progress.js` 222–231), so nothing is lost. Consider a longer limit on personal browsers (for example 30 days) and keep the 24-hour limit only when someone chooses it. *Measure first with the counter below.*
2. **Cut the survey to level and time before the first lesson.** Move reason and reminder to a card after the first lesson, or to Settings. Keep reading (it decides whether the starter can be skipped). Make Continue visible without scrolling: a sticky bottom bar, or moving to the next question on each tap.
3. **Start the first lesson with the four taster words.** They're already known, so the first screen after sign-up feels like the taster carrying on, and the letter chart comes second.
4. **Move placement after the first lesson,** or make "I don't know yet" the default for beginners, so typing Arabic isn't the first task.
5. **Count vocabulary and drill sessions as study days,** so returners are measured fairly and the streak reflects them.
6. **Store "skipped survey" separately** from "finished survey", so the funnel can tell them apart.
7. **Check whether people who chose a reminder time come back more.** This needs the `reminders` table's columns first.

**A small, privacy-respecting way to track the funnel going forward.** Use the same pattern as `private.taps` (`backend.sql` 252–266): one daily counter per step, with no user id, email or device. Each step is one call that adds 1 to today's count. Steps that would answer the questions above:

| Step | Called when | Answers |
|---|---|---|
| `survey_done` / `survey_skipped` | Continue or Skip on the survey | How many skip, and whether that changes after rec. 2 |
| `placement_done` | Placement finishes or is skipped | Whether placement loses people (rec. 4) |
| `tour_seen` | The tour card is shown | Whether the tour matters |
| `first_lesson` | The first lesson step is finished | Time to first value |
| `signin_ok` / `idle_signout` | Sign-in works, or the idle limit sends someone to the landing page | Whether rec. 1 is the biggest leak |

Each counter is one row per day per step (`private.counts (day, step, n)`). Keep 90 days. Show them on the owner dashboard next to the taps. Nothing is linked to a person, which matches the privacy page's promise that we don't track people across the web. Nothing is built yet: tell me if you want it.

---

## One-screen summary

**Biggest leak:** the return visit. The 24-hour idle sign-out (`auth.js` 22, 43–47, 88–90) sends a learner who comes back the next day to the landing page with no message. This is the most likely cause of the drop from "did a lesson" to "came back", but the size isn't measured yet.

**Fix to try first:** send expired sessions to sign-in with a short explanation, and give personal browsers a longer limit. Progress is already kept on the device, so nothing is lost. Add the `idle_signout` counter first, so you can see how many people it's catching.

**Also worth knowing:**
- The first lesson is about 20 taps away, with a 5-question survey in the middle.
- The taster's words aren't used until the seventh step.
- The funnel covers saved state only. We don't record anything inside a lesson.
- Study days don't count vocabulary or drill sessions.

---

_Generated by [Claude Code](https://claude.ai/code)_
