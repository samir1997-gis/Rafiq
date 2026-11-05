# Rafiq in the App Store and Google Play: the listing (#352)

Paste into App Store Connect and the Play Console. Name and subtitle were checked with TypeSafe
(`tools/typesafe-exp/store_listing.py`: 5.56 of 6, ahead of "Learn Arabic & Salah" and "Learn Arabic for Salah").
Every claim matches the app (2.3): 785 words with audio, 36 conversations, 12 units, every word of the salah and 10 short surahs.

## App Store

**Name** (30): Rafiq – Arabic for Muslims
**Subtitle** (30): Understand every word you pray
**Category:** Education (secondary: Reference)
**Keywords** (100, no spaces; the name's words are already searched, so they aren't repeated):
`quran,salah,namaz,prayer,islam,learn,alphabet,quranic,dua,vocabulary,surah,fusha,msa,reading,words`

**Promotional text** (170, can be changed any time without review):
Short daily Arabic lessons from the very first letter, with audio, reviews that make words stick, and every word of your salah explained.

**Description:**

Understand every word of your salah, and learn the Arabic Muslims use, a few minutes a day.

Rafiq takes you from the very first letter to real conversations. Every lesson is short, every word has audio, and Rafiq brings words back just before you'd forget them, so they stick.

YOUR SALAH, WORD BY WORD
• Every word of the prayer explained, from the opening takbīr to the closing salām
• 10 short surahs, word by word
• Pray along: the whole prayer at praying pace, each word lit with its meaning
• Start with the 20 words you say most: over half of everything you say in a four-rakʿah prayer

FROM THE FIRST LETTER
• A reading starter: the letters in shape families, how they join, the vowel marks
• The basics: say your first sentence with your own name
• 12 everyday units, 36 conversations and 785 words with audio, all fully vowelled
• Grammar one idea at a time, in plain English

PRACTISE AND REMEMBER
• Reviews timed for just before you'd forget, built from your own lessons
• Reply in your own words and get feedback on your Arabic
• Real-life scenes: the airport, the doctor, the masjid, a restaurant and more
• Verbs, joining words, a spelling bee, numbers, days, months and colours
• Ask Rafiq, your AI tutor: ask anything about Arabic, or tap Why? after a mistake

MADE FOR YOUR DAY
• 5 to 10 minutes a day, with a daily reminder at the time you choose
• Lessons and audio work without a connection
• Your progress follows you between your phone and rafiq-arabic.com

The Arabic and its vowel marks are checked by a teacher. Rafiq teaches language; for questions about how to pray, ask a scholar.

PLANS
Start with a free week. Then choose Essentials or Complete, monthly or yearly. Payment is charged to your Apple ID at confirmation of purchase. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period. Manage or cancel any time in your App Store account settings.

Terms of use: https://rafiq-arabic.com/terms.html
Privacy policy: https://rafiq-arabic.com/privacy.html

**URLs:** Support https://rafiq-arabic.com/help.html · Marketing https://rafiq-arabic.com · Privacy https://rafiq-arabic.com/privacy.html
**Copyright:** 2026 Rafiq

**Subscriptions** (App Store Connect → Subscriptions, one group "Rafiq"; ids as `supabase/functions/_shared/store.ts` reads them):
| Product id | Name shown | Period | Introductory offer |
|---|---|---|---|
| rafiq_essentials_monthly | Essentials (monthly) | 1 month | Free, 1 week |
| rafiq_essentials_yearly | Essentials (yearly) | 1 year | Free, 1 week |
| rafiq_complete_monthly | Complete (monthly) | 1 month | Free, 1 week |
| rafiq_complete_yearly | Complete (yearly) | 1 year | Free, 1 week |
Prices: the owner's decision (the website is £6.99 / £49.99 and £11.99 / £79.99; Apple and Google take 15% in the small business programmes).

## App privacy (App Store Connect → App Privacy)

Tracking: **No** (no ads, no tracking SDKs, nothing shared with data brokers).
Data collected, all **linked to the user**, **not used for tracking**, purpose **App functionality**:
| Apple's category | What it is in Rafiq |
|---|---|
| Contact info → Email address | the account's email |
| Contact info → Name | the name given at sign-up |
| Identifiers → User ID | the account id |
| Purchases → Purchase history | the plan bought (through the App Store) |
| Usage data → Product interaction | lessons done, words learnt, reviews, streak (to save progress) |
| User content → Other user content | questions to Ask Rafiq; sentences typed in answers |
| Diagnostics → Other diagnostic data | device and browser type, only when the learner sends a report |

The app's `PrivacyInfo.xcprivacy` says the same.

## Age rating

No objectionable content in any category: rate **4+**. If App Store Connect asks about AI assistants or chat, answer **yes**: Ask Rafiq is an AI tutor, limited by its instructions to Arabic and the course; answers can be reported (⚑).

## App Review information

**Sign-in:** review@rafiq-arabic.com · password: the one you set as the GitHub secret `REVIEW_PASSWORD`
(created by Supabase users → `review-account`; it has Complete for free and opens on Home).

**Notes for the reviewer** (paste):
Rafiq teaches Arabic in short daily lessons. An account is needed because each learner's progress, review schedule and plan are saved to their account and sync between devices (and rafiq-arabic.com). The demo account above is signed up, set up and has every feature open.
• Press Continue on Home to start the next lesson; lessons and audio also work offline.
• Ask Rafiq (the Rafiq tab) is an AI tutor powered by Anthropic's Claude. Before the first question the app explains what is sent and asks permission; nothing is sent without it.
• Subscriptions are sold only through in-app purchase (Plans). Sign in with Apple is offered on the sign-in screen.
• Daily reminders are local notifications, only after the learner turns them on.

## Google Play

**App name** (30): Rafiq – Arabic for Muslims
**Short description** (80): Learn Arabic from the first letter and understand every word of your salah.
**Full description:** the App Store description, with the PLANS paragraph as:
Start with a free week. Then choose Essentials or Complete, monthly or yearly. Subscriptions renew automatically until you cancel; manage or cancel any time in Google Play → Payments & subscriptions.
**Category:** Education · **Tags:** Language learning, Education
**Subscriptions:** `rafiq_essentials` and `rafiq_complete`, each with base plans `monthly` and `yearly`, and a free 1-week trial offer.
**Data safety:** the same data as App privacy above: collected, not shared, encrypted in transit, deletable in the app (Settings → Delete my account) or by email.
**Content rating:** answer the IARC questionnaire with no violence, sexual content, gambling or user-to-user communication; it comes out as Everyone / PEGI 3.
**Testing before release:** a new personal Play account needs a closed test with at least 12 testers for 14 days before going public.
