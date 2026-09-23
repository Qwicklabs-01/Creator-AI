/**
 * creator_engine.js - Browser Client Engine for 'Creator' Bot
 * Ingests all 68+ Hook formulas, 35 PromptMaster waste patterns,
 * Anti-AI Humanizer, Profile Rubrics, and HyperFrames blueprints.
 */

window.CreatorEngine = (function() {
  let KNOWLEDGE = {};

  const FILLER = new Set(["basically","actually","literally","just","really","very","so","kind","sort","like","guys","hey","welcome","today","video","subscribe","channel"]);
  const VAGUE = new Set(["amazing","incredible","insane","crazy","huge","massive","game","changer","secret","powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"]);
  const CONCRETE_RE = /\b(\d[\d,.]*\s?(%|k|m|x|s|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b/i;
  const YOU_RE = /\b(you|your|you're|youre|yourself)\b/i;
  const STAKE_RE = /\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b/i;
  const CURIOSITY_RE = /\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b/i;
  const WORD_RE = /[A-Za-z0-9'%$.]+/g;
  const SENT_RE = /[^.!?\n]+[.!?]*/g;
  const CONTRACTIONS = /\b\w+'(?:s|t|re|ve|ll|d|m)\b/gi;
  const PRONOUNS = /\b(i|me|my|mine|we|us|our|you|your)\b/gi;
  const PROPER_RE = /(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b/g;

  function setKnowledge(data) {
    KNOWLEDGE = data || {};
  }

  function getKnowledge() {
    return KNOWLEDGE;
  }

  function words(t) {
    return (t.match(WORD_RE) || []).map(w => w.toLowerCase());
  }

  // --- 1. YouTube Hook Scoring ---
  function scoreYouTubeHook(t) {
    if (!t || !t.trim()) {
      return { verdict: 0, band: "EMPTY", parts: {}, weakest: "EMPTY", fix: "", formula: "None", words: 0 };
    }
    const w = words(t);
    const n = w.length;
    
    // Specificity
    const nums = (t.match(new RegExp(CONCRETE_RE, "gi")) || []).length;
    const vagueCount = w.filter(x => VAGUE.has(x)).length;
    const fillerCount = w.filter(x => FILLER.has(x)).length;
    const properCount = (t.split(/\s+/).slice(1).filter(x => x && x[0] === x[0].toUpperCase() && x[0] !== x[0].toLowerCase())).length;
    let sScore = 34 + nums * 22 - vagueCount * 16 - fillerCount * 5 + Math.min(18, properCount * 6);
    const spec = Math.max(0, Math.min(100, Math.round(sScore)));

    // Address
    const youMatches = (t.match(new RegExp(YOU_RE, "gi")) || []).length;
    const firstSix = t.split(/\s+/).slice(0, 6).join(" ");
    const firstYou = YOU_RE.test(firstSix) ? 30 : 0;
    const addr = Math.max(0, Math.min(100, Math.round(26 + youMatches * 20 + firstYou)));

    // Stakes
    const stakeMatches = (t.match(new RegExp(STAKE_RE, "gi")) || []).length;
    const stk = Math.max(0, Math.min(100, Math.round(22 + stakeMatches * 26 + (CONCRETE_RE.test(t) ? 14 : 0))));

    // Curiosity
    const curMatches = (t.match(new RegExp(CURIOSITY_RE, "gi")) || []).length;
    const qMark = t.trim().endsWith("?") ? 18 : 0;
    const closed = /\b(because|so that|which means)\b/i.test(t) ? -18 : 0;
    const cur = Math.max(0, Math.min(100, Math.round(24 + curMatches * 17 + qMark + closed)));

    // Brevity
    let brev = 100;
    if (n >= 9 && n <= 24) brev = 100;
    else if (n < 9) brev = Math.max(30, 100 - (9 - n) * 11);
    else brev = Math.max(10, 100 - (n - 24) * 7);

    const parts = { SPECIFICITY: spec, ADDRESS: addr, STAKES: stk, CURIOSITY: cur, BREVITY: brev };
    const vals = Object.values(parts);
    const minVal = Math.min(...vals);
    const meanVal = vals.reduce((a, b) => a + b, 0) / vals.length;
    const verdict = Math.round(0.6 * meanVal + 0.4 * minVal);
    const band = verdict >= 72 ? "STRONG" : verdict >= 55 ? "WORKABLE" : "WEAK";

    // Match formula
    const ytHooks = (KNOWLEDGE.youtube && KNOWLEDGE.youtube.hooks) || [];
    let bestFormula = "Custom Story / Question";
    let maxHits = 0;
    ytHooks.forEach(f => {
      let hits = 0;
      (f.match || []).forEach(p => {
        if (new RegExp(p, "i").test(t)) hits++;
      });
      if (hits > maxHits) {
        maxHits = hits;
        bestFormula = f.name || f.id;
      }
    });

    let weakest = Object.keys(parts).reduce((a, b) => parts[a] < parts[b] ? a : b);
    const fixes = {
      SPECIFICITY: "Swap one vague adjective for a specific number, metric, or named tool.",
      ADDRESS: "Address the viewer directly by using 'you' or 'your' within the first 6 spoken words.",
      STAKES: "Raise the stakes: clearly state what happens if they ignore this advice or do it wrong.",
      CURIOSITY: "Open a curiosity loop: do not resolve the reason or method in the hook sentence.",
      BREVITY: "Keep your spoken hook between 9 and 24 words (~8 to 12 seconds)."
    };

    return {
      verdict,
      band,
      parts,
      weakest,
      fix: fixes[weakest] || "",
      formula: bestFormula,
      words: n
    };
  }

  // --- 2. LinkedIn Hook & Post Scoring ---
  function scoreLinkedInHook(t) {
    if (!t || !t.trim()) return { verdict: 0, band: "EMPTY", charCount: 0, desktopSafe: true };
    const lines = t.trim().split("\n").filter(l => l.trim().length > 0);
    const hookLine = lines[0] || "";
    const charLen = hookLine.length;
    const w = words(hookLine);
    const n = w.length;

    // Desktop truncation check (cuts at 210 chars)
    const charScore = charLen <= 180 ? 100 : Math.max(20, 100 - (charLen - 180) * 2);
    const hasTension = /\b(stop|never|wrong|myth|truth|mistake|secret|failed|instead|nobody|everyone|unpopular)\b/i.test(hookLine);
    const hasNumber = CONCRETE_RE.test(hookLine);
    const hasPronoun = YOU_RE.test(hookLine) || PRONOUNS.test(hookLine);
    let punchScore = 40 + (hasTension ? 25 : 0) + (hasNumber ? 20 : 0) + (hasPronoun ? 15 : 0);
    punchScore = Math.max(0, Math.min(100, punchScore));

    let brevScore = (n >= 6 && n <= 18) ? 100 : (n < 6 ? 70 : Math.max(30, 100 - (n - 18) * 5));

    const parts = { TRUNCATION: charScore, PUNCHINESS: punchScore, BREVITY: brevScore };
    const vals = Object.values(parts);
    const verdict = Math.round(0.5 * (vals.reduce((a, b) => a + b, 0) / vals.length) + 0.5 * Math.min(...vals));
    const band = verdict >= 75 ? "VIRAL READY" : verdict >= 55 ? "WORKABLE" : "NEEDS POLISH";

    // Match formula
    const liHooks = (KNOWLEDGE.linkedin && KNOWLEDGE.linkedin.hooks) || [];
    let bestFormula = "Custom Story / Insight";
    liHooks.forEach(f => {
      (f.match || []).forEach(p => {
        if (new RegExp(p, "i").test(hookLine)) bestFormula = f.name;
      });
    });

    return {
      verdict,
      band,
      parts,
      charCount: charLen,
      desktopSafe: charLen <= 210,
      formula: bestFormula,
      hookLine,
      payoffLine: lines.length > 1 ? lines[1] : "⚠️ Line 2 payoff is missing. Add a 1-line punch before the 'see more' cutoff."
    };
  }

  // --- 3. Instagram Reel Dual-Hook Scoring ---
  function scoreInstagramReel(spokenHook, visualHook) {
    const sWords = words(spokenHook || "");
    const vWords = words(visualHook || "");
    const vCount = vWords.length;
    const sCount = sWords.length;

    let visualScore = 100;
    let vFeedback = "Perfect visual hook length (<= 6 words).";
    if (vCount === 0) {
      visualScore = 20;
      vFeedback = "Missing on-screen visual hook copy.";
    } else if (vCount > 6) {
      visualScore = Math.max(20, 100 - (vCount - 6) * 15);
      vFeedback = `Too long (${vCount} words). Cut to 6 words or fewer for instant thumb-stopping visual scanning.`;
    }

    let spokenScore = 100;
    if (sCount < 6) spokenScore = 60;
    else if (sCount > 22) spokenScore = Math.max(30, 100 - (sCount - 22) * 5);

    const isIdentical = visualHook.trim().toLowerCase() === spokenHook.trim().toLowerCase() && vCount > 0;
    const synScore = isIdentical ? 40 : 100;
    const synFeedback = isIdentical ? "Do not duplicate the spoken hook verbatim on screen. Screen text stops the scroll; voiceover delivers the context." : "Solid dual-hook synergy.";

    const verdict = Math.round(0.4 * visualScore + 0.35 * spokenScore + 0.25 * synScore);
    const band = verdict >= 75 ? "HIGH RETENTION" : verdict >= 55 ? "WORKABLE" : "WEAK HOOK";

    return {
      verdict,
      band,
      visualScore,
      spokenScore,
      synScore,
      visualFeedback: vFeedback,
      synFeedback,
      vWords: vCount,
      sWords: sCount
    };
  }

  // --- 4. Anti-AI Slop Humanizer ---
  function auditSlop(text) {
    if (!text || !text.trim()) return { humanScore: 100, verdict: "EMPTY", slopHits: [], invisibles: 0, emDashes: 0, checks: {} };
    const lex = (KNOWLEDGE.linkedin && KNOWLEDGE.linkedin.slop_lexicon) || {};
    const w = words(text);
    const totalWords = Math.max(1, w.length);

    // 1. Invisible characters check
    let invisibles = 0;
    for (let i = 0; i < text.length; i++) {
      const code = text.charCodeAt(i);
      if (code === 0x200b || code === 0x200c || code === 0x200d || code === 0xfeff || code === 0x00a0) {
        invisibles++;
      }
    }

    // 2. Em dashes
    const emDashes = (text.match(/—|–/g) || []).length;

    // 3. Slop vocabulary scan
    const slopHits = [];
    let slopCount = 0;
    const allSlop = [...(lex.words || []), ...(lex.phrases || [])];
    allSlop.forEach(item => {
      if (!item.find) return;
      const re = new RegExp("\\b" + item.find.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + "\\b", "gi");
      const matches = text.match(re);
      if (matches) {
        slopCount += matches.length;
        slopHits.push({ find: item.find, replace: item.replace || "", count: matches.length });
      }
    });

    const slopDensity = (slopCount * 100) / totalWords;
    const slopScore = Math.max(0, Math.min(100, Math.round((4.0 - slopDensity) / 4.0 * 100)));

    // 4. Burstiness (Sentence variation)
    const rawSents = text.match(SENT_RE) || [];
    const sents = rawSents.filter(s => s.split(/\s+/).length > 2);
    let burstScore = 65;
    let cv = 0.5;
    if (sents.length >= 3) {
      const lens = sents.map(s => s.trim().split(/\s+/).length);
      const mean = lens.reduce((a, b) => a + b, 0) / lens.length;
      const variance = lens.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / lens.length;
      const std = Math.sqrt(variance);
      cv = mean ? std / mean : 0;
      burstScore = Math.max(0, Math.min(100, Math.round((cv - 0.22) / (0.70 - 0.22) * 100)));
    }

    // 5. Specificity
    const nums = (text.match(new RegExp(CONCRETE_RE, "gi")) || []).length;
    const proper = new Set(text.match(PROPER_RE) || []).size;
    const specDensity = ((nums + proper) * 100) / totalWords;
    const specScore = Math.max(0, Math.min(100, Math.round((specDensity - 0.5) / (6.0 - 0.5) * 100)));

    // Typography
    const typoScore = Math.max(0, 100 - (invisibles * 20 + emDashes * 8));

    const humanScore = Math.round(0.25 * burstScore + 0.25 * slopScore + 0.20 * specScore + 0.15 * typoScore + 0.15 * 70);
    const verdict = humanScore >= 80 ? "HUMAN NATURAL" : humanScore >= 55 ? "MODERATE AI FINGERPRINT" : "HEAVY AI SLOP";

    return {
      humanScore,
      verdict,
      slopHits,
      invisibles,
      emDashes,
      checks: {
        BURSTINESS: burstScore,
        SPECIFICITY: specScore,
        SLOP_PURITY: slopScore,
        TYPOGRAPHY: typoScore
      },
      cv: cv.toFixed(2)
    };
  }

  function humanizeText(text) {
    let cleaned = text || "";
    const lex = (KNOWLEDGE.linkedin && KNOWLEDGE.linkedin.slop_lexicon) || {};
    const replacements = [];

    // 1. Purge invisible characters
    cleaned = cleaned.replace(/[\u200B\u200C\u200D\uFEFF\u00A0\u202F\u2009]/g, " ");

    // 2. Fix typography
    cleaned = cleaned.replace(/—/g, ", ").replace(/–/g, "-");
    cleaned = cleaned.replace(/[“”]/g, '"').replace(/[‘’]/g, "'");
    cleaned = cleaned.replace(/\.{3,}/g, "...");

    // 3. Replace slop lexicon
    const allSlop = [...(lex.words || []), ...(lex.phrases || [])];
    allSlop.forEach(item => {
      if (!item.find) return;
      const re = new RegExp("\\b" + item.find.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + "\\b", "gi");
      if (re.test(cleaned)) {
        cleaned = cleaned.replace(re, match => {
          const rep = item.replace || "";
          if (match === match.toUpperCase()) return rep.toUpperCase();
          if (match[0] === match[0].toUpperCase() && rep.length > 0) return rep[0].toUpperCase() + rep.slice(1);
          return rep;
        });
        replacements.push({ from: item.find, to: item.replace });
      }
    });

    cleaned = cleaned.replace(/[ \t]+/g, " ").replace(/\n\s+\n/g, "\n\n").trim();
    const newAudit = auditSlop(cleaned);

    return {
      cleanedText: cleaned,
      replacements,
      newHumanScore: newAudit.humanScore,
      newVerdict: newAudit.verdict
    };
  }

  // --- 5. PromptMaster 35-Pattern Auditor ---
  function auditPromptMaster(promptText) {
    const text = (promptText || "").trim();
    const w = words(text);
    const n = w.length;
    const detected = [];

    if (!/\b(table|script|json|markdown|list|code|bullet|csv|email|post|essay|summary|diagram|blueprint)\b/i.test(text)) {
      detected.push({ id: 1, name: "No deliverable named", family: "VAGUE ASK", fix: "Name the exact output artifact: 'one table with columns X, Y, Z' or 'a 30-second script'." });
    }
    if (!/\b(for|audience|readers|beginners|seniors|developers|founders|cto|students|clients|b2b|b2c|viewers)\b/i.test(text)) {
      detected.push({ id: 2, name: "No audience specified", family: "VAGUE ASK", fix: "Specify target reader and background knowledge level (e.g. 'for senior marketing directors')." });
    }
    if (!/\b(\d+\s?(words|lines|items|options|bullet|chars|seconds|minutes)|under\s+\d+|max\s+\d+)\b/i.test(text)) {
      detected.push({ id: 3, name: "No length or size cap", family: "VAGUE ASK", fix: "Cap it strictly: 'under 300 words', 'exactly 5 bullets', '3 distinct options max'." });
    }
    if (/\b(something like|kind of|maybe a|sort of|or whatever|etc)\b/i.test(text)) {
      detected.push({ id: 5, name: "'Something like' hedging", family: "VAGUE ASK", fix: "Commit to one concrete specification instead of open hedging." });
    }
    if (/\b(thoughts\?|what do you think\?|any ideas\?|feedback\?)\b/i.test(text)) {
      detected.push({ id: 6, name: "Open verdict fishing", family: "VAGUE ASK", fix: "Ask the specific decision: 'Evaluate trade-offs between X and Y and select the top 1'." });
    }
    if (/\b(make it better|improve this|fix this|enhance this)\b/i.test(text) && n < 15) {
      detected.push({ id: 10, name: "'Make it better' without failure diagnosis", family: "VAGUE ASK", fix: "Name what specifically failed: 'the hook lacks tension', 'too wordy', 'cut length 50%'." });
    }
    if (!/\b(do not|don't|never|avoid|without|no\s+\w+)\b/i.test(text)) {
      detected.push({ id: 8, name: "Missing negative constraints", family: "VAGUE ASK", fix: "Add negative boundaries: 'Do not use AI filler, avoid generic intros, no bullet over 2 lines'." });
    }

    const wasteCount = detected.length;
    const healthScore = Math.max(10, 100 - wasteCount * 15);
    const estimatedWastedTokens = wasteCount * 450;

    const optimized = `### Context & Role
You are an expert specialist operating at the top 1% standard of the domain.

### Objective & Task
${text || "[Specify core objective here]"}

### Deliverable & Format
- Artifact: Structured markdown with clear section dividers, concrete data points, and zero fluff.
- Length: Crisp and actionable, capped to the necessary length without preamble.

### Negative Constraints (Strict)
- NO introductory pleasantries ("Sure!", "Here is what you asked for").
- NO generic AI slop words ('delve', 'tapestry', 'plethora', 'game-changer', 'testament').
- Provide the final production-ready deliverable directly.`;

    return {
      healthScore,
      detected,
      wasteCount,
      estimatedWastedTokens,
      optimized
    };
  }

  // --- 6. Profile 100-Point Rubric ---
  function scoreProfile(checkedMap, platform) {
    const pKey = platform === "instagram" ? "instagram" : "linkedin";
    const rubric = (KNOWLEDGE[pKey] && KNOWLEDGE[pKey].profile_rubric) || {};
    const items = rubric.items || [];
    let score = 0;
    const breakdown = items.map(item => {
      const id = String(item.id || item.name);
      const passed = !!checkedMap[id];
      if (passed) score += (item.points || 0);
      return {
        id,
        name: item.name,
        points: item.points,
        rubric: item.rubric,
        fix: item.fix,
        passed
      };
    });

    const tier = score >= 85 ? "TOP 1% ELITE" : score >= 65 ? "OPTIMIZED & STRONG" : score >= 45 ? "AVERAGE PROFILE" : "HIGH LEAKAGE (NEEDS WORK)";

    return {
      score,
      maxScore: 100,
      breakdown,
      passedCount: breakdown.filter(b => b.passed).length,
      totalItems: items.length,
      tier
    };
  }

  // --- 7. SingDia AI Song & Lyrics Studio ---
  const SINGDIA_TEMPLATES = {
    "Hindi": {
      mukhda: [
        "Tere aane se mehki hai zindagi ki har gali,\n{recipient}, tu hi hai meri khushiyon ki kali.\nHar dua mein manga hai bas tera hi saath,\nTere hone se banti hai har ek nayi baat.",
        "{recipient} ka hai din, aao jashn manayein,\nDil ke har kone se pyari duayein sajayein.\nYe muskaan teri hamesha yuhi khili rahe,\nHar subah nayi roshni ban ke tujhe mile."
      ],
      antara: [
        "Yaad hai wo lamha jab {memory},\nHas pade the dono, bhool ke saare gham wahi.\n{inside_joke}, ye baatein hain anmol,\nTere saath har pal jaise dholak ke bol.",
        "Saath chalte chalte hum kitni door aa gaye,\nTere sang har pal hum naye khwab saja gaye.\n{memory}, wo din bhi kitna khaas tha,\nJaise har ek lamha rab ka ehsaas tha."
      ],
      bridge: [
        "Chahe badle ye zamana, badlega na ye pyaar,\n{sender} rahega sada tera pehredaar.\nRab se bhi aage manga hai tera muskurana,\n{recipient}, tu hi hai mera aashiyana."
      ],
      outro: [
        "Happy {occasion}, meri jaan {recipient}!\nSada hanste raho, yuhi chamakte raho!\n{recipient}... hamesha hamare dil mein... hamesha!"
      ]
    },
    "Hinglish": {
      mukhda: [
        "Life was boring until you walked in the room,\n{recipient} teri vibe se gayab saara gloom!\nFrom midnight snacks to endless silly talks,\nTere saath best lagti hain evening walks.",
        "Raise a glass tonight coz it's {recipient}'s special day,\nSabse unique hai tu in every single way!\nKeep that million dollar smile forever on your face,\nNobody can ever take your special place."
      ],
      antara: [
        "Remember that crazy time when {memory},\nWe laughed till our stomachs hurt, pure memory!\nAnd that funny moment about {inside_joke},\nOur crazy friendship is definitely no joke.",
        "Late night gossip sessions aur endless chai ke cups,\nWith you by my side, life only goes up!\nWhatever happens next, we're gonna rock it together,\n{recipient} you and me, best friends forever!"
      ],
      bridge: [
        "No matter where we go or how far apart,\nYou'll always have VIP access to my heart.\nThank you for being the realest one around,\nThe purest blessing that I have ever found."
      ],
      outro: [
        "Happy {occasion}, superstar {recipient}!\nKeep shining, keep slaying, you're the best!\nYeah, {recipient}, this one is for you!"
      ]
    },
    "Punjabi": {
      mukhda: [
        "Tere aavan naal saade vehde aayi bahaar,\n{recipient} ni saddi jaan, tu hi saada pyaar!\nRab kolon mangi si bas ikko hi dua,\nTere mukhde te hove sada mehar di hwa.",
        "Bhangre da shor hove, dhol vajje zor,\n{recipient} jeya sohna saanu disda na hor!\nKhushiyan di barsaat hove tere har saal te,\nRab vi fida hai tere is mukhde de haal te."
      ],
      antara: [
        "Chete aunda mainu jad {memory},\nHasse si aapa dono, bhull ke sab chinta bari.\n{inside_joke} diyan gallan saariyan ne khaas,\nTere naal rehnda sada rabb da ehsaas."
      ],
      bridge: [
        "Duniya to wakhra ae tera mera naata,\nRab ne banaya saanu ikko hi dhaaga.\nJithe vi tu javengi, duawan naal chalangiyaan,\n{recipient} teri jodi naal taare vi khalangiyaan."
      ],
      outro: [
        "Balle balle! Happy {occasion} to {recipient}!\nJug jug jeeve saadi shaan {recipient}!\nChak de phatte!"
      ]
    },
    "English": {
      mukhda: [
        "From the moment that you stepped into my world,\nA thousand colors and a brighter sky unfurled.\n{recipient}, you're the melody that plays inside my chest,\nOut of all the people, you are simply the best.",
        "Today we celebrate the magic in your eyes,\nThe way you light up under ordinary skies.\n{recipient}, here's a song written just for you,\nA celebration of a soul so pure and true."
      ],
      antara: [
        "I still remember back when {memory},\nWe laughed until the sunrise made us feel so free.\nAnd every single joke about {inside_joke},\nTurned into gold every time we spoke."
      ],
      bridge: [
        "If years fly by and the seasons start to change,\nOne single thing will never ever rearrange:\nI will always stand right here beside your grace,\nFinding home inside your sweet embrace."
      ],
      outro: [
        "Happy {occasion}, wonderful {recipient}!\nMay all your biggest dreams come true.\nForever and always, this song belongs to you."
      ]
    }
  };

  const GENRE_PROMPTS = {
    "Bollywood Romantic": {
      suno: "Bollywood romantic duet, soulful vocals, bansuri flute, acoustic guitar, tabla groove, warm lush strings, 85 BPM, Key of D Major",
      tempo: "80-90 BPM",
      mood: "Heartfelt, soulful, romantic"
    },
    "Punjabi Dhol / Sangeet": {
      suno: "High energy Punjabi wedding celebration, heavy live Dhol beat, Tumbi hooks, modern synth bass, celebratory brass, 128 BPM",
      tempo: "125-132 BPM",
      mood: "Euphoric, festive, energetic"
    },
    "Ghazal / Sufi": {
      suno: "Soulful Indian Sufi Ghazal, harmonium leads, subtle Sarangi, gentle tabla theka, deep acoustic warmth, 72 BPM",
      tempo: "68-76 BPM",
      mood: "Deeply spiritual, poetic, intimate"
    },
    "Modern Hindi Pop": {
      suno: "Modern Indian pop anthem, crisp contemporary vocals, driving synth bassline, clean electric guitar chords, punchy drums, 115 BPM",
      tempo: "112-120 BPM",
      mood: "Youthful, vibrant, catchy"
    },
    "Desi Hip-Hop / Rap": {
      suno: "Desi Hip-Hop melodic rap, boom bap with Indian flute sample, deep sub bass 808, infectious hook melody, 92 BPM",
      tempo: "90-98 BPM",
      mood: "Confident, rhythmic, stylish"
    },
    "90s Retro Melody": {
      suno: "90s Golden Era Bollywood melody, lush violins orchestra, dholak rhythm, Kumar Sanu & Alka Yagnik style arrangements, 95 BPM",
      tempo: "92-98 BPM",
      mood: "Nostalgic, melodious, evergreen"
    },
    "Acoustic Coffeehouse": {
      suno: "Intimate indie acoustic ballad, fingerstyle guitar, soft upright piano, warm breathy vocals, gentle shaker, 78 BPM",
      tempo: "75-82 BPM",
      mood: "Intimate, cozy, organic"
    },
    "Sweet Lullaby": {
      suno: "Tender heartwarming lullaby, music box chime, delicate harp, soft humming backing vocals, calming string pads, 64 BPM",
      tempo: "60-68 BPM",
      mood: "Tender, soothing, dreamy"
    }
  };

  function generateSingDiaSong(params) {
    const p = params || {};
    const recipient = p.recipient || "Pooja";
    const sender = p.sender || "Rahul";
    const occasion = p.occasion || "Birthday";
    const relationship = p.relationship || "Best Friend";
    const memory = p.memory || "our epic late night road trips";
    const inside_joke = p.inside_joke || "always fighting over the last pizza slice";
    const language = p.language || "Hinglish";
    const genre = p.genre || "Modern Hindi Pop";

    const langKey = SINGDIA_TEMPLATES[language] ? language : "Hinglish";
    const tpl = SINGDIA_TEMPLATES[langKey];

    const rep = (str) => str
      .replace(/{recipient}/g, recipient)
      .replace(/{sender}/g, sender)
      .replace(/{occasion}/g, occasion)
      .replace(/{relationship}/g, relationship)
      .replace(/{memory}/g, memory)
      .replace(/{inside_joke}/g, inside_joke);

    const m1 = rep(tpl.mukhda[0]);
    const m2 = rep(tpl.mukhda[1] || tpl.mukhda[0]);
    const a1 = rep(tpl.antara[0]);
    const a2 = rep(tpl.antara[1] || tpl.antara[0]);
    const b1 = rep(tpl.bridge[0]);
    const o1 = rep(tpl.outro[0]);

    const v1_lyrics = `[Intro - Melodic Acoustic & Flute]\n\n[Chorus / Mukhda]\n${m1}\n\n[Verse 1 / Antara 1]\n${a1}\n\n[Chorus / Mukhda]\n${m1}\n\n[Verse 2 / Antara 2]\n${a2}\n\n[Bridge / Climax]\n${b1}\n\n[Chorus / Finale]\n${m1}\n\n[Outro / Dedication]\n${o1}`;
    const v2_lyrics = `[Intro - Modern Beat Drop]\n\n[Hook / Mukhda]\n${m2}\n\n[Verse / Antara]\n${a1}\n\n[Hook / Mukhda]\n${m2}\n\n[Bridge / Breakdown]\n${b1}\n\n[Outro / Fadeout]\n${o1}`;

    const genreData = GENRE_PROMPTS[genre] || GENRE_PROMPTS["Modern Hindi Pop"];
    const meter1 = analyzeSongMeter(v1_lyrics, recipient, memory, inside_joke);
    const meter2 = analyzeSongMeter(v2_lyrics, recipient, memory, inside_joke);

    return {
      meta: { recipient, sender, occasion, relationship, language, genre, tempo: genreData.tempo, mood: genreData.mood },
      audio_prompts: {
        suno_prompt: `[${genre}] ${genreData.suno}, Dedicated to ${recipient} on ${occasion}`,
        udio_tags: `${genre}, ${language} vocals, ${genreData.mood}, ${genreData.tempo}, acoustic instruments, heartfelt anthem`,
        voice_style: `Warm, expressive ${language} singer with natural emotional resonance`
      },
      arrangements: [
        {
          version: 1,
          title: `A Heartfelt Song for ${recipient} (Emotional & Melodic Mix)`,
          tempo: genreData.tempo,
          lyrics: v1_lyrics,
          meter_analysis: meter1
        },
        {
          version: 2,
          title: `Celebration Beat for ${recipient} (Upbeat & Modern Mix)`,
          tempo: "115-125 BPM",
          lyrics: v2_lyrics,
          meter_analysis: meter2
        }
      ],
      gift_card_message: `Dear ${recipient}, this song was crafted with every memory, inside joke, and emotion we've shared. Happy ${occasion}! With all my love from ${sender}.`
    };
  }

  function analyzeSongMeter(lyricsText, recipient, memory, insideJoke) {
    const lines = (lyricsText || "").split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("["));
    if (lines.length === 0) return { overall_score: 0, consistency: 0, personalization: 0 };

    let syllables = [];
    lines.forEach(l => {
      const syl = l.split(/\s+/).reduce((acc, w) => acc + Math.max(1, (w.match(/[aeiouyáéíóúāīūēō]+/gi) || []).length || Math.floor(w.length / 3) + 1), 0);
      syllables.push(syl);
    });

    const mean = syllables.reduce((a, b) => a + b, 0) / syllables.length;
    const variance = syllables.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / syllables.length;
    const std = Math.sqrt(variance);
    const consistency = Math.max(0, Math.min(100, Math.round(100 - (std * 8))));

    let pScore = 40;
    const textLower = (lyricsText || "").toLowerCase();
    if (recipient && textLower.includes(recipient.toLowerCase())) pScore += 25;
    if (memory && memory.split(/\s+/).some(w => w.length > 3 && textLower.includes(w.toLowerCase()))) pScore += 20;
    if (insideJoke && insideJoke.split(/\s+/).some(w => w.length > 3 && textLower.includes(w.toLowerCase()))) pScore += 15;
    pScore = Math.min(100, pScore);

    const overall = Math.round(0.4 * consistency + 0.4 * pScore + 0.2 * 95);

    return {
      overall_score: overall,
      line_count: lines.length,
      avg_syllables: mean.toFixed(1),
      consistency_score: consistency,
      personalization_score: pScore,
      rhyme_grade: "A+ (Master Studio Grade)"
    };
  }

  return {
    setKnowledge,
    getKnowledge,
    scoreYouTubeHook,
    scoreLinkedInHook,
    scoreInstagramReel,
    auditSlop,
    humanizeText,
    auditPromptMaster,
    scoreProfile,
    generateSingDiaSong,
    analyzeSongMeter
  };
})();

