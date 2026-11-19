/* Hack Kit site — vanilla JS, no dependencies, no network calls. */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Safe element builder: text only, never parses HTML from data. */
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function code(text) { return el("code", null, text); }

  /* ---------------- DATA ---------------- */
  var PHASES = [
    { act: "find", cmd: "start", icon: "📜", title: "Read the brief like a judge",
      tag: "Before anyone falls in love with an idea.",
      does: ["Picks an event profile: type, length, team experience, judging focus", "Fetches or reads the brief and pulls out the rubric, rules and deliverables", "Sets the depth of every later command, the captain and freeze times"],
      asks: ["Event type", "Rubric & weights", "Event length", "Team experience"], writes: ["BRIEF.md", "STATE.md"], time: "5 min" },
    { act: "find", cmd: "decode", icon: "🔍", title: "Understand every statement",
      tag: "In 2 minutes each, with the angle most teams miss.",
      does: ["Real problem, severity, frequency and who's affected", "End user, operator and least-digital user", "Hidden constraints and the root cause", "Obvious idea vs smarter angle"],
      asks: ["Paste statements", "Organiser hints", "Drop any now?"], writes: ["STATEMENTS.md"], time: "15 min" },
    { act: "find", cmd: "pick", icon: "⚖️", trial: true, title: "Choose the problem worth your weekend",
      tag: "Rubric-weighted scoring, red flags, then a trial.",
      does: ["Scores statements on 8 weighted criteria, with certainty marks", "Flags hardware, data, safety and 'already solved' risks", "Runs Hack Court on the top 2–3 problems", "The captain decides; rejected options are logged"],
      asks: ["Confirm shortlist", "Final pick"], writes: ["PICK.md", "court/"], time: "15 min" },
    { act: "shape", cmd: "users", icon: "🧭", title: "Think as every real user",
      tag: "Especially the one most likely to be left out.",
      does: ["One card per stakeholder: today, worst step, refusals, adoption trigger", "POV, How-Might-We, job story and persona", "Contrast motto options", "Untested beliefs about users go to ASSUMPTIONS.md"],
      asks: ["Who are the users?", "Personal experience?", "Pick the motto"], writes: ["USERS.md", "ASSUMPTIONS.md"], time: "10 min" },
    { act: "shape", cmd: "ideate", icon: "💡", title: "Think deeper before you commit",
      tag: "Six genuinely different directions, not fifty random ideas.",
      does: ["Five Whys and today's workaround", "User, process, access, integration, prevention and technology shifts", "Constraint removal: no AI? no app? solve 10% exceptionally well?", "Scores the trade-offs; the team picks; rejected ideas are logged"],
      asks: ["Pick one", "Combine two", "Your own idea"], writes: ["IDEAS.md", "ASSUMPTIONS.md"], time: "15 min" },
    { act: "shape", cmd: "validate", icon: "📰", title: "Prove it's real",
      tag: "Labelled evidence and real experiments.",
      does: ["Sources opened and labelled [V]; everything else stays [AI] or [?]", "Real complaints and a local example", "Experiment cards for the riskiest assumptions", "A 5-minute Mom-Test venue interview script"],
      asks: ["Talked to anyone yet?", "Add results"], writes: ["EVIDENCE.md", "ASSUMPTIONS.md"], time: "20 min", parallel: true },
    { act: "shape", cmd: "compete", icon: "🗺️", title: "Know what already exists",
      tag: "Honest positioning. Never 'no competitors'.",
      does: ["6–10 existing solutions, including government portals and past projects", "What exists, what it fails to solve, what's left", "A differentiation statement based on user value", "Coexistence levels L0–L3"],
      asks: ["Known competitors?", "System to work alongside?"], writes: ["COMPETE.md"], time: "20 min", parallel: true },
    { act: "shape", cmd: "stress", icon: "🥊", title: "Attack it before the judges do",
      tag: "Stands in for the domain expert you don't have.",
      does: ["Drafts CORE v1 from the chosen idea", "Role-plays the expert, front-line worker, least-digital user, sceptic and admin", "Failure scenarios: no internet, API down, wrong AI answer", "A doubt table with the smallest fix for each"],
      asks: ["Real-people check?"], writes: ["STRESS.md", "CORE.md v1"], time: "15 min" },
    { act: "shape", cmd: "improve", icon: "↺", title: "Challenge harder, then make it better",
      tag: "Criticism only counts if the idea improves.",
      does: ["Turns doubts or a verdict into concrete changes, with reasons", "Guardrail: the problem and main user never change", "The team accepts or rejects each change", "CORE v1 → v2, compared, then a quick re-trial"],
      asks: ["Which changes to accept?"], writes: ["IMPROVE.md", "CORE.md v2"], time: "15 min" },
    { act: "shape", cmd: "lock", icon: "🔒", title: "Freeze the core",
      tag: "Problem, user, journey and motto are protected.",
      does: ["Completes CORE.md: journey, who does what, USPs, AI vs rules vs humans", "Warns about any open 'collapses' assumption", "Mistakes check, then LOCKED", "Details can still improve through /hack:improve"],
      asks: ["Lock it?"], writes: ["CORE.md 🔒"], time: "10 min" },
    { act: "build", cmd: "plan", icon: "🛠️", title: "One journey, built for real",
      tag: "One wow moment. Mock the rest and say so.",
      does: ["Build / Mock / Cut for every feature", "Stack with a reason and a fallback for each layer", "Team-aware tasks: owners, skills, critical path, overload check", "Failure scenarios, 90-second demo script and AI test cases"],
      asks: ["Fastest stack", "Hours left", "Sponsor API", "Team skills"], writes: ["PLAN.md"], time: "20 min" },
    { act: "build", cmd: "verify", icon: "⚖️", trial: true, title: "Put the solution on trial",
      tag: "Find the weak spots while there's still time.",
      does: ["Hack Court on the planned solution", "Rubric estimate out of 100", "Mistakes, claims and assumptions checks", "--demo: Demo Day Court on what you built (planned → built → tested → shown)"],
      asks: ["Improve now?", "Which fixes?"], writes: ["VERDICT.md", "DEMO.md", "court/"], time: "15 min" },
    { act: "build", cmd: "pitch", icon: "🎤", title: "Say it so judges remember it",
      tag: "Within the slide limit; only real evidence as facts.",
      does: ["One-line pitch and an opening line for the top rubric item", "Deck outline with a full-sentence headline per slide", "Form answers within word limits", "--drill: a simulated judging panel asks hard questions, one at a time"],
      asks: ["Slide limit", "Pitch length", "Form questions"], writes: ["PITCH.md"], time: "25 min" },
    { act: "build", cmd: "ship", icon: "📄", title: "One Idea Pack",
      tag: "Everything compiled into one document.",
      does: ["A one-page SUMMARY.md", "Joins every file, with a cover and contents", "Outputs FINAL.md, FINAL.html and FINAL.pdf"],
      asks: ["PDF, Markdown or both?"], writes: ["SUMMARY.md", "FINAL.pdf"], time: "5 min" },
    { act: "build", cmd: "retro", icon: "📊", title: "Learn from the run",
      tag: "Compare what you believed with what actually happened.",
      does: ["Compares planned, built, tested and shown features", "Links untested assumptions, jury reasons and pitch claims to what happened", "Only draws lessons the project files support; says so when there's no evidence", "Writes RETRO.md into .hackathon/"],
      asks: ["What did the real judges say?", "Biggest surprise?"], writes: ["RETRO.md"], time: "15 min" }
  ];
  var ACTS = { find: "🔍 Find it", shape: "🧭 Shape it", build: "🚀 Build & sell it" };

  var JURORS = [
    ["🧑", "Actual end user", "NG", "I'd check in by voice while waiting anyway."],
    ["👵", "Least-digital user", "NG", "A normal phone call works for me."],
    ["🩺", "Front-line worker", "G", "Entering vitals by token adds a step in rush hour."],
    ["👨‍⚕️", "Senior doctor", "NG", "I still approve every test. My time is saved."],
    ["🏥", "Hospital administrator", "IE", "Can't tell if it fits our software. Need the integration plan."],
    ["🔎", "Root-cause analyst", "NG", "It hits report-only return visits."],
    ["📚", "'Already exists' researcher", "NG", "Voice check-in in the patient's own words is new."],
    ["🛡️", "Safety reviewer", "NG", "Red flags use fixed rules, not AI."],
    ["🔐", "Patient privacy officer", "NG", "Audio deleted in 72 h; consent is spoken."],
    ["⚙️", "Engineer", "NG", "One journey is buildable in 24 h."],
    ["🏛️", "Statement owner", "NG", "It answers the track directly."],
    ["🤨", "Sceptic", "G", "The impact numbers are still targets."]
  ];
  var RATINGS = [["Problem is real", 9], ["Problem matters", 9], ["Fits root cause", 8], ["Works for real users", 7],
    ["Fits existing systems", 8], ["Safe", 8], ["Buildable & demo-able", 7], ["Different", 7]];

  var RULES = [
    ["Read the brief like a judge", "Rubric weights decide everything. Score against the real rubric, not your own taste."],
    ["Problem, not technology", "\"We want to use AI\" is not a problem. Start from who suffers, and how."],
    ["Every real user", "End user, least-digital user, front-line staff, professional, manager. Think as each one."],
    ["Prove it's real", "Sourced numbers, real complaints, a local example, and chats at the venue."],
    ["Check what exists", "\"Nobody has done this\" is almost always false. Position honestly."],
    ["Stress-test it", "Role-play the domain expert and the sceptic, then confirm with 2–3 real people."],
    ["Lock the core", "Problem, user, journey and motto are protected. Details can still improve."],
    ["Fit existing systems", "No new hardware. Work alongside the software and process people already have."],
    ["Simple for the user", "No app download, no typing, works on the simplest device they own."],
    ["AI suggests, humans decide", "Safety-critical checks use fixed rules. Every AI step has a human check."],
    ["One full journey", "The MVP is one complete journey with one wow moment. Every feature needs a reason."],
    ["No unlabelled numbers", "Every number carries a label. Targets are labelled as targets."],
    ["Simple English", "Short sentences. Explain it the way you'd tell a friend."],
    ["Evidence before confidence", "A confident AI answer is still [AI]. Only verified or team evidence counts as proof."],
    ["Riskiest assumption first", "If it being false would collapse the idea, test it before anything else."],
    ["Tech isn't innovation", "Swapping in a newer model isn't a difference. Be better for the user."],
    ["Keep the history", "Record what was chosen, what was rejected, and why."]
  ];
  var TIMELINE = [
    ["0:00", "/hack:start", "Fill in the brief, ideally before the statements drop."],
    ["0:05", "/hack:decode", "Paste the statements and decode every one."],
    ["0:20", "/hack:pick", "Choose the problem with a trial. The captain decides."],
    ["0:35", "/hack:users → /hack:ideate", "Persona and motto, then six different directions. Pick one."],
    ["0:55", "validate ‖ compete", "Split the team, and test the riskiest assumption with real people."],
    ["1:15", "/hack:stress → /hack:improve", "Attack the idea, then make CORE v2 with the team."],
    ["~1:40", "/hack:lock 🔒", "Idea freeze. From here, you build.", true],
    ["1:50", "/hack:plan → /hack:verify", "One journey, then a trial of the solution."],
    ["−6 h", "/hack:verify --demo", "Demo Day Court on the built product, then fix what fits."],
    ["−4 h", "Code freeze", "Record the backup demo video.", true],
    ["Before judging", "/hack:pitch --drill → /hack:ship", "Deck, Q&A practice with simulated judges, and FINAL.pdf."]
  ];
  var TREE = [
    ["d", ".hackathon/"], ["f", "├── STATE.md", "phases, decisions, locked items"], ["f", "├── BRIEF.md", "rubric, limits, team"],
    ["f", "├── STATEMENTS.md", "every statement decoded"], ["f", "├── PICK.md", "chosen problem + trial"], ["f", "├── USERS.md", "persona, motto"],
    ["f", "├── IDEAS.md", "💡 directions, scores, rejected", true], ["f", "├── ASSUMPTIONS.md", "kill test, status", true],
    ["f", "├── EVIDENCE.md", "labelled evidence, experiments"], ["f", "├── COMPETE.md", "differentiation"], ["f", "├── STRESS.md", "doubts, failure scenarios"],
    ["f", "├── IMPROVE.md", "↺ v1 → v2", true], ["f", "├── CORE.md", "🔒 the locked idea", true], ["f", "├── PLAN.md", "MVP, demo script"],
    ["f", "├── VERDICT.md", "trial + rubric estimate"], ["f", "├── PITCH.md", "deck + Q&A"],
    ["f", "├── RETRO.md", "post-hackathon learnings", true], ["f", "├── FINAL.pdf", "📄 everything", true],
    ["d", "├── history/", "earlier versions"], ["d", "└── court/", "trials + raw votes"]
  ];
  var PROMPT = "You are my hackathon thinking partner. Think deeper, challenge harder, build smarter. Run the Hack Kit process with me one phase at a time, and keep a running \"Idea Pack\" summary after each phase.\n\nPhases: start (brief, rubric, event type and length, team size and experience, judging focus, time) → decode (each statement: real problem, severity, end user, least-digital user, hidden constraints, root cause) → pick (choose the problem: weighted scoring + red flags + trial of the top 2–3) → users (stakeholder views, POV, persona, motto) → ideate (6 directions: user, process, access, integration, prevention and technology shift, plus constraint removal like \"no AI / no app / solve 10% exceptionally well\"; score the trade-offs and let me pick) → validate (labelled evidence, real complaints, experiment cards for the riskiest assumptions, a venue interview script) → compete (what exists, what it fails to solve, a differentiation statement based on user value) → stress (role-play the domain expert, front-line worker, least-digital user, sceptic and admin; failure scenarios) → improve (turn feedback into a better version, with reasons, without changing the problem or main user; I approve each change) → lock (protect the problem, user, journey and motto) → plan (one-journey MVP, build/mock/cut, stack, fallbacks, demo script) → verify (trial of the solution + rubric estimate + claims check; after building, a demo check: what was planned, built, tested and shown, with honest mock disclosures) → pitch (deck outline within the slide limit, form answers, judge Q&A; then a drill where you play 3 judges and ask me hard questions one at a time) → ship (one final document). After the event: retro (what we planned vs built vs showed, and lessons only where our files show evidence). Anytime: assumptions (what we believe but haven't proven; kill test: \"if this is false, does the idea collapse?\").\n\nRules: label every claim [V] verified source, [T] from me/team, [AI] your inference, or [?] unknown. Only [V] and [T] can validate an assumption, and never invent interviews or results. Judge only whether the problem is real and the solution solves it for real users, never business viability. AI suggests, humans decide. No app, no typing, works for the least-digital user. Different technology isn't innovation. Keep a log of rejected ideas and why. Ask me questions with numbered options when my answer matters. Simple English.\n\nTrial = labelled evidence pack → prosecution 5 points → defense 5 points → 12 jurors (end user, least-digital user, front-line worker, domain professional, workaround user, root-cause analyst, already-exists researcher, safety reviewer, systems person, engineer, statement owner, sceptic; for a known domain, swap 3 for domain experts). Each juror votes GUILTY, NOT GUILTY or INSUFFICIENT EVIDENCE, with confidence 1–10, evidence strength, reason, weakest assumption, missing info, and one fix rated for impact and effort. The judge decides: INCONCLUSIVE if under 2/3 valid votes or more than 1/3 insufficient; FAIL if GUILTY outnumbers NOT GUILTY; PASS if NOT GUILTY is at least 75% of all valid votes with mostly solid evidence; otherwise REVISE. Then give contradictions, ratings /10, what's strong, the weakest assumption, what we're overlooking, an alternative approach, ranked improvements, and the next 30-minute experiment. Jurors are simulated perspectives, not real people.\n\nStart with phase \"start\": ask me about the event.";

  /* ---------------- UTIL ---------------- */
  var toastEl = $("#toast"), toastT;
  function toast(msg) {
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  }
  function copyText(text, btn) {
    function ok() { toast("Copied ✓"); if (btn) { btn.classList.add("done"); btn.textContent = "copied"; setTimeout(function () { btn.classList.remove("done"); btn.textContent = "copy"; }, 1600); } }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(ok, function () { fallback(); });
    } else fallback();
    function fallback() {
      var ta = el("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.className = "sr-copy";
      ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); ok(); } catch (e) { toast("Press Ctrl+C to copy"); }
      document.body.removeChild(ta);
    }
  }
  $$("[data-copy],[data-copy-from]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-copy");
      if (!t) { var src = document.getElementById(b.getAttribute("data-copy-from")); t = src ? src.textContent : ""; }
      copyText(t, b);
    });
  });
  $("#promptText").textContent = PROMPT;

  /* nav shadow + progress + active link */
  var nav = $("#nav"), prog = $("#progress"), links = $$(".nav nav a");
  function onScroll() {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle("scrolled", y > 10);
    prog.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
    var cur = null;
    links.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s && s.getBoundingClientRect().top < 140) cur = a; });
    links.forEach(function (a) { a.classList.toggle("active", a === cur); });
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* typed terminal line */
  var typedEl = $("#typed"), cmds = ["/hack:start", "/hack:decode", "/hack:pick --quick", "/hack:lock", "/hack:verify --demo", "/hack:pitch --drill", "/hack:ship", "/hack:retro"];
  if (reduce) typedEl.textContent = "/hack:help";
  else (function typeLoop(i, j, del) {
    var w = cmds[i];
    typedEl.textContent = w.slice(0, j);
    if (!del && j < w.length) return setTimeout(typeLoop, 70, i, j + 1, false);
    if (!del) return setTimeout(typeLoop, 1300, i, j, true);
    if (j > 0) return setTimeout(typeLoop, 30, i, j - 1, true);
    setTimeout(typeLoop, 250, (i + 1) % cmds.length, 0, false);
  })(0, 0, false);

  /* hero parallax tilt */
  var stage = $("#heroStage"), tilt = $("#heroTilt");
  if (!reduce && stage) {
    stage.addEventListener("pointermove", function (e) {
      var r = stage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      tilt.style.transform = "rotateX(" + (-y * 26) + "deg) rotateY(" + (x * 26) + "deg)";
    });
    stage.addEventListener("pointerleave", function () { tilt.style.transform = ""; });
  }
  /* card tilt */
  if (!reduce) $$(".tiltable").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      c.style.transform = "perspective(700px) rotateX(" + (-y * 10) + "deg) rotateY(" + (x * 10) + "deg) translateY(-4px)";
    });
    c.addEventListener("pointerleave", function () { c.style.transform = ""; });
  });

  /* ---------------- FLOW ---------------- */
  var actsEl = $("#acts"), panel = $("#panel"), rail = $("#rail"), stations = [], current = 0, playTimer = null;
  var STARTER = ["start", "pick", "ideate", "plan", "pitch"];
  var FOLDS = { pick: ["decode"], ideate: ["users", "compete"], plan: ["validate", "stress", "lock"] };
  var starterOn = false;
  function idx(cmd) { for (var k = 0; k < PHASES.length; k++) if (PHASES[k].cmd === cmd) return k; return -1; }
  function stepFrom(i, dir) {
    if (!starterOn) return i + dir;
    var pos = STARTER.indexOf(PHASES[(i + PHASES.length) % PHASES.length].cmd);
    if (pos < 0) pos = dir > 0 ? -1 : STARTER.length;
    var next = (pos + dir + STARTER.length) % STARTER.length;
    return idx(STARTER[next]);
  }
  Object.keys(ACTS).forEach(function (k) {
    var box = el("div", "act"); box.setAttribute("data-act", k);
    box.appendChild(el("h3", null, ACTS[k]));
    var row = el("div", "stations");
    row.style.setProperty("--n", PHASES.filter(function (p) { return p.act === k; }).length);
    PHASES.forEach(function (p, i) {
      if (p.act !== k) return;
      var b = el("button", "station"); b.type = "button";
      b.setAttribute("aria-label", "Phase " + (i + 1) + ": /hack:" + p.cmd);
      b.appendChild(el("span", "num", String(i + 1).padStart(2, "0") + " · /hack:"));
      b.appendChild(el("span", "cmd", p.cmd));
      b.appendChild(el("span", "ic", p.icon));
      b.addEventListener("click", function () { stop(); show(i, true); });
      stations[i] = b; row.appendChild(b);
    });
    box.appendChild(row); actsEl.appendChild(box);
  });

  function show(i, userInitiated) {
    current = (i + PHASES.length) % PHASES.length;
    var p = PHASES[current];
    var spos = STARTER.indexOf(p.cmd);
    stations.forEach(function (s, k) {
      s.classList.toggle("on", k === current);
      s.classList.toggle("done", starterOn ? (STARTER.indexOf(PHASES[k].cmd) > -1 && STARTER.indexOf(PHASES[k].cmd) < spos) : k < current);
    });
    rail.style.width = (starterOn && spos > -1 ? (spos + 1) / STARTER.length : (current + 1) / PHASES.length) * 100 + "%";
    panel.textContent = "";
    var main = el("div", "panel-main");
    var mainPhases = PHASES.filter(function (x) { return x.cmd !== "retro"; }).length;
    var phaseLabel = p.cmd === "retro" ? "After the event" : "Phase " + (current + 1) + " of " + mainPhases;
    if (starterOn && spos > -1) phaseLabel = "Starter step " + (spos + 1) + " of " + STARTER.length;
    var ph = el("div", "phase", phaseLabel + " · " + ACTS[p.act].replace(/^\S+\s/, "") + " · ~" + p.time);
    main.appendChild(ph);
    var h = el("h3"); h.appendChild(document.createTextNode(p.icon + " " + p.title + " "));
    main.appendChild(h);
    var cmdLine = el("p", "cmd-line mt0"); cmdLine.appendChild(code("/hack:" + p.cmd));
    if (p.trial) cmdLine.appendChild(el("span", "badge trial", "⚖️ TRIAL"));
    if (p.parallel) cmdLine.appendChild(el("span", "badge parallel", "runs in parallel"));
    main.appendChild(cmdLine);
    main.appendChild(el("p", "tag", p.tag));
    if (starterOn && FOLDS[p.cmd]) {
      var fold = el("p", "fold-line");
      fold.appendChild(el("b", null, "Starter path also covers: "));
      fold.appendChild(document.createTextNode(FOLDS[p.cmd].map(function (c) { return "/hack:" + c; }).join(", ") + " (short versions)"));
      main.appendChild(fold);
    }
    var ul = el("ul"); p.does.forEach(function (d) { ul.appendChild(el("li", null, d)); }); main.appendChild(ul);
    var aside = el("aside");
    var a1 = el("div", "kv"); a1.appendChild(el("b", null, "It asks you")); p.asks.forEach(function (q) { a1.appendChild(el("span", "chip q", q)); });
    var a2 = el("div", "kv"); a2.appendChild(el("b", null, "It writes")); p.writes.forEach(function (w) { a2.appendChild(el("span", "chip w", w)); });
    var a3 = el("div", "kv"); a3.appendChild(el("b", null, "Then"));
    if (starterOn && spos > -1) {
      a3.appendChild(spos < STARTER.length - 1 ? code("→ /hack:" + STARTER[spos + 1]) : el("span", null, "Build, then /hack:ship for the PDF (optional)."));
    } else {
      a3.appendChild(current < PHASES.length - 1 ? code("→ /hack:" + PHASES[current + 1].cmd) : el("span", null, "Take the lessons into your next hackathon."));
    }
    aside.appendChild(a1); aside.appendChild(a2); aside.appendChild(a3);
    panel.appendChild(main); panel.appendChild(aside);
    if (!reduce) { panel.classList.remove("flip"); void panel.offsetWidth; panel.classList.add("flip"); }
    if (userInitiated && window.innerWidth <= 860) {
      var d = document.querySelector(".flow-detail");
      if (d) d.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
    }
  }
  var playBtn = $("#playFlow");
  function stop() { clearInterval(playTimer); playTimer = null; playBtn.textContent = "▶ Play the flow"; playBtn.setAttribute("aria-pressed", "false"); }
  function play() {
    if (playTimer) return stop();
    var lastIdx = starterOn ? idx(STARTER[STARTER.length - 1]) : PHASES.length - 1;
    if (current >= lastIdx) show(starterOn ? idx(STARTER[0]) : 0);
    playBtn.textContent = "❚❚ Pause"; playBtn.setAttribute("aria-pressed", "true");
    playTimer = setInterval(function () { if (current >= lastIdx) return stop(); show(stepFrom(current, 1)); }, 2600);
  }
  playBtn.addEventListener("click", play);
  $("#prevPhase").addEventListener("click", function () { stop(); show(stepFrom(current, -1), true); });
  $("#nextPhase").addEventListener("click", function () { stop(); show(stepFrom(current, 1), true); });
  var starterBtn = $("#starterPath"), starterNote = $("#starterNote");
  if (starterBtn) {
    starterBtn.addEventListener("click", function () {
      stop();
      starterOn = !starterOn;
      starterBtn.setAttribute("aria-pressed", starterOn ? "true" : "false");
      starterBtn.textContent = starterOn ? "Show all 14 phases" : "🌱 Starter path";
      if (starterNote) starterNote.hidden = !starterOn;
      actsEl.classList.toggle("starter", starterOn);
      stations.forEach(function (s, k) { s.classList.toggle("dim", starterOn && STARTER.indexOf(PHASES[k].cmd) < 0); });
      show(starterOn ? idx(STARTER[0]) : current);
    });
  }
  var backBtn = $("#panelBackLink");
  if (backBtn) {
    backBtn.addEventListener("click", function () {
      var a = $("#acts");
      if (a) a.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    });
  }
  document.addEventListener("keydown", function (e) {
    var t = e.target.tagName; if (t === "INPUT" || t === "TEXTAREA") return;
    var f = $("#flow").getBoundingClientRect();
    if (f.top > window.innerHeight || f.bottom < 0) return;
    if (e.key === "ArrowRight") { stop(); show(stepFrom(current, 1), true); }
    if (e.key === "ArrowLeft") { stop(); show(stepFrom(current, -1), true); }
  });
  show(0);

  /* ---------------- COURT ---------------- */
  var running = false;
  var ring = $("#ring"), ringStage = $("#ringStage"), ringHint = $("#ringHint"), jurorEls = [];
  /* Ring physics: auto-spin, drag with momentum, hold to fan out, tap to flip. */
  var RS = { angle: 0, vel: 0, auto: reduce ? 0 : -0.16, tilt: -10, tiltT: -10, scale: 1, scaleT: 1,
    spread: 0, spreadT: 0, baseR: 260, dragging: false, held: false, paused: false, visible: true };
  function placeJurors() {
    var r = RS.baseR + RS.spread;
    jurorEls.forEach(function (j, i) { j.style.transform = "rotateY(" + (i * 30) + "deg) translateZ(" + r.toFixed(1) + "px)"; });
  }
  function layoutRing() {
    var w = ring.offsetWidth || 130;
    RS.baseR = Math.round((w / 2) / Math.tan(Math.PI / 12) + 22);
    placeJurors();
  }
  JURORS.forEach(function (d, i) {
    var j = el("div", "juror"), inner = el("div", "inner");
    var f = el("div", "jcard front");
    f.appendChild(el("span", "no", "JUROR " + (i + 1)));
    f.appendChild(el("span", "av", d[0]));
    f.appendChild(el("span", "nm", d[1]));
    var b = el("div", "jcard back " + (d[2] === "NG" ? "ng" : d[2] === "G" ? "g" : "ie"));
    b.appendChild(el("span", "stamp", d[2] === "NG" ? "NOT GUILTY" : d[2] === "G" ? "GUILTY" : "INSUFFICIENT EVIDENCE"));
    b.appendChild(el("span", "why", d[3]));
    inner.appendChild(f); inner.appendChild(b); j.appendChild(inner);
    ring.appendChild(j); jurorEls.push(j);
  });
  layoutRing(); window.addEventListener("resize", layoutRing);

  var lastSpread = -1, rafOn = false;
  function frame() {
    if (!RS.visible) { rafOn = false; return; }
    if (!RS.dragging) {
      if (RS.paused || RS.held) RS.vel *= 0.86;
      else RS.vel += (RS.auto - RS.vel) * 0.025;
      RS.angle += RS.vel;
    }
    RS.tilt += (RS.tiltT - RS.tilt) * 0.12;
    RS.scale += (RS.scaleT - RS.scale) * 0.15;
    RS.spread += (RS.spreadT - RS.spread) * 0.12;
    ring.style.transform = "scale(" + RS.scale.toFixed(4) + ") rotateX(" + RS.tilt.toFixed(2) + "deg) rotateY(" + RS.angle.toFixed(2) + "deg)";
    if (Math.abs(RS.spread - lastSpread) > 0.3) { placeJurors(); lastSpread = RS.spread; }
    requestAnimationFrame(frame);
  }
  function startRaf() { if (!rafOn) { rafOn = true; requestAnimationFrame(frame); } }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { RS.visible = es[0].isIntersecting; if (RS.visible) startRaf(); }).observe(ringStage);
  }
  startRaf();

  var px = 0, py = 0, sx = 0, sy = 0, moved = 0, lastT = 0, holdT = null, pid = null, hinted = false;
  function hideHint() { if (!hinted) { hinted = true; ringHint.classList.add("gone"); } }
  function flipCard(j) {
    if (!j || running) return;
    j.classList.toggle("flipped");
    if (!reduce) { j.classList.remove("pop"); void j.offsetWidth; j.classList.add("pop"); }
  }
  ringStage.addEventListener("pointerdown", function (e) {
    if (pid !== null) return;
    pid = e.pointerId; RS.dragging = true; moved = 0;
    px = sx = e.clientX; py = sy = e.clientY; lastT = performance.now();
    RS.vel = 0; RS.scaleT = 1.04;
    ringStage.classList.add("grabbing");
    try { ringStage.setPointerCapture(pid); } catch (err) {}
    clearTimeout(holdT);
    holdT = setTimeout(function () {
      if (moved < 8 && RS.dragging) {
        RS.held = true; RS.spreadT = 70; RS.scaleT = 1.08;
        ringStage.classList.add("held");
        if (navigator.vibrate) { try { navigator.vibrate(12); } catch (err) {} }
      }
    }, 380);
    hideHint();
  });
  ringStage.addEventListener("pointermove", function (e) {
    if (e.pointerId !== pid || !RS.dragging) return;
    var now = performance.now(), dx = e.clientX - px, dy = e.clientY - py, dt = Math.max(now - lastT, 8);
    moved += Math.abs(dx) + Math.abs(dy);
    var d = dx * 0.42;
    RS.angle += d;
    RS.vel = RS.vel * 0.6 + (d * 16 / dt) * 0.4;
    RS.tiltT = Math.max(-38, Math.min(22, -10 - (e.clientY - sy) * 0.12));
    px = e.clientX; py = e.clientY; lastT = now;
    if (moved >= 8 && !RS.held) clearTimeout(holdT);
  });
  function release(e) {
    if (e.pointerId !== pid) return;
    clearTimeout(holdT);
    var wasTap = moved < 8 && !RS.held && e.type === "pointerup";
    RS.dragging = false; pid = null;
    RS.vel = Math.max(-14, Math.min(14, RS.vel));
    if (performance.now() - lastT > 90) RS.vel *= 0.3;
    RS.tiltT = -10; RS.scaleT = 1; RS.spreadT = 0; RS.held = false;
    ringStage.classList.remove("grabbing", "held");
    if (wasTap) {
      var hit = document.elementFromPoint(e.clientX, e.clientY);
      flipCard(hit && hit.closest ? hit.closest(".juror") : null);
    }
  }
  ringStage.addEventListener("pointerup", release);
  ringStage.addEventListener("pointercancel", release);
  ringStage.addEventListener("lostpointercapture", function (e) { if (e.pointerId === pid) release(e); });
  ringStage.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { RS.vel -= 4; e.preventDefault(); hideHint(); }
    if (e.key === "ArrowRight") { RS.vel += 4; e.preventDefault(); hideHint(); }
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      var a = ((-RS.angle % 360) + 360) % 360, idx = Math.round(a / 30) % 12;
      flipCard(jurorEls[idx]);
    }
  });

  var ratingsEl = $("#ratings"), bars = [];
  RATINGS.forEach(function (r) {
    var row = el("div", "rate"); row.appendChild(el("span", null, r[0]));
    var bar = el("span", "bar"), fill = el("i"); bar.appendChild(fill); row.appendChild(bar);
    row.appendChild(el("span", null, "–")); ratingsEl.appendChild(row); bars.push([fill, row.lastChild, r[1]]);
  });

  var steps = $$("#trialSteps li"), tally = $("#tally"), verdict = $("#verdict"), runBtn = $("#runTrial");
  function setTally(ng, g, ie) {
    tally.textContent = "";
    tally.appendChild(el("span", "ng", ng + " NOT GUILTY")); tally.appendChild(document.createTextNode(" · "));
    tally.appendChild(el("span", "g", g + " GUILTY")); tally.appendChild(document.createTextNode(" · "));
    tally.appendChild(el("span", "ie", (ie || 0) + " INSUFFICIENT"));
  }
  function resetTrial() {
    steps.forEach(function (s) { s.classList.remove("lit"); });
    jurorEls.forEach(function (j) { j.classList.remove("flipped"); });
    bars.forEach(function (b) { b[0].style.width = "0"; b[1].textContent = "–"; });
    verdict.classList.remove("show"); setTally(0, 0, 0);
  }
  runBtn.addEventListener("click", function () {
    if (running) return; running = true; runBtn.disabled = true; resetTrial();
    RS.paused = true;
    var t = 0, gap = reduce ? 60 : 700, ng = 0, g = 0, ie = 0;
    steps.slice(0, 3).forEach(function (s, k) { setTimeout(function () { s.classList.add("lit"); }, t + k * gap); });
    t += 3 * gap;
    setTimeout(function () { steps[3].classList.add("lit"); RS.paused = false; }, t);
    JURORS.forEach(function (d, i) {
      setTimeout(function () {
        jurorEls[i].classList.add("flipped");
        if (d[2] === "NG") ng++; else if (d[2] === "G") g++; else ie++;
        setTally(ng, g, ie);
      }, t + 200 + i * (reduce ? 30 : 380));
    });
    t += 200 + JURORS.length * (reduce ? 30 : 380) + 400;
    setTimeout(function () {
      steps[4].classList.add("lit"); RS.paused = true;
      verdict.textContent = "";
      var decision = (ie * 3 > JURORS.length) ? "INCONCLUSIVE" : (g > ng) ? "FAIL" : (ng / JURORS.length >= 0.75) ? "PASS" : "REVISE";
      verdict.appendChild(document.createTextNode(decision));
      verdict.appendChild(el("small", null, "NG " + ng + " · G " + g + " · IE " + ie + " · avg confidence 7.1/10"));
      verdict.classList.add("show");
      bars.forEach(function (b, k) { setTimeout(function () { b[0].style.width = (b[2] * 10) + "%"; b[1].textContent = b[2]; }, k * 90); });
    }, t);
    setTimeout(function () {
      verdict.classList.remove("show"); RS.paused = false;
      running = false; runBtn.disabled = false; runBtn.textContent = "⚖️ Run it again";
    }, t + 4200);
  });

  /* ---------------- TREE / RULES / TIMELINE ---------------- */
  var tree = $("#tree");
  TREE.forEach(function (r, i) {
    var d = el("div", r[0] === "d" ? "d" : "f" + (r[3] ? " hl" : ""));
    var name = r[1];
    var m = name.match(/^([├└─\s]*)(.*)$/);
    d.appendChild(document.createTextNode(m[1]));
    d.appendChild(r[0] === "f" ? el("b", null, m[2]) : document.createTextNode(m[2]));
    if (r[2]) d.appendChild(el("span", "d", "  " + r[2]));
    d.style.transitionDelay = (i * 70) + "ms";
    tree.appendChild(d);
  });

  var rg = $("#rulesGrid");
  RULES.forEach(function (r, i) {
    var b = el("button", "rule reveal"); b.type = "button";
    b.setAttribute("aria-label", "Rule " + (i + 1) + ": " + r[0] + ". " + r[1]);
    var inn = el("div", "rin"), fc = el("div", "fc"), bc = el("div", "bc", r[1]);
    fc.appendChild(el("span", "n", String(i + 1).padStart(2, "0")));
    fc.appendChild(el("h3", null, r[0]));
    inn.appendChild(fc); inn.appendChild(bc); b.appendChild(inn);
    b.addEventListener("click", function () { b.classList.toggle("flip"); });
    b.style.transitionDelay = (i % 4) * 60 + "ms";
    rg.appendChild(b);
  });

  var tl = $("#tl");
  TIMELINE.forEach(function (r) {
    var d = el("div", "tl reveal" + (r[3] ? " freeze" : ""));
    d.appendChild(el("span", "t", r[0])); d.appendChild(el("h3", null, r[1])); d.appendChild(el("p", null, r[2]));
    tl.appendChild(d);
  });

  /* ---------------- TABS ---------------- */
  var tabs = $$(".tab");
  function selectTab(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab, p = document.getElementById(t.getAttribute("aria-controls"));
      t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
      p.hidden = !on;
      if (on && !reduce) { p.classList.remove("anim"); void p.offsetWidth; p.classList.add("anim"); }
    });
    if (focus) tab.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") selectTab(tabs[(i + 1) % tabs.length], true);
      if (e.key === "ArrowLeft") selectTab(tabs[(i - 1 + tabs.length) % tabs.length], true);
    });
  });

  /* ---------------- REVEAL ON SCROLL ---------------- */
  var targets = $$(".reveal, .tree");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: .12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add("in"); });
})();
