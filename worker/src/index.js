/* rafiq-judge — a Cloudflare Worker that holds the TypeSafe key and answers
   a fixed set of questions for the site:

     POST {kind:'vocab',   arabic, glosses:[...], answer}  → {ok}
     POST {kind:'produce', english, model, answer}         → {ok, err}
     POST {kind:'build',   english, model, answer}         → {ok, order}
     POST {kind:'rewrite', task, original, model, answer}  → {ok, changes, err}
     POST {kind:'prompt',  task, model, answer}            → {done, grammar, err}
     POST {kind:'reply',   situation, previous, previous_en, suggested, answer} → {fits, grammar, err}

   Values are TypeSafe probabilities (done is a 0–2 score); the page decides
   what to do with them. The questions are built here, not in the browser, so
   the endpoint can't be used as a general-purpose TypeSafe proxy. Question
   wording comes from tools/typesafe-exp, where it was measured. */

const API = 'https://api.typesafe.ai/v1/systemone';
const ORIGINS = [
  'https://rafiq-arabic.com',
  'https://www.rafiq-arabic.com',
  'https://sal716eh-spec.github.io',
  'capacitor://localhost',   // the iPhone app (#35)
  'https://localhost',       // the Android app
];
const MAX = 600;   // characters per field; the longest model answer is ~250

const VOCAB_Q = {
  ok: {
    type: 'noul',
    instructions: {
      task: 'A beginner learning Arabic was shown `arabic` and typed its English meaning as `answer`. ' +
            'The textbook glosses are in `glosses`. Should a fair teacher mark it correct?',
      accept: ['a synonym or near-synonym with the same meaning',
               "the same word without 'to', 'a' or 'the', or in another form (plural, past tense)",
               'a small spelling slip where the intended English word is obvious',
               'leaving out a gender note such as (m) or (f)'],
      reject: ['a different word, even a related one (bedroom for room)',
               'an opposite or a word from the same topic with another meaning'],
    },
    criteria: { true: 'Mark correct', false: 'Mark wrong' },
  },
};

const ERRS = {
  gender_agreement: 'A word has the wrong gender (masculine/feminine) for what it refers to',
  wrong_person_or_tense: 'A verb or pronoun is in the wrong person, number or tense',
  wrong_word: 'One word or detail is replaced by a different one, changing a fact',
  different_meaning: 'The words are rearranged or changed so the sentence says something else',
  missing_word: 'Needed words are left out, so the sentence is incomplete',
  spelling: 'A word is misspelled so it is a different or non-existent word',
  grammar_other: 'Some other grammatical error',
};

const PRODUCE_Q = {
  ok: {
    type: 'noul',
    instructions: {
      task: 'A beginner was asked to say `english_prompt` in Modern Standard Arabic and wrote ' +
            "`learner_answer`. `model_answer` is one correct answer. Is the learner's answer correct?",
      ignore: ['missing vowel marks (harakat) and case endings that are not written',
               'hamza forms, ة written as ه, ى as ي, spacing, punctuation',
               'synonyms and any word order Arabic allows'],
      not_ignore: ['wrong gender, person, number or tense',
                   'a changed fact, word or meaning', 'missing words', 'misspelled words'],
    },
    criteria: { true: 'Correct answer', false: 'Contains an error' },
  },
  err: {
    type: 'choice',
    instructions: 'What is the main problem with `learner_answer` as an Arabic rendering of ' +
                  '`english_prompt`, compared with `model_answer`?',
    criteria: {
      none: 'Correct: same meaning as the model answer and grammatical. Missing vowel marks, ' +
            'hamza spelling, ة/ه and attached و are fine; so are synonyms and word orders Arabic allows.',
      ...ERRS,
    },
  },
};

// Build-it: the learner's tile order differs from the model answer. Meaning alone
// let a scrambled order through (tools/typesafe-exp/round2b.py), so word
// order gets its own question.
const BUILD_Q = {
  ok: PRODUCE_Q.ok,
  order: {
    type: 'noul',
    instructions: {
      task: '`learner_answer` is the pieces of `model_answer` put in a different order. Is the new order ' +
            'natural, grammatical Arabic that means the same as `english_prompt`?',
      rules: ['an adjective must come straight after its noun (الدور الخامس, not الخامس في الدور)',
              'the order of events must not change',
              'a demonstrative must agree with the noun after it'],
    },
    criteria: { true: 'Acceptable order', false: 'Unnatural, ungrammatical, or changes the meaning' },
  },
};

// Transform and Fix-it: a typed rewrite of `original`.
const REWRITE_Q = {
  ok: {
    type: 'noul',
    instructions: {
      task: 'A beginner was given `original` and asked to do `task`. They wrote `learner_answer`. ' +
            '`model_answer` is one correct answer. Did they do the task correctly?',
      ignore: ['missing vowel marks (harakat) and case endings that are not written',
               'hamza forms, ة written as ه, ى as ي, spacing, punctuation',
               'a different but equally correct way of doing the task'],
      not_ignore: ['the change asked for was not made, or only partly made',
                   'other words changed that should have stayed the same',
                   'wrong gender, person, number or tense', 'misspelled words'],
    },
    criteria: { true: 'Task done correctly', false: 'Not done correctly' },
  },
  changes: {
    type: 'noul',
    instructions: {
      task: 'Compare `original`, `model_answer` and `learner_answer`, ignoring vowel marks. Does `learner_answer` ' +
            'make every change that `model_answer` makes, or an equally correct alternative, with no new mistakes?',
      check: ['every verb that should change has changed (e.g. both verbs to the past)',
              'after كم the noun is singular (كم حصة, never كم حصص)',
              "the person is right: asking someone a question uses 'you' (تـ), not 'I' (أ)"],
    },
    criteria: { true: 'All required changes made correctly', false: 'A required change is missing or wrong' },
  },
  err: {
    type: 'choice',
    instructions: 'What is the main problem with `learner_answer` as an answer to `task` applied to `original`?',
    criteria: {
      none: 'Correct: the task is done and the sentence is grammatical. Missing vowel marks, ' +
            'hamza spelling and ة/ه are fine, and so is another correct way of doing it.',
      not_done: 'The change asked for in `task` was not made, or the sentence was copied unchanged',
      ...ERRS,
    },
  },
};

// Conversation partner: the learner replies in their own words to the other
// speaker's line. With the situation in the state: 46/47 labelled replies and
// all 90 suggested replies judged a fit (tools/typesafe-exp/round3b.py).
/* Asked only when the other speaker has a next line: that line was written as
   an answer to `expected_reply`, so check the learner's own reply still gives it
   what it responds to (measured: at 0.6 it let none of 9 non-following replies
   through on 24 labelled cases; tools/typesafe-exp/follows.py). */
const FOLLOWS_Q = {
  type: 'noul',
  instructions: {
    task: "In a beginner's Arabic conversation (`situation`), the other person's next line `next_line` (`next_line_english`) " +
          'was written as a reply to the expected learner line `expected_reply`. The learner actually said `learner_reply` ' +
          '(earlier they said: `learner_earlier`). Does the learner\'s actual reply give `next_line` everything it responds to?',
    yes_if: ['it asks the same question (in any wording), or gives the same kind of answer with their own details',
             'what next_line reacts to is present in the actual reply, even if other details differ'],
    no_if: ['next_line answers a question the learner did not ask',
            "next_line reacts to something the learner didn't say, or said the opposite of",
            'next_line asks for something the learner has already told them',
            "next_line uses a name that isn't the learner's (check what they said earlier)",
            'the learner asked a question that next_line ignores'],
  },
  criteria: { true: 'Next line still fits', false: 'Next line no longer fits' },
};

const REPLY_Q = {
  fits: {
    type: 'noul',
    instructions: {
      task: "In a beginner's Arabic conversation (`situation`), the other person said `previous_line`. The learner " +
            'replied `learner_reply`. Could this naturally be said next in this conversation?',
      counts: ["an answer to a question, with the learner's own details (it need not match `suggested_reply`)",
               'a thank-you, an acknowledgement or a polite response to what was said',
               'a question or remark that naturally belongs to this situation at this point, as `suggested_reply` does'],
      does_not_count: ['a remark about something unrelated to the situation or to what was just said',
                       'an answer to a different question from the one asked',
                       'a personal question out of the blue that ignores what was just said'],
      note: 'Ignore grammar and spelling here.',
    },
    criteria: { true: 'A natural next line', false: "Doesn't follow on" },
  },
  grammar: {
    type: 'noul',
    instructions: {
      task: 'Ignoring missing vowel marks, is `learner_reply` grammatical, correctly spelled Arabic?',
      check: ['gender agreement, and addressing a man as أنتَ', 'the right person and tense on verbs',
              'numbers with the right gender (ثلاثة إخوة, not ثلاث إخوة)'],
    },
    criteria: { true: 'No errors', false: 'At least one error' },
  },
  err: {
    type: 'choice',
    instructions: 'What is the main grammar or spelling problem in `learner_reply`?',
    criteria: {
      none: 'No grammar or spelling problem (missing vowel marks are fine)',
      gender_agreement: ERRS.gender_agreement,
      wrong_person_or_tense: ERRS.wrong_person_or_tense,
      spelling: ERRS.spelling,
      grammar_other: ERRS.grammar_other,
    },
  },
};

// Free speaking: an open answer to a prompt. Task completion and grammar are
// separate, so a learner can hear "done, but check the grammar".
const PROMPT_Q = {
  done: {
    type: 'score',
    instructions: 'A beginner was asked `task` and answered in Arabic with `learner_answer`. ' +
                  '`model_answer` is one example answer; theirs may say different things. ' +
                  'How completely does their answer do what `task` asks? Ignore grammar here.',
    criteria: ['Does not answer the task: off-topic or nothing relevant',
               'Partly answers: on topic, but noticeably less than the task asks for ' +
               '(fewer sentences, questions or items than requested)',
               'Fully answers the task, even if the details differ from the model answer'],
  },
  grammar: {
    type: 'noul',
    instructions: {
      task: 'Ignoring missing vowel marks, is `learner_answer` grammatical, correctly spelled Arabic?',
      check: ['gender agreement between nouns, adjectives, pronouns and verbs',
              'the right person on verbs', 'indefinite accusative nouns written with their alif (دجاجا)'],
    },
    criteria: { true: 'No errors', false: 'At least one error' },
  },
  err: {
    type: 'choice',
    instructions: 'What is the main grammar or spelling problem in `learner_answer`?',
    criteria: {
      none: 'No grammar or spelling problem (missing vowel marks are fine)',
      gender_agreement: ERRS.gender_agreement,
      wrong_person_or_tense: ERRS.wrong_person_or_tense,
      spelling: ERRS.spelling,
      grammar_other: ERRS.grammar_other,
    },
  },
};

const str = v => typeof v === 'string' && v.trim() !== '' && v.length <= MAX;

function cors(origin) {
  const h = { 'Vary': 'Origin' };
  if (ORIGINS.includes(origin)) {
    h['Access-Control-Allow-Origin'] = origin;
    h['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    h['Access-Control-Allow-Headers'] = 'Content-Type';
    h['Access-Control-Max-Age'] = '86400';
  }
  return h;
}

function reply(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json', ...cors(origin) },
  });
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });
    if (req.method !== 'POST') return reply({ error: 'POST only' }, 405, origin);
    if (!ORIGINS.includes(origin)) return reply({ error: 'origin not allowed' }, 403, origin);

    let b;
    try { b = await req.json(); } catch { return reply({ error: 'bad json' }, 400, origin); }

    let state, questions;
    if (b.kind === 'vocab' && str(b.arabic) && str(b.answer) &&
        Array.isArray(b.glosses) && b.glosses.length > 0 && b.glosses.length <= 8 && b.glosses.every(str)) {
      state = { arabic: b.arabic, glosses: b.glosses, answer: b.answer };
      questions = VOCAB_Q;
    } else if ((b.kind === 'produce' || b.kind === 'build') && str(b.english) && str(b.model) && str(b.answer)) {
      state = { english_prompt: b.english, model_answer: b.model, learner_answer: b.answer };
      questions = b.kind === 'build' ? BUILD_Q : PRODUCE_Q;
    } else if (b.kind === 'rewrite' && str(b.task) && str(b.original) && str(b.model) && str(b.answer)) {
      state = { task: b.task, original: b.original, model_answer: b.model, learner_answer: b.answer };
      questions = REWRITE_Q;
    } else if (b.kind === 'reply' && str(b.previous) && str(b.previous_en) && str(b.suggested) && str(b.answer)) {
      state = { situation: str(b.situation) ? b.situation : 'a friendly conversation',
                previous_line: b.previous, previous_line_english: b.previous_en,
                suggested_reply: b.suggested, learner_reply: b.answer };
      questions = REPLY_Q;
      // optional: the other speaker's next line, to check it still follows
      if (str(b.next) && str(b.next_en)) {
        const earlier = Array.isArray(b.earlier) ? b.earlier.filter(str).slice(-6) : [];
        Object.assign(state, { next_line: b.next, next_line_english: b.next_en, expected_reply: b.suggested,
                               learner_earlier: earlier.length ? earlier : ['(nothing yet)'] });
        questions = { ...REPLY_Q, follows: FOLLOWS_Q };
      }
    } else if (b.kind === 'prompt' && str(b.task) && str(b.model) && str(b.answer)) {
      state = { task: b.task, model_answer: b.model, learner_answer: b.answer };
      questions = PROMPT_Q;
    } else {
      return reply({ error: 'bad request' }, 400, origin);
    }

    const r = await fetch(API, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${env.TYPESAFE_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ state, model: 'jev-latest', questions }),
    });
    if (!r.ok) return reply({ error: 'upstream ' + r.status }, 502, origin);
    // Flatten each answer to its number (noul, score) or label (choice).
    const a = (await r.json()).answers, out = {};
    for (const [k, v] of Object.entries(a)) out[k] = v.type === 'choice' ? v.choice : v.type === 'score' ? v.score : v.noul;
    return reply(out, 200, origin);
  },
};
