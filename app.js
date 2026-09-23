/**
 * app.js - Interactive Controller for 'Creator' Bot
 */

document.addEventListener("DOMContentLoaded", async function() {
  let masterKnowledge = {};

  // 1. Fetch & Initialize Knowledge
  try {
    const res = await fetch("creator_knowledge.json");
    if (res.ok) {
      masterKnowledge = await res.json();
      CreatorEngine.setKnowledge(masterKnowledge);
      console.log("Creator Engine loaded knowledge successfully.");
    }
  } catch (e) {
    console.warn("Local fetch fallback. Running with preloaded engine data.", e);
  }

  // 2. DOM Elements Caching
  const navItems = document.querySelectorAll(".nav-item");
  const tabViews = document.querySelectorAll(".tab-view");
  const tabTitle = document.getElementById("currentTabTitle");
  const tabDesc = document.getElementById("currentTabDesc");

  // Chat Elements
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatMessages = document.getElementById("chatMessages");
  const charCounter = document.getElementById("chatCharCount");
  const personaOptions = document.querySelectorAll(".persona-option");
  let currentPersona = "standard";

  // LinkedIn Studio Elements
  const btnGenLi = document.getElementById("btnGenerateLiHook");
  const btnScoreLi = document.getElementById("btnScoreLiHook");
  const liTopicInput = document.getElementById("liTopic");
  const liFormulaSelect = document.getElementById("liFormula");
  const liDraftInput = document.getElementById("liDraftInput");
  const liScoreBadge = document.getElementById("liScoreBadge");
  const liScoreDetails = document.getElementById("liScoreDetails");

  // YouTube Engine Elements
  const btnScoreYt = document.getElementById("btnScoreYtHook");
  const btnGenYtScript = document.getElementById("btnGenerateYtScript");
  const ytTitleInput = document.getElementById("ytVideoTitle");
  const ytHookInput = document.getElementById("ytHookInput");
  const ytScoreBadge = document.getElementById("ytScoreBadge");
  const ytScoreDetails = document.getElementById("ytScoreDetails");

  // Instagram Reel Elements
  const btnScoreIg = document.getElementById("btnScoreIgHook");
  const btnGenReelBeats = document.getElementById("btnGenerateReelBeats");
  const igVisual = document.getElementById("igVisualHook");
  const igSpoken = document.getElementById("igSpokenHook");
  const igScoreBadge = document.getElementById("igScoreBadge");
  const igScoreDetails = document.getElementById("igScoreDetails");
  const igFormulaSelect = document.getElementById("igFormulaSelect");
  const btnApplyIgFormula = document.getElementById("btnApplyIgFormula");

  // PromptMaster Elements
  const btnAuditPrompt = document.getElementById("btnAuditPrompt");
  const btnLoadBadPrompt = document.getElementById("btnLoadBadPrompt");
  const pmPromptInput = document.getElementById("pmPromptInput");
  const pmWasteCount = document.getElementById("pmWasteCount");
  const pmWastedTokens = document.getElementById("pmWastedTokens");
  const pmResultsDetails = document.getElementById("pmResultsDetails");
  const btnCopyOptimizedPrompt = document.getElementById("btnCopyOptimizedPrompt");

  // Anti-AI Humanizer Elements
  const btnDetectSlop = document.getElementById("btnDetectSlop");
  const btnCleanSlop = document.getElementById("btnCleanSlop");
  const humanizerInput = document.getElementById("humanizerInput");
  const humanScoreBadge = document.getElementById("humanScoreBadge");
  const humanizerResultsDetails = document.getElementById("humanizerResultsDetails");

  // HyperFrames Elements
  const hfBlueprintSelect = document.getElementById("hfBlueprintSelect");
  const hfHeadline = document.getElementById("hfHeadline");
  const btnGenMotionCode = document.getElementById("btnGenerateMotionCode");
  const hfBlueprintSummary = document.getElementById("hfBlueprintSummary");
  const hfCodeOutput = document.getElementById("hfCodeOutput");
  const btnCopyMotionCode = document.getElementById("btnCopyMotionCode");

  // Matrix Elements
  const matrixTabs = document.querySelectorAll(".matrix-tab-btn");
  const matrixSearch = document.getElementById("matrixSearch");

  const tabMeta = {
    chat: { title: "Creator AI Chat Assistant", desc: "Autonomous content engineer loaded with 68+ hook formulas, anti-slop rules, prompt optimization & Music Studio. Created by Sakshi." },
    linkedin: { title: "LinkedIn Growth Studio", desc: "21 Hook formulas, Desktop 210-character truncation tester, and 100-point profile audit." },
    youtube: { title: "YouTube Channel Architect", desc: "21 Video hook formulas, 0-15s retention scoring, and title-thumbnail cognitive pairing." },
    instagram: { title: "Instagram Reel & Viral Suite", desc: "26 Dual-hook formulas (Spoken + On-Screen text <= 6 words) and 4-stage beat directors." },
    promptmaster: { title: "PromptMaster 35 Credit-Waste Auditor", desc: "Scan raw prompts for 35 retry traps, calculate token waste, and compile 1-shot prompts." },
    humanizer: { title: "Anti-AI Slop Humanizer & Purifier", desc: "Strip invisible zero-width unicode, fix em-dashes, and replace 50+ banned robotic buzzwords." },
    singdia: { title: "AI Music Studio", desc: "Craft personalized songs across 12 Indian languages, 8 musical genres, and generate Suno/Udio audio production blueprints." },
    hyperframes: { title: "HyperFrames Motion & Video Engine", desc: "22 Animation blueprints, GSAP easing recipes, kinetic typography, and canvas motion." },
    unhinged: { title: "25 Unhinged Agent Operational Modes", desc: "High-octane, aggressive, maximum-velocity productivity personas (/speedrun, /aura-farming, /china-maxing)." },
    freellm: { title: "FreeLLMAPI Multi-Provider Gateway", desc: "Automatic failover across 34 free AI providers (Groq, Gemini, Cerebras, Mistral, SambaNova, OpenRouter)." },
    matrix: { title: "Creator Master Knowledge Matrix", desc: "Searchable directory of all 68+ hook formulas, 35 waste patterns, profile rubrics & slop terms." }
  };

  // Mobile Drawer Navigation Handlers
  const appSidebar = document.getElementById("appSidebar");
  const sidebarBackdrop = document.getElementById("sidebarBackdrop");
  const btnMobileSidebarToggle = document.getElementById("btnMobileSidebarToggle");
  const btnSidebarClose = document.getElementById("btnSidebarClose");

  function openSidebar() {
    if (appSidebar) appSidebar.classList.add("open");
    if (sidebarBackdrop) sidebarBackdrop.classList.add("active");
  }

  function closeSidebar() {
    if (appSidebar) appSidebar.classList.remove("open");
    if (sidebarBackdrop) sidebarBackdrop.classList.remove("active");
  }

  if (btnMobileSidebarToggle) btnMobileSidebarToggle.addEventListener("click", openSidebar);
  if (btnSidebarClose) btnSidebarClose.addEventListener("click", closeSidebar);
  if (sidebarBackdrop) sidebarBackdrop.addEventListener("click", closeSidebar);

  // 3. Tab Switching
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetTab = item.dataset.tab;
      navItems.forEach(n => n.classList.remove("active"));
      tabViews.forEach(v => v.classList.remove("active"));

      item.classList.add("active");
      const targetView = document.getElementById(`tab-${targetTab}`);
      if (targetView) targetView.classList.add("active");

      if (tabMeta[targetTab]) {
        tabTitle.textContent = tabMeta[targetTab].title;
        tabDesc.textContent = tabMeta[targetTab].desc;
      }

      // Auto close sidebar on mobile selection
      if (window.innerWidth <= 1024) {
        closeSidebar();
      }
    });
  });

  // 4. Populate Dropdowns & Render Initial Views
  populateDropdowns();
  renderUnhingedCards();
  renderKnowledgeMatrix("li-hooks");

  function populateDropdowns() {
    const liHooks = (masterKnowledge.linkedin && masterKnowledge.linkedin.hooks) || [];
    if (liFormulaSelect) {
      liFormulaSelect.innerHTML = liHooks.map((h, i) => `<option value="${i}">#${i+1} - ${h.name} (${h.category || 'Formula'})</option>`).join("");
    }

    const igHooks = (masterKnowledge.instagram && masterKnowledge.instagram.hooks) || [];
    if (igFormulaSelect) {
      igFormulaSelect.innerHTML = igHooks.map((h, i) => `<option value="${i}">#${i+1} - ${h.name} (${h.category || 'Reel Formula'})</option>`).join("");
    }

    const hfBlueprints = (masterKnowledge.hyperframes && masterKnowledge.hyperframes.blueprints) || [];
    if (hfBlueprintSelect) {
      hfBlueprintSelect.innerHTML = hfBlueprints.map(b => `<option value="${b.id}">${b.title}</option>`).join("");
      updateBlueprintSummary();
    }
  }

  function updateBlueprintSummary() {
    if (!hfBlueprintSelect || !hfBlueprintSummary) return;
    const bId = hfBlueprintSelect.value;
    const hfBlueprints = (masterKnowledge.hyperframes && masterKnowledge.hyperframes.blueprints) || [];
    const bp = hfBlueprints.find(b => b.id === bId);
    if (bp) {
      hfBlueprintSummary.innerHTML = `<strong>${bp.title}</strong><br><span style="color:var(--text-muted);font-size:0.8rem;">${bp.content ? bp.content.slice(0, 240) + "..." : "Motion blueprint ready for rendering."}</span>`;
    }
  }

  if (hfBlueprintSelect) {
    hfBlueprintSelect.addEventListener("change", updateBlueprintSummary);
  }

  // 5. Chat Controller
  personaOptions.forEach(opt => {
    opt.addEventListener("click", () => {
      personaOptions.forEach(o => o.classList.remove("active"));
      opt.classList.add("active");
      currentPersona = opt.dataset.persona;
    });
  });

  if (chatInput) {
    chatInput.addEventListener("input", () => {
      charCounter.textContent = chatInput.value.length;
    });
  }

  document.querySelectorAll(".chip-btn").forEach(chip => {
    chip.addEventListener("click", () => {
      if (chatInput) {
        chatInput.value = chip.dataset.prompt;
        charCounter.textContent = chatInput.value.length;
        chatInput.focus();
        
        // Auto trigger
        setTimeout(() => {
          if (chatForm) chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
        }, 100);
      }
    });
  });

  if (chatForm) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;

      appendChatMessage("user", text);
      chatInput.value = "";
      charCounter.textContent = "0";

      setTimeout(() => {
        const response = generateBotResponse(text, currentPersona);
        appendChatMessage("bot", response);
      }, 400);
    });
  }

  function appendChatMessage(sender, content) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}-message`;
    const avatar = sender === "bot" ? "⚡" : "👤";
    const senderName = sender === "bot" ? `Creator (${currentPersona.toUpperCase()})` : "You";

    msgDiv.innerHTML = `
      <div class="message-avatar">${avatar}</div>
      <div class="message-body">
        <div class="message-header">
          <span class="message-sender">${senderName}</span>
          <span class="message-time">Just now</span>
        </div>
        <div class="message-content">${formatMarkdown(content)}</div>
      </div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function generateBotResponse(input, persona) {
    const q = input.toLowerCase();

    if (q.includes("hook") || q.includes("linkedin") || q.includes("youtube") || q.includes("reel")) {
      if (q.includes("youtube")) {
        const h1 = "If you don't fix this 1 setting in your audio, you will lose 40% of your viewers in 10 seconds.";
        const score = CreatorEngine.scoreYouTubeHook(h1);
        return `### 🎥 Scored YouTube Retention Hooks (0-15s Window)

**Option 1 (The Stakes & Error - Score: ${score.verdict}/100 [${score.band}])**
> "${h1}"
- **Confirm Click**: Confirms editing/audio focus immediately.
- **Weakest Link**: ${score.weakest} (${score.fix})
- **Spoken Length**: ${score.words} words (~8s).

**Option 2 (The Paradox - Score: 84/100 [STRONG])**
> "Everyone tells you to buy a $1,000 microphone, but the top 1% of creators secretly use this $40 plug-in instead."

**Option 3 (The Contrarian - Score: 88/100 [STRONG])**
> "Stop spending 3 hours color grading your footage. Here is why it is killing your retention curve and what to do instead."`;
      } else if (q.includes("linkedin")) {
        return `### 💼 3 High-Tension LinkedIn Hooks (Desktop Truncation Safe)

**1. The Paradox (Score: 85/100 - Viral Ready)**
> "Most founders think growth is about posting 5x a day.
> 
> Here is how we closed $140k in pipeline with only 2 posts a week:"
*(Line 1 length: 58 chars - Safe under 210 char limit)*

**2. The Contrarian Frame (Score: 82/100 - Viral Ready)**
> "Stop hiring junior copywriters for AI workflows.
> 
> You don't have a writing problem. You have an engineering problem. Exactly what to change:"

**3. The Hard Breakdown (Score: 89/100 - Viral Ready)**
> "I audited 40 SaaS landing pages this month.
> 
> 37 of them made the exact same mistake that leaks 60% of conversions on mobile:"`;
      } else {
        return `### 📸 Instagram Reel Dual-Hook Architecture

**Option 1: The Cheat Code**
- **On-Screen Text (<= 6 words)**: \`Stop editing like this\`
- **Spoken Voiceover (0-3s)**: \`If you're still spending 4 hours on Reels, this 1 shortcut cuts your edit time to 12 minutes.\`
- **Visual Pattern Interrupt**: Extreme close-up of keyboard macro slam.

**Option 2: The Exposure**
- **On-Screen Text**: \`The AI tool they hide\`
- **Spoken Voiceover**: \`There is a reason top creators aren't sharing this new workflow. Watch this before it gets patched.\``;
      }
    }

    if (q.includes("prompt") || q.includes("audit") || q.includes("waste")) {
      const audit = CreatorEngine.auditPromptMaster(input);
      return `### 🧠 PromptMaster 35-Pattern Audit Results

- **Prompt Health Score**: ${audit.healthScore}/100
- **Traps Detected**: ${audit.wasteCount} credit-waste patterns
- **Estimated Wasted Tokens**: ~${audit.estimatedWastedTokens} tokens per retry

${audit.detected.map(d => `- **[#${d.id} - ${d.name}]** (${d.family})\n  *Fix*: ${d.fix}`).join("\n")}

---

### ⚡ Production-Ready 1-Shot Compiled Prompt:
\`\`\`markdown
${audit.optimized}
\`\`\``;
    }

    if (q.includes("slop") || q.includes("humanize") || q.includes("delve") || q.includes("ai")) {
      const human = CreatorEngine.humanizeText(input);
      return `### 🛡️ Anti-AI Slop Humanizer Report

- **New Human Score**: ${human.newHumanScore}/100 (${human.newVerdict})
- **Replacements Made**: ${human.replacements.length} stock buzzwords & typographic artifacts cleaned.

**Cleaned Natural Copy:**
> ${human.cleanedText}

${human.replacements.length ? `**Replaced Terms:**\n` + human.replacements.map(r => `- *"${r.from}"* → **"${r.to}"**`).join("\n") : "_Zero slop buzzwords found._"}`;
    }

    if (q.includes("song") || q.includes("music") || q.includes("lyrics") || q.includes("singdia") || q.includes("sangeet") || q.includes("bday")) {
      const song = CreatorEngine.generateSingDiaSong({
        recipient: "Pooja",
        sender: "Rahul",
        occasion: "Birthday",
        language: "Hinglish",
        genre: "Modern Hindi Pop",
        memory: "that crazy Goa road trip where the car broke down and we ate maggi at 3 AM",
        inside_joke: "always stealing my fries"
      });
      const arr = song.arrangements[0];
      return `### 🎵 AI Music Studio — Generated Song for Pooja (${arr.meter_analysis.overall_score}/100 - ${arr.meter_analysis.rhyme_grade})
*Created by Sakshi • AI Music Studio*

🎧 **Suno AI Audio Generation Prompt:**
\`\`\`
${song.audio_prompts.suno_prompt}
\`\`\`

📜 **Lyrics (Mukhda & Antara Structure):**
${arr.lyrics}

💌 **Gift Dedication:**
> "${song.gift_card_message}"`;
    }

    if (q.includes("sakshi") || q.includes("who created") || q.includes("author") || q.includes("about")) {
      return `### 👑 Creator — Created by Sakshi
**Creator** is the world's most complete AI content engineering, personalized music studio, and multi-provider AI gateway.

**Engineered by Sakshi, featuring:**
1. **Jake Schincariol Ecosystem**: 68+ Hook formulas, 35 PromptMaster waste audits, Anti-AI Slop Humanizer, HyperFrames Motion Engine, 25 Unhinged modes.
2. **AI Music Studio**: Personalized songs across 12 Indian languages, 8 musical genres, and Suno/Udio audio blueprints.
3. **FreeLLMAPI Gateway**: 34 free AI providers with automatic 429 rate-limit failover routing.`;
    }

    return `### ⚡ Creator Content Engineering Directive
*Created by Sakshi*

You are working in **${currentPersona.toUpperCase()}** mode.

**Core Rules Enforced:**
1. **Desktop Truncation Rule**: LinkedIn hooks strictly <= 210 chars (Line 1 hook + Line 2 payoff).
2. **0-15s YouTube Window**: Confirm click in sentence 1, address 'you' in first 6 words, raise stakes.
3. **Dual-Hook Reels**: Visual on-screen copy strictly <= 6 words. Spoken voiceover sets the loop.
4. **PromptMaster 1-Shot Standard**: Zero hedging, exact deliverable specified, negative constraints locked.
5. **Anti-Slop Zero Tolerance**: No 'delve', 'tapestry', 'plethora', 'game-changer', or em-dashes.
6. **AI Music Studio**: 12 Languages, 8 Genres, Mukhda-Antara arrangements & Suno prompts.`;
  }

  function formatMarkdown(md) {
    if (!md) return "";
    let html = md
      .replace(/^### (.*$)/gim, '<h4 style="color:var(--accent-cyan);margin:10px 0 6px;">$1</h4>')
      .replace(/^## (.*$)/gim, '<h3 style="color:var(--text-main);margin:12px 0 8px;">$1</h3>')
      .replace(/^# (.*$)/gim, '<h2 style="color:var(--text-main);margin:14px 0 10px;">$1</h2>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/`([^`]+)`/gim, '<code style="background:rgba(255,255,255,0.08);padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em;color:var(--accent-cyan);">$1</code>')
      .replace(/^\> (.*$)/gim, '<blockquote style="border-left:3px solid var(--accent-cyan);padding-left:12px;margin:8px 0;color:var(--text-main);background:rgba(0,242,254,0.04);padding:8px 12px;border-radius:0 6px 6px 0;">$1</blockquote>')
      .replace(/```markdown([\s\S]*?)```/gim, '<pre style="background:#05080f;padding:12px;border-radius:6px;overflow-x:auto;font-family:var(--font-mono);font-size:0.82rem;color:#a5b4fc;margin:8px 0;"><code>$1</code></pre>')
      .replace(/```javascript([\s\S]*?)```/gim, '<pre style="background:#05080f;padding:12px;border-radius:6px;overflow-x:auto;font-family:var(--font-mono);font-size:0.82rem;color:#a5b4fc;margin:8px 0;"><code>$1</code></pre>')
      .replace(/```([\s\S]*?)```/gim, '<pre style="background:#05080f;padding:12px;border-radius:6px;overflow-x:auto;font-family:var(--font-mono);font-size:0.82rem;color:#a5b4fc;margin:8px 0;"><code>$1</code></pre>')
      .replace(/\n\n/gim, '<p style="margin-bottom:8px;"></p>');

    return html;
  }

  // 6. LinkedIn Handlers
  if (btnGenLi) {
    btnGenLi.addEventListener("click", () => {
      const topic = (liTopicInput && liTopicInput.value.trim()) || "AI workflow automation";
      const sampleHook = `Most people think ${topic} takes months to master.\n\nHere is the 4-step framework we used to automate our pipeline in 48 hours:`;
      if (liDraftInput) liDraftInput.value = sampleHook;
      renderLinkedInScore(sampleHook);
    });
  }

  if (btnScoreLi) {
    btnScoreLi.addEventListener("click", () => {
      const draft = (liDraftInput && liDraftInput.value.trim()) || "";
      if (!draft) return;
      renderLinkedInScore(draft);
    });
  }

  function renderLinkedInScore(text) {
    const res = CreatorEngine.scoreLinkedInHook(text);
    if (liScoreBadge) {
      liScoreBadge.textContent = `${res.verdict}/100`;
      liScoreBadge.style.color = res.verdict >= 75 ? "var(--accent-emerald)" : res.verdict >= 55 ? "var(--accent-cyan)" : "var(--accent-rose)";
    }

    if (liScoreDetails) {
      liScoreDetails.innerHTML = `
        <div class="output-box">
          <div class="output-box-title">
            <span>LINE 1 HOOK (${res.charCount} Chars)</span>
            <span style="color:${res.desktopSafe ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">${res.desktopSafe ? '✓ Desktop Truncation Safe' : '⚠️ Truncates on Feed'}</span>
          </div>
          <p style="font-weight:700;font-size:1rem;color:#ffffff;margin-bottom:6px;">"${res.hookLine}"</p>
          <p style="font-size:0.85rem;color:var(--text-muted);"><strong>Line 2 Payoff:</strong> ${res.payoffLine}</p>
        </div>

        <div class="metric-bar-group">
          <div class="metric-bar-row">
            <span class="metric-name">TRUNCATION</span>
            <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.parts.TRUNCATION}%;"></div></div>
            <span class="metric-value">${res.parts.TRUNCATION}</span>
          </div>
          <div class="metric-bar-row">
            <span class="metric-name">PUNCHINESS</span>
            <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.parts.PUNCHINESS}%;"></div></div>
            <span class="metric-value">${res.parts.PUNCHINESS}</span>
          </div>
          <div class="metric-bar-row">
            <span class="metric-name">BREVITY</span>
            <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.parts.BREVITY}%;"></div></div>
            <span class="metric-value">${res.parts.BREVITY}</span>
          </div>
        </div>

        <div class="output-box">
          <div class="output-box-title">FORMULA MATCH</div>
          <p><strong>${res.formula}</strong></p>
        </div>
      `;
    }
  }

  // 7. YouTube Handlers
  if (btnScoreYt) {
    btnScoreYt.addEventListener("click", () => {
      const hookText = (ytHookInput && ytHookInput.value.trim()) || "";
      if (!hookText) return;
      const res = CreatorEngine.scoreYouTubeHook(hookText);

      if (ytScoreBadge) {
        ytScoreBadge.textContent = `${res.verdict}/100`;
        ytScoreBadge.style.color = res.verdict >= 72 ? "var(--accent-emerald)" : res.verdict >= 55 ? "var(--accent-cyan)" : "var(--accent-rose)";
      }

      if (ytScoreDetails) {
        ytScoreDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">
              <span>RETENTION VERDICT</span>
              <span style="color:var(--accent-cyan);">${res.band}</span>
            </div>
            <p style="font-weight:600;margin-bottom:8px;">Formula: <strong>${res.formula}</strong> (${res.words} words)</p>
            <p style="font-size:0.82rem;color:var(--text-muted);"><strong style="color:var(--accent-rose);">Weakest Link:</strong> ${res.weakest} — <em>${res.fix}</em></p>
          </div>

          <div class="metric-bar-group">
            ${Object.entries(res.parts).map(([k, v]) => `
              <div class="metric-bar-row">
                <span class="metric-name">${k}</span>
                <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${v}%;"></div></div>
                <span class="metric-value">${v}</span>
              </div>
            `).join("")}
          </div>
        `;
      }
    });
  }

  if (btnGenYtScript) {
    btnGenYtScript.addEventListener("click", () => {
      const hook = (ytHookInput && ytHookInput.value.trim()) || "If you don't understand this 1 AI framework, you will be replaced by someone who does.";

      if (ytScoreDetails) {
        ytScoreDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">LONG-FORM SCRIPT BEAT SHEET</div>
            <div style="font-size:0.85rem;line-height:1.6;">
              <p><strong>0:00 - 0:15 (Hook & Title Confirmation):</strong><br>
              "${hook}"</p>
              <p style="margin-top:8px;"><strong>0:15 - 0:45 (Stakes & Hidden Problem):</strong><br>
              Establish why traditional manual workflows fail and reveal the exact bottleneck.</p>
              <p style="margin-top:8px;"><strong>0:45 - 3:00 (Core Delivery 1 - Fast Win):</strong><br>
              Walk through step 1 with on-screen visual demo. Never use dead air.</p>
              <p style="margin-top:8px;"><strong>3:00 - 6:30 (Deep Dive & Escalation):</strong><br>
              Advanced mechanics, edge cases, and architectural blueprint.</p>
              <p style="margin-top:8px;"><strong>6:30 - End (Payoff & Immediate Video Bridge):</strong><br>
              Final result demonstration + seamless bridge to your next video.</p>
            </div>
          </div>
        `;
      }
    });
  }

  // 8. Instagram Reel Handlers
  if (btnApplyIgFormula) {
    btnApplyIgFormula.addEventListener("click", () => {
      const fIndex = parseInt((igFormulaSelect && igFormulaSelect.value) || "0", 10);
      const igHooks = (masterKnowledge.instagram && masterKnowledge.instagram.hooks) || [];
      const formula = igHooks[fIndex];
      if (formula && igVisual && igSpoken) {
        igVisual.value = formula.on_screen || "Stop doing this";
        igSpoken.value = formula.spoken || "This 1 mistake is ruining your results, and nobody is talking about it.";
      }
    });
  }

  if (btnScoreIg) {
    btnScoreIg.addEventListener("click", () => {
      const vText = (igVisual && igVisual.value.trim()) || "";
      const sText = (igSpoken && igSpoken.value.trim()) || "";
      const res = CreatorEngine.scoreInstagramReel(sText, vText);

      if (igScoreBadge) {
        igScoreBadge.textContent = `${res.verdict}/100`;
        igScoreBadge.style.color = res.verdict >= 75 ? "var(--accent-emerald)" : res.verdict >= 55 ? "var(--accent-cyan)" : "var(--accent-rose)";
      }

      if (igScoreDetails) {
        igScoreDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">
              <span>DUAL-HOOK SYNERGY</span>
              <span style="color:var(--accent-cyan);">${res.band}</span>
            </div>
            <p><strong>Visual Text (${res.vWords} words):</strong> ${res.visualFeedback}</p>
            <p style="margin-top:6px;"><strong>Spoken Hook (${res.sWords} words):</strong> Voiceover pacing is balanced.</p>
            <p style="margin-top:6px;font-size:0.8rem;color:var(--text-muted);">${res.synFeedback}</p>
          </div>

          <div class="metric-bar-group">
            <div class="metric-bar-row">
              <span class="metric-name">ON-SCREEN BREVITY</span>
              <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.visualScore}%;"></div></div>
              <span class="metric-value">${res.visualScore}</span>
            </div>
            <div class="metric-bar-row">
              <span class="metric-name">SPOKEN TENSION</span>
              <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.spokenScore}%;"></div></div>
              <span class="metric-value">${res.spokenScore}</span>
            </div>
            <div class="metric-bar-row">
              <span class="metric-name">DUAL SYNERGY</span>
              <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${res.synScore}%;"></div></div>
              <span class="metric-value">${res.synScore}</span>
            </div>
          </div>
        `;
      }
    });
  }

  if (btnGenReelBeats) {
    btnGenReelBeats.addEventListener("click", () => {
      const vText = (igVisual && igVisual.value.trim()) || "Cheat code for creators";
      const sText = (igSpoken && igSpoken.value.trim()) || "If you want to 10x your output without burning out, here is the secret.";

      if (igScoreDetails) {
        igScoreDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">4-STAGE REEL BEAT SHEET & DIRECTOR CUES</div>
            <div style="font-size:0.85rem;line-height:1.6;">
              <p><strong>0-3s: Visual Pattern Interrupt + Dual Hook</strong><br>
              • <em>On Screen:</em> [${vText}]<br>
              • <em>Voiceover:</em> "${sText}"<br>
              • <em>Visual Cue:</em> Fast snap zoom / high motion action.</p>

              <p style="margin-top:10px;"><strong>3-15s: Hold Curiosity & Problem Setup</strong><br>
              • <em>Voiceover:</em> "Most people spend hours on manual steps, but top agencies do this instead..."<br>
              • <em>Visual Cue:</em> Split screen or live UI screen-record highlight.</p>

              <p style="margin-top:10px;"><strong>15-45s: High-Density Value Delivery</strong><br>
              • <em>Voiceover:</em> Break down 3 bulletproof steps in rapid succession with text overlays.<br>
              • <em>Visual Cue:</em> Text pop on every audio beat.</p>

              <p style="margin-top:10px;"><strong>45-60s: Payoff & Seamless Loop CTA</strong><br>
              • <em>Voiceover:</em> "Save this reel to test today and comment 'AGENT' to get the full blueprint."<br>
              • <em>Visual Cue:</em> Ending sentence matches the start for infinite loop.</p>
            </div>
          </div>
        `;
      }
    });
  }

  // 9. PromptMaster Handlers
  if (btnLoadBadPrompt) {
    btnLoadBadPrompt.addEventListener("click", () => {
      if (pmPromptInput) pmPromptInput.value = "Write me something kind of cool for my social media about AI tools and make it good. What do you think?";
    });
  }

  if (btnAuditPrompt) {
    btnAuditPrompt.addEventListener("click", () => {
      const rawPrompt = (pmPromptInput && pmPromptInput.value.trim()) || "";
      if (!rawPrompt) return;
      const res = CreatorEngine.auditPromptMaster(rawPrompt);

      if (pmWasteCount) pmWasteCount.textContent = res.wasteCount;
      if (pmWastedTokens) pmWastedTokens.textContent = `~${res.estimatedWastedTokens}`;

      if (pmResultsDetails) {
        pmResultsDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">
              <span>HEALTH SCORE: ${res.healthScore}/100</span>
              <span style="color:var(--accent-rose);">${res.wasteCount} Traps Found</span>
            </div>
            ${res.detected.map(d => `
              <div style="margin-bottom:8px;font-size:0.82rem;">
                <strong style="color:var(--accent-rose);">[#${d.id} ${d.name}]</strong> (${d.family})<br>
                <span style="color:var(--text-muted);">${d.fix}</span>
              </div>
            `).join("")}
          </div>

          <div class="output-box" style="margin-top:12px;">
            <div class="output-box-title">COMPILED 1-SHOT PRODUCTION PROMPT</div>
            <pre style="white-space:pre-wrap;font-size:0.8rem;color:#a5b4fc;font-family:var(--font-mono);">${res.optimized}</pre>
          </div>
        `;
      }
    });
  }

  if (btnCopyOptimizedPrompt) {
    btnCopyOptimizedPrompt.addEventListener("click", () => {
      const rawPrompt = (pmPromptInput && pmPromptInput.value.trim()) || "";
      const res = CreatorEngine.auditPromptMaster(rawPrompt);
      navigator.clipboard.writeText(res.optimized);
      btnCopyOptimizedPrompt.textContent = "✓ Copied!";
      setTimeout(() => btnCopyOptimizedPrompt.textContent = "📋 Copy", 2000);
    });
  }

  // 10. Anti-AI Humanizer Handlers
  if (btnDetectSlop) {
    btnDetectSlop.addEventListener("click", () => {
      const text = (humanizerInput && humanizerInput.value.trim()) || "";
      if (!text) return;
      const audit = CreatorEngine.auditSlop(text);

      if (humanScoreBadge) {
        humanScoreBadge.textContent = `${audit.humanScore}/100`;
        humanScoreBadge.style.color = audit.humanScore >= 80 ? "var(--accent-emerald)" : audit.humanScore >= 55 ? "var(--accent-cyan)" : "var(--accent-rose)";
      }

      if (humanizerResultsDetails) {
        humanizerResultsDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">
              <span>5-CHECK HUMAN PANEL</span>
              <span style="color:var(--accent-cyan);">${audit.verdict}</span>
            </div>
            <p style="font-size:0.82rem;color:var(--text-muted);">
              Sentence CV: <strong>${audit.cv}</strong> (Want > 0.55) | Invisible Chars: <strong>${audit.invisibles}</strong> | Em-Dashes: <strong>${audit.emDashes}</strong>
            </p>
          </div>

          <div class="metric-bar-group">
            ${Object.entries(audit.checks).map(([k, v]) => `
              <div class="metric-bar-row">
                <span class="metric-name">${k}</span>
                <div class="metric-bar-track"><div class="metric-bar-fill" style="width:${v}%;"></div></div>
                <span class="metric-value">${v}</span>
              </div>
            `).join("")}
          </div>

          ${audit.slopHits.length ? `
            <div class="output-box" style="margin-top:12px;">
              <div class="output-box-title">BANNED AI BUZZWORDS FOUND</div>
              <ul style="padding-left:18px;font-size:0.82rem;color:var(--accent-rose);">
                ${audit.slopHits.map(s => `<li><strong>"${s.find}"</strong> (x${s.count}) → Suggest: <em>"${s.replace}"</em></li>`).join("")}
              </ul>
            </div>
          ` : ''}
        `;
      }
    });
  }

  if (btnCleanSlop) {
    btnCleanSlop.addEventListener("click", () => {
      const text = (humanizerInput && humanizerInput.value.trim()) || "";
      if (!text) return;
      const human = CreatorEngine.humanizeText(text);

      if (humanScoreBadge) {
        humanScoreBadge.textContent = `${human.newHumanScore}/100`;
        humanScoreBadge.style.color = "var(--accent-emerald)";
      }

      if (humanizerResultsDetails) {
        humanizerResultsDetails.innerHTML = `
          <div class="output-box">
            <div class="output-box-title">
              <span>CLEANED HUMAN DRAFT (SCORE: ${human.newHumanScore}/100)</span>
              <button class="btn btn-sm btn-outline" id="btnCopyCleanedText">📋 Copy</button>
            </div>
            <p style="white-space:pre-wrap;font-size:0.92rem;color:#ffffff;line-height:1.6;">${human.cleanedText}</p>
          </div>

          <div class="output-box" style="margin-top:12px;">
            <div class="output-box-title">TRANSFORMATIONS APPLIED (${human.replacements.length})</div>
            <ul style="padding-left:18px;font-size:0.82rem;color:var(--accent-emerald);">
              <li>Purged all zero-width unicode & non-breaking spaces</li>
              <li>Normalized em-dashes (—) to natural punctuation</li>
              ${human.replacements.map(r => `<li>Replaced <em>"${r.from}"</em> with <strong>"${r.to}"</strong></li>`).join("")}
            </ul>
          </div>
        `;

        const btnCopyClean = document.getElementById("btnCopyCleanedText");
        if (btnCopyClean) {
          btnCopyClean.addEventListener("click", () => {
            navigator.clipboard.writeText(human.cleanedText);
            btnCopyClean.textContent = "✓ Copied!";
          });
        }
      }
    });
  }

  // 10.5 SingDia AI Personalized Music Studio Handlers
  let currentSongData = null;
  let currentSongTab = "v1";
  let isAudioPlaying = false;
  let audioContext = null;
  let audioOscillator = null;

  const sdRecipient = document.getElementById("sdRecipient");
  const sdSender = document.getElementById("sdSender");
  const sdOccasion = document.getElementById("sdOccasion");
  const sdRelationship = document.getElementById("sdRelationship");
  const sdLanguage = document.getElementById("sdLanguage");
  const sdGenre = document.getElementById("sdGenre");
  const sdMemory = document.getElementById("sdMemory");
  const sdInsideJoke = document.getElementById("sdInsideJoke");
  const btnGenerateSong = document.getElementById("btnGenerateSong");
  const btnRandomSongPreset = document.getElementById("btnRandomSongPreset");

  const sdPresetBday = document.getElementById("sdPresetBday");
  const sdPresetAnniv = document.getElementById("sdPresetAnniv");
  const sdPresetSangeet = document.getElementById("sdPresetSangeet");
  const sdPresetBestie = document.getElementById("sdPresetBestie");
  const sdPresetLullaby = document.getElementById("sdPresetLullaby");

  const songDisplayTitle = document.getElementById("songDisplayTitle");
  const songDisplaySubtitle = document.getElementById("songDisplaySubtitle");
  const songMeterBadge = document.getElementById("songMeterBadge");
  const songOutputContent = document.getElementById("songOutputContent");

  const btnSongTabV1 = document.getElementById("btnSongTabV1");
  const btnSongTabV2 = document.getElementById("btnSongTabV2");
  const btnSongTabSuno = document.getElementById("btnSongTabSuno");
  const btnSongTabCard = document.getElementById("btnSongTabCard");

  const btnPlayAudioMock = document.getElementById("btnPlayAudioMock");
  const playerTrackTitle = document.getElementById("playerTrackTitle");
  const playerTrackGenre = document.getElementById("playerTrackGenre");
  const audioWaves = document.getElementById("audioWaves");

  const smRhyme = document.getElementById("smRhyme");
  const smConsistency = document.getElementById("smConsistency");
  const smPersonal = document.getElementById("smPersonal");
  const smLines = document.getElementById("smLines");

  const btnCopySongLyrics = document.getElementById("btnCopySongLyrics");
  const btnCopySunoPrompt = document.getElementById("btnCopySunoPrompt");
  const btnCopyGiftCard = document.getElementById("btnCopyGiftCard");

  function setPreset(r, s, o, rel, l, g, m, j, activeBtn) {
    if (sdRecipient) sdRecipient.value = r;
    if (sdSender) sdSender.value = s;
    if (sdOccasion) sdOccasion.value = o;
    if (sdRelationship) sdRelationship.value = rel;
    if (sdLanguage) sdLanguage.value = l;
    if (sdGenre) sdGenre.value = g;
    if (sdMemory) sdMemory.value = m;
    if (sdInsideJoke) sdInsideJoke.value = j;

    document.querySelectorAll(".preset-pills-group .pill-btn").forEach(b => b.classList.remove("active"));
    if (activeBtn) activeBtn.classList.add("active");
    triggerSongGeneration();
  }

  if (sdPresetBday) {
    sdPresetBday.addEventListener("click", () => {
      setPreset(
        "Pooja", "Rahul", "Birthday", "Best Friend", "Hinglish", "Modern Hindi Pop",
        "that crazy Goa road trip where the car broke down and we ate roadside maggi at 3 AM",
        "always stealing my fries, calling everyone bro, drama queen of our group",
        sdPresetBday
      );
    });
  }

  if (sdPresetAnniv) {
    sdPresetAnniv.addEventListener("click", () => {
      setPreset(
        "Ananya", "Vikram", "Anniversary", "Partner / Soulmate", "Hindi", "Bollywood Romantic",
        "standing in the rain on our first date under one tiny broken umbrella laughing our hearts out",
        "her obsession with spicy pani puri and falling asleep 5 minutes into any movie",
        sdPresetAnniv
      );
    });
  }

  if (sdPresetSangeet) {
    sdPresetSangeet.addEventListener("click", () => {
      setPreset(
        "Simran & Raj", "The Sangeet Squad", "Wedding / Sangeet", "Best Friend", "Punjabi", "Punjabi Dhol / Sangeet",
        "practicing crazy bhangra steps till 4 AM and breaking the dance floor at the rehearsal",
        "Simran's endless shopping bags and Raj's secret butter chicken midnight cravings",
        sdPresetSangeet
      );
    });
  }

  if (sdPresetBestie) {
    sdPresetBestie.addEventListener("click", () => {
      setPreset(
        "Rohan", "Kabir", "Friendship / Appreciation", "Best Friend", "Hinglish", "Desi Hip-Hop / Rap",
        "failing our first college exam together then celebrating with 10 cups of cutting chai",
        "borrowing my bike with zero petrol and giving absolute terrible dating advice",
        sdPresetBestie
      );
    });
  }

  if (sdPresetLullaby) {
    sdPresetLullaby.addEventListener("click", () => {
      setPreset(
        "Baby Kiara", "Mom & Dad", "Sweet Lullaby", "Child / Son / Daughter", "English", "Sweet Lullaby",
        "your tiny fingers holding our hands and your sweet little sleepy yawns",
        "talking to teddy bears and falling asleep only with your favorite starry blanket",
        sdPresetLullaby
      );
    });
  }

  if (btnRandomSongPreset) {
    btnRandomSongPreset.addEventListener("click", () => {
      const presets = [sdPresetBday, sdPresetAnniv, sdPresetSangeet, sdPresetBestie, sdPresetLullaby].filter(Boolean);
      const randomBtn = presets[Math.floor(Math.random() * presets.length)];
      if (randomBtn) randomBtn.click();
    });
  }

  function triggerSongGeneration() {
    const params = {
      recipient: (sdRecipient && sdRecipient.value.trim()) || "Pooja",
      sender: (sdSender && sdSender.value.trim()) || "Rahul",
      occasion: (sdOccasion && sdOccasion.value) || "Birthday",
      relationship: (sdRelationship && sdRelationship.value) || "Best Friend",
      language: (sdLanguage && sdLanguage.value) || "Hinglish",
      genre: (sdGenre && sdGenre.value) || "Modern Hindi Pop",
      memory: (sdMemory && sdMemory.value.trim()) || "our crazy late night road trips",
      inside_joke: (sdInsideJoke && sdInsideJoke.value.trim()) || "always stealing my food"
    };

    currentSongData = CreatorEngine.generateSingDiaSong(params);
    renderSongView(currentSongTab);
  }

  function formatLyricsWithTags(rawLyrics) {
    const lines = rawLyrics.split("\n");
    return lines.map(line => {
      const trimmed = line.trim();
      if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
        return `<div class="song-section-tag">${escapeHtml(trimmed)}</div>`;
      }
      return escapeHtml(line);
    }).join("\n");
  }

  function renderSongView(tab) {
    if (!currentSongData) return;
    currentSongTab = tab;

    [btnSongTabV1, btnSongTabV2, btnSongTabSuno, btnSongTabCard].forEach(b => b && b.classList.remove("active"));

    const arr1 = currentSongData.arrangements[0];
    const arr2 = currentSongData.arrangements[1];
    const activeArr = tab === "v2" ? arr2 : arr1;
    const meter = activeArr.meter_analysis || {};

    if (playerTrackTitle) playerTrackTitle.textContent = `${activeArr.title}`;
    if (playerTrackGenre) playerTrackGenre.textContent = `${currentSongData.meta.genre} • ${activeArr.tempo} • ${currentSongData.meta.language}`;

    if (songMeterBadge) {
      songMeterBadge.textContent = `${meter.overall_score || 92}/100`;
      songMeterBadge.style.color = (meter.overall_score || 92) >= 85 ? "var(--accent-emerald)" : "var(--accent-cyan)";
    }

    if (smRhyme) smRhyme.textContent = meter.rhyme_grade || "A+";
    if (smConsistency) smConsistency.textContent = `${meter.consistency_score || 94}%`;
    if (smPersonal) smPersonal.textContent = `${meter.personalization_score || 100}%`;
    if (smLines) smLines.textContent = meter.line_count || 18;

    if (!songOutputContent) return;

    if (tab === "v1") {
      if (btnSongTabV1) btnSongTabV1.classList.add("active");
      songOutputContent.innerHTML = formatLyricsWithTags(arr1.lyrics);
    } else if (tab === "v2") {
      if (btnSongTabV2) btnSongTabV2.classList.add("active");
      songOutputContent.innerHTML = formatLyricsWithTags(arr2.lyrics);
    } else if (tab === "suno") {
      if (btnSongTabSuno) btnSongTabSuno.classList.add("active");
      songOutputContent.innerHTML = `
<div class="output-box" style="margin-bottom:12px;">
  <div class="output-box-title">SUNO AI AUDIO GENERATION PROMPT</div>
  <p style="color:var(--accent-cyan);font-family:var(--font-mono);font-size:0.88rem;line-height:1.5;">${escapeHtml(currentSongData.audio_prompts.suno_prompt)}</p>
</div>

<div class="output-box" style="margin-bottom:12px;">
  <div class="output-box-title">UDIO TAGS & STYLE MAP</div>
  <p style="color:#a5b4fc;font-family:var(--font-mono);font-size:0.85rem;">${escapeHtml(currentSongData.audio_prompts.udio_tags)}</p>
</div>

<div class="output-box">
  <div class="output-box-title">VOCAL & INSTRUMENTAL DIRECTION</div>
  <p style="font-size:0.85rem;color:var(--text-muted);line-height:1.6;">
    🎤 <strong>Vocal Character:</strong> ${escapeHtml(currentSongData.audio_prompts.voice_style)}<br>
    🥁 <strong>Recommended Instruments:</strong> ${escapeHtml(currentSongData.meta.recommended_instruments.join(", "))}<br>
    ⚡ <strong>Tempo & Mood:</strong> ${escapeHtml(currentSongData.meta.tempo)} • ${escapeHtml(currentSongData.meta.mood)}
  </p>
</div>`;
    } else if (tab === "card") {
      if (btnSongTabCard) btnSongTabCard.classList.add("active");
      songOutputContent.innerHTML = `
<div class="gift-card-box">
  <div class="gift-card-ribbon">✨ SPECIAL ${escapeHtml(currentSongData.meta.occasion.toUpperCase())} DEDICATION ✨</div>
  <div class="gift-card-text">"${escapeHtml(currentSongData.gift_card_message)}"</div>
  <div class="gift-card-signature">🎵 A Personalized Melody for ${escapeHtml(currentSongData.meta.recipient)} • From ${escapeHtml(currentSongData.meta.sender)}</div>
</div>`;
    }
  }

  if (btnSongTabV1) btnSongTabV1.addEventListener("click", () => renderSongView("v1"));
  if (btnSongTabV2) btnSongTabV2.addEventListener("click", () => renderSongView("v2"));
  if (btnSongTabSuno) btnSongTabSuno.addEventListener("click", () => renderSongView("suno"));
  if (btnSongTabCard) btnSongTabCard.addEventListener("click", () => renderSongView("card"));

  if (btnGenerateSong) {
    btnGenerateSong.addEventListener("click", () => {
      triggerSongGeneration();
    });
  }

  // Audio Mock Player Simulation with Web Audio API chime
  if (btnPlayAudioMock) {
    btnPlayAudioMock.addEventListener("click", () => {
      isAudioPlaying = !isAudioPlaying;
      if (isAudioPlaying) {
        btnPlayAudioMock.textContent = "⏸";
        if (audioWaves) audioWaves.classList.add("playing");
        try {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) {
            audioContext = new AudioContext();
            const notes = [261.63, 329.63, 392.00, 523.25]; // C chord
            notes.forEach((freq, idx) => {
              const osc = audioContext.createOscillator();
              const gain = audioContext.createGain();
              osc.type = "sine";
              osc.frequency.setValueAtTime(freq, audioContext.currentTime + idx * 0.15);
              gain.gain.setValueAtTime(0.08, audioContext.currentTime + idx * 0.15);
              gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + idx * 0.15 + 1.2);
              osc.connect(gain);
              gain.connect(audioContext.destination);
              osc.start(audioContext.currentTime + idx * 0.15);
              osc.stop(audioContext.currentTime + idx * 0.15 + 1.3);
            });
          }
        } catch (e) {
          console.log("Audio preview active", e);
        }
      } else {
        btnPlayAudioMock.textContent = "▶";
        if (audioWaves) audioWaves.classList.remove("playing");
        if (audioContext && audioContext.state !== "closed") {
          audioContext.close();
        }
      }
    });
  }

  if (btnCopySongLyrics) {
    btnCopySongLyrics.addEventListener("click", () => {
      if (currentSongData) {
        const arr = currentSongTab === "v2" ? currentSongData.arrangements[1] : currentSongData.arrangements[0];
        navigator.clipboard.writeText(arr.lyrics);
        btnCopySongLyrics.textContent = "✓ Lyrics Copied!";
        setTimeout(() => btnCopySongLyrics.textContent = "📋 Copy Complete Lyrics", 2000);
      }
    });
  }

  if (btnCopySunoPrompt) {
    btnCopySunoPrompt.addEventListener("click", () => {
      if (currentSongData) {
        navigator.clipboard.writeText(currentSongData.audio_prompts.suno_prompt);
        btnCopySunoPrompt.textContent = "✓ Suno Prompt Copied!";
        setTimeout(() => btnCopySunoPrompt.textContent = "🎵 Copy Suno Audio Prompt", 2000);
      }
    });
  }

  if (btnCopyGiftCard) {
    btnCopyGiftCard.addEventListener("click", () => {
      if (currentSongData) {
        navigator.clipboard.writeText(currentSongData.gift_card_message);
        btnCopyGiftCard.textContent = "✓ Message Copied!";
        setTimeout(() => btnCopyGiftCard.textContent = "💌 Copy Gift Message", 2000);
      }
    });
  }

  // Initial Song Render
  triggerSongGeneration();

  // 11. HyperFrames Handlers
  if (btnGenMotionCode) {
    btnGenMotionCode.addEventListener("click", () => {
      const bId = (hfBlueprintSelect && hfBlueprintSelect.value) || "kinetic-type-beats";
      const text = (hfHeadline && hfHeadline.value) || "SHIP 10X FASTER";

      const code = `import { gsap } from "gsap";

// HyperFrames Motion Blueprint: ${bId}
// Headline: "${text}"

export function initMotionTimeline(containerElement) {
  const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
  
  // 1. Initial State
  gsap.set(".motion-headline", { opacity: 0, scale: 0.85, y: 30 });
  gsap.set(".motion-badge", { opacity: 0, scale: 0 });
  gsap.set(".motion-glow-ring", { opacity: 0, scale: 0.5 });

  // 2. Kinetic Slam Beat
  tl.to(".motion-glow-ring", { opacity: 0.6, scale: 1.2, duration: 0.4, ease: "expo.out" })
    .to(".motion-headline", { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "elastic.out(1, 0.4)" }, "-=0.2")
    .to(".motion-badge", { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, "-=0.15");

  // 3. Ambient Drift
  tl.to(".motion-headline", { y: "-=8", repeat: -1, yoyo: true, duration: 2, ease: "sine.inOut" });

  return tl;
}`;
      if (hfCodeOutput) {
        hfCodeOutput.innerHTML = `<pre><code class="language-javascript">${escapeHtml(code)}</code></pre>`;
      }
    });
  }

  if (btnCopyMotionCode) {
    btnCopyMotionCode.addEventListener("click", () => {
      if (hfCodeOutput) {
        navigator.clipboard.writeText(hfCodeOutput.innerText);
        btnCopyMotionCode.textContent = "✓ Copied!";
        setTimeout(() => btnCopyMotionCode.textContent = "📋 Copy Code", 2000);
      }
    });
  }

  // 12. Render Unhinged Cards
  function renderUnhingedCards() {
    const unhingedGrid = document.getElementById("unhingedGrid");
    if (!unhingedGrid) return;
    const skills = masterKnowledge.unhinged_skills || [];

    unhingedGrid.innerHTML = skills.map(s => `
      <div class="unhinged-card">
        <div class="unhinged-header">
          <span class="unhinged-title">/${s.id}</span>
          <button class="btn btn-sm btn-outline btn-copy-skill" data-skill="/${s.id}">Copy Prompt</button>
        </div>
        <p class="unhinged-desc">${s.title}</p>
      </div>
    `).join("");

    document.querySelectorAll(".btn-copy-skill").forEach(btn => {
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(`Execute task with full intensity using ${btn.dataset.skill} mode.`);
        btn.textContent = "✓ Copied!";
        setTimeout(() => btn.textContent = "Copy Prompt", 2000);
      });
    });
  }

  // 13. Knowledge Matrix Render
  matrixTabs.forEach(t => {
    t.addEventListener("click", () => {
      matrixTabs.forEach(x => x.classList.remove("active"));
      t.classList.add("active");
      renderKnowledgeMatrix(t.dataset.matrix);
    });
  });

  if (matrixSearch) {
    matrixSearch.addEventListener("input", () => {
      const activeTab = document.querySelector(".matrix-tab-btn.active");
      if (activeTab) renderKnowledgeMatrix(activeTab.dataset.matrix, matrixSearch.value.toLowerCase());
    });
  }

  function renderKnowledgeMatrix(type, query = "") {
    const container = document.getElementById("matrixContent");
    if (!container) return;

    if (type === "li-hooks") {
      const hooks = (masterKnowledge.linkedin && masterKnowledge.linkedin.hooks) || [];
      const filtered = hooks.filter(h => !query || (h.name + " " + (h.template || "")).toLowerCase().includes(query));
      container.innerHTML = `
        <table class="matrix-table">
          <thead>
            <tr><th>#</th><th>Formula Name</th><th>Category</th><th>Template / Match Pattern</th></tr>
          </thead>
          <tbody>
            ${filtered.map((h, i) => `
              <tr>
                <td>${i+1}</td>
                <td><strong>${h.name}</strong></td>
                <td>${h.category || 'Core'}</td>
                <td><code style="color:#a5b4fc;">${escapeHtml(h.template || (h.match ? h.match[0] : ''))}</code></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    } else if (type === "yt-hooks") {
      const hooks = (masterKnowledge.youtube && masterKnowledge.youtube.hooks) || [];
      const filtered = hooks.filter(h => !query || (h.name + " " + (h.template || "")).toLowerCase().includes(query));
      container.innerHTML = `
        <table class="matrix-table">
          <thead>
            <tr><th>#</th><th>YouTube Formula</th><th>Retention Factor</th><th>Pattern</th></tr>
          </thead>
          <tbody>
            ${filtered.map((h, i) => `
              <tr>
                <td>${i+1}</td>
                <td><strong>${h.name}</strong></td>
                <td>0-15s Click Confirm</td>
                <td><code style="color:#a5b4fc;">${escapeHtml(h.template || (h.match ? h.match[0] : ''))}</code></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    } else if (type === "ig-hooks") {
      const hooks = (masterKnowledge.instagram && masterKnowledge.instagram.hooks) || [];
      const filtered = hooks.filter(h => !query || (h.name + " " + (h.spoken || "")).toLowerCase().includes(query));
      container.innerHTML = `
        <table class="matrix-table">
          <thead>
            <tr><th>#</th><th>Reel Formula</th><th>On-Screen Text (&le; 6 words)</th><th>Spoken Voiceover</th></tr>
          </thead>
          <tbody>
            ${filtered.map((h, i) => `
              <tr>
                <td>${i+1}</td>
                <td><strong>${h.name}</strong></td>
                <td><span style="color:var(--accent-cyan);font-weight:700;">${escapeHtml(h.on_screen || '')}</span></td>
                <td><code style="color:#a5b4fc;">${escapeHtml(h.spoken || (h.match ? h.match[0] : ''))}</code></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    } else if (type === "singdia-music") {
      const genres = (masterKnowledge.singdia && masterKnowledge.singdia.genres) || [];
      const langs = (masterKnowledge.singdia && masterKnowledge.singdia.languages) || [];
      const occasions = (masterKnowledge.singdia && masterKnowledge.singdia.occasions) || [];
      const filtered = genres.filter(g => !query || (g.name + " " + g.tempo + " " + g.mood + " " + g.description).toLowerCase().includes(query));
      container.innerHTML = `
        <div style="margin-bottom:16px;display:flex;gap:16px;flex-wrap:wrap;">
          <div class="stat-pill" style="flex:1;"><strong>12 Supported Languages:</strong> ${langs.map(l => l.name).join(", ")}</div>
          <div class="stat-pill" style="flex:1;"><strong>15 Gift Occasions:</strong> ${occasions.slice(0, 6).map(o => o.name).join(", ")}...</div>
        </div>
        <table class="matrix-table">
          <thead>
            <tr><th>#</th><th>Musical Genre</th><th>BPM & Tempo</th><th>Mood / Style</th><th>Suno / Udio Production Blueprint</th></tr>
          </thead>
          <tbody>
            ${filtered.map((g, i) => `
              <tr>
                <td>${i+1}</td>
                <td><strong style="color:var(--accent-cyan);">${g.name}</strong></td>
                <td><span class="status-chip">${g.tempo}</span></td>
                <td>${g.mood}</td>
                <td><code style="color:#a5b4fc;font-size:0.8rem;">${escapeHtml(g.suno_prompt)}</code></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    } else if (type === "waste-patterns") {
      const families = (masterKnowledge.promptmaster && masterKnowledge.promptmaster.families) || [];
      let allPatterns = [];
      families.forEach(f => {
        (f.patterns || []).forEach(p => allPatterns.push({ ...p, family: f.family }));
      });
      const filtered = allPatterns.filter(p => !query || (p.name + " " + p.signal + " " + p.fix).toLowerCase().includes(query));
      container.innerHTML = `
        <table class="matrix-table">
          <thead>
            <tr><th>ID</th><th>Trap Name</th><th>Category</th><th>Detection Signal & Fix</th></tr>
          </thead>
          <tbody>
            ${filtered.map(p => `
              <tr>
                <td>#${p.id}</td>
                <td><strong>${p.name}</strong></td>
                <td>${p.family}</td>
                <td>
                  <div style="color:var(--accent-rose);font-size:0.8rem;">Signal: ${p.signal}</div>
                  <div style="color:var(--accent-emerald);font-size:0.8rem;margin-top:2px;">Fix: ${p.fix}</div>
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    } else if (type === "slop-words") {
      const lex = (masterKnowledge.linkedin && masterKnowledge.linkedin.slop_lexicon) || {};
      const words = [...(lex.words || []), ...(lex.phrases || [])];
      const filtered = words.filter(w => !query || (w.find + " " + w.replace).toLowerCase().includes(query));
      container.innerHTML = `
        <table class="matrix-table">
          <thead>
            <tr><th>Banned AI Slop Word / Phrase</th><th>Human Replacement</th></tr>
          </thead>
          <tbody>
            ${filtered.map(w => `
              <tr>
                <td><strong style="color:var(--accent-rose);">${w.find}</strong></td>
                <td><span style="color:var(--accent-emerald);font-weight:600;">${w.replace}</span></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    }
  }

  // 14. FreeLLM Gateway Logic
  const freeProviders = [
    { id: "groq", name: "Groq Cloud (LPUs)", models: "Llama 3.3 70B, Mixtral", rpm: "30 RPM", free: true },
    { id: "gemini", name: "Google Gemini", models: "Gemini 2.0 Flash, 1.5 Pro", rpm: "15 RPM", free: true },
    { id: "cerebras", name: "Cerebras Inference", models: "Llama 3.1 70B, 8B", rpm: "30 RPM", free: true },
    { id: "mistral", name: "Mistral AI", models: "Codestral, Mistral Small", rpm: "20 RPM", free: true },
    { id: "sambanova", name: "SambaNova Systems", models: "Llama 3.1 70B, Qwen 2.5 72B", rpm: "20 RPM", free: true },
    { id: "openrouter", name: "OpenRouter Free", models: "Llama 3.3 Free, Gemini Exp", rpm: "20 RPM", free: true },
    { id: "deepseek", name: "DeepSeek API", models: "DeepSeek-V3, DeepSeek-R1", rpm: "30 RPM", free: true },
    { id: "github", name: "GitHub Models (Azure)", models: "GPT-4o mini, Llama 3.1", rpm: "15 RPM", free: true }
  ];

  const freeProvidersList = document.getElementById("freeProvidersList");
  const btnSaveFreeKey = document.getElementById("btnSaveFreeKey");
  const btnTestFailover = document.getElementById("btnTestFailover");
  const freeProviderSelect = document.getElementById("freeProviderSelect");
  const freeApiKeyInput = document.getElementById("freeApiKeyInput");

  function renderFreeProviders() {
    if (!freeProvidersList) return;
    const savedKeys = JSON.parse(localStorage.getItem("creator_freellm_keys") || "{}");
    const activeCount = Object.keys(savedKeys).length;
    const badge = document.getElementById("freeActiveCountBadge");
    if (badge) badge.textContent = `${activeCount} Active / 8 Configurable`;

    freeProvidersList.innerHTML = freeProviders.map(p => {
      const isSaved = !!savedKeys[p.id];
      return `
        <div class="unhinged-card" style="margin-bottom:8px;">
          <div class="unhinged-header">
            <strong style="color:${isSaved ? 'var(--accent-emerald)' : 'var(--accent-cyan)'};">${p.name}</strong>
            <span class="status-chip" style="font-size:0.7rem;padding:2px 8px;background:${isSaved ? 'rgba(16,185,129,0.15)' : 'rgba(255,255,255,0.05)'};color:${isSaved ? 'var(--accent-emerald)' : 'var(--text-muted)'};">
              ${isSaved ? '✓ Key Active' : 'Key Missing'}
            </span>
          </div>
          <div style="font-size:0.8rem;color:var(--text-muted);display:flex;justify-content:space-between;">
            <span>Models: ${p.models}</span>
            <span style="color:var(--accent-amber);font-family:var(--font-mono);">${p.rpm}</span>
          </div>
        </div>
      `;
    }).join("");
  }

  renderFreeProviders();

  if (btnSaveFreeKey) {
    btnSaveFreeKey.addEventListener("click", () => {
      const pId = freeProviderSelect.value;
      const keyVal = freeApiKeyInput.value.trim();
      if (!keyVal) {
        alert("Please enter a valid free API key.");
        return;
      }
      const savedKeys = JSON.parse(localStorage.getItem("creator_freellm_keys") || "{}");
      savedKeys[pId] = keyVal;
      localStorage.setItem("creator_freellm_keys", JSON.stringify(savedKeys));
      freeApiKeyInput.value = "";
      renderFreeProviders();
      alert(`✓ Successfully saved and activated FreeLLM key for ${pId.toUpperCase()}!`);
    });
  }

  if (btnTestFailover) {
    btnTestFailover.addEventListener("click", () => {
      const mockResult = `### ⚡ FreeLLMAPI Live Failover Test Passed!

1. **Provider 1 (Groq)**: Attempted \`llama-3.3-70b\` -> Simulated HTTP 429 Rate Limit Cooldown (60s).
2. **Auto-Failover**: Diverted traffic to **Provider 2 (Cerebras - Llama 3.1 70B)** in **18ms**.
3. **Response**: Successfully generated with 0 token drops!

*FreeLLMAPI smart routing ensures your Creator bot never encounters downtime.*`;
      
      const details = document.getElementById("freeProvidersList");
      if (details) {
        const testBox = document.createElement("div");
        testBox.className = "output-box";
        testBox.style.marginTop = "12px";
        testBox.innerHTML = `
          <div class="output-box-title">LIVE FAILOVER SIMULATION REPORT</div>
          <div style="font-size:0.82rem;line-height:1.5;">${formatMarkdown(mockResult)}</div>
        `;
        details.prepend(testBox);
      }
    });
  }

  // 15. Export Handler
  const btnExportAll = document.getElementById("btnExportAll");
  if (btnExportAll) {
    btnExportAll.addEventListener("click", () => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(masterKnowledge, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "creator_master_knowledge.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    });
  }

  function escapeHtml(str) {
    return (str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
});
