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
      does: ["Fetches or reads the brief and pulls out the rubric, rules and deliverables", "Translates the top 3 rubric items into plain words", "Sets quick or full mode, the captain, and the freeze times"],
      asks: ["Rubric & weights", "Slide limit", "Time left", "Team skills"], writes: ["BRIEF.md", "STATE.md"], time: "5 min" },
    { act: "find", cmd: "decode", icon: "🔍", title: "Understand every statement",
      tag: "In 2 minutes each, with the angle 70% of teams miss.",
      does: ["Real problem, end user, operator, least-digital user", "Hidden constraints: language, offline, devices, existing systems", "Root cause (3 whys), data situation", "Obvious idea vs smarter angle"],
      asks: ["Paste statements", "Organiser hints", "Drop any now?"], writes: ["STATEMENTS.md"], time: "15 min" },
    { act: "find", cmd: "pick", icon: "⚖️", trial: true, title: "Choose the statement worth your weekend",
      tag: "Rubric-weighted scoring, red flags, then a trial.",
      does: ["Scores every statement on 8 weighted criteria", "Flags hardware, data, safety and 'already solved' risks", "Runs a courtroom trial on the top 2–3", "Recommends one, and the captain decides"],
      asks: ["Confirm shortlist", "Final pick"], writes: ["PICK.md", "court/"], time: "15 min" },
    { act: "shape", cmd: "users", icon: "🧭", title: "Think as every real user",
      tag: "Especially the one most likely to be left out.",
      does: ["One card per stakeholder: today, worst step, refusals, adoption trigger", "POV statement, How-Might-We, job story", "Persona with a day in their life", "Contrast motto options"],
      asks: ["Who are the users?", "Personal experience?", "Pick the motto"], writes: ["USERS.md"], time: "10 min" },
    { act: "shape", cmd: "validate", icon: "📰", title: "Prove it's real",
      tag: "Three layers of evidence, every source opened.",
      does: ["Sourced numbers from government data, papers and reports", "Real complaints from news, forums and app reviews", "A local example near the event", "A 5-minute Mom-Test venue interview script"],
      asks: ["Talked to anyone yet?", "Add venue notes"], writes: ["EVIDENCE.md"], time: "20 min", parallel: true },
    { act: "shape", cmd: "compete", icon: "🗺️", title: "Know what already exists",
      tag: "Honest positioning. Never 'no competitors'.",
      does: ["6–10 existing solutions, including government portals and past hackathon projects", "Gap table on what matters to the user", "Coexistence levels L0–L3 with existing systems", "A one-line positioning statement"],
      asks: ["Known competitors?", "System to work alongside?"], writes: ["COMPETE.md"], time: "20 min", parallel: true },
    { act: "shape", cmd: "stress", icon: "🥊", title: "Attack it before the judges do",
      tag: "Stands in for the domain expert you don't have.",
      does: ["Role-plays the expert, front-line worker, least-digital user, sceptic and admin", "Fix table: the smallest fix that keeps the core", "Warns when a fix drifts from the idea"],
      asks: ["Which fixes to accept?"], writes: ["STRESS.md", "CORE.md (draft)"], time: "15 min" },
    { act: "shape", cmd: "lock", icon: "🔒", title: "Freeze the core",
      tag: "One idea the whole team can repeat word for word.",
      does: ["Motto, positioning, persona before and after, end-to-end journey", "Who does what, 4–6 USPs tied to user pains", "AI vs rules vs humans table", "Mistakes check, then LOCKED"],
      asks: ["Lock it?"], writes: ["CORE.md 🔒"], time: "10 min" },
    { act: "build", cmd: "plan", icon: "🛠️", title: "One journey, built for real",
      tag: "One wow moment. Mock the rest and say so.",
      does: ["Build / Mock / Cut for every feature", "Stack with a reason and a fallback for each layer", "Hour-by-hour plan and freeze times", "90-second demo script and 8–12 AI test cases"],
      asks: ["Fastest stack", "Hours left", "Sponsor API", "Roles"], writes: ["PLAN.md"], time: "20 min" },
    { act: "build", cmd: "verify", icon: "⚖️", trial: true, title: "Put the solution on trial",
      tag: "Find the weak spots while there's still time to fix them.",
      does: ["Courtroom trial of the planned solution", "Rubric score out of 100, as a strict judge would give it", "Mistakes check and claims check", "Ranked fixes, applied inside the core"],
      asks: ["Which fixes to apply?"], writes: ["VERDICT.md", "court/"], time: "15 min" },
    { act: "build", cmd: "pitch", icon: "🎤", title: "Say it so judges remember it",
      tag: "Within the slide limit, every number sourced.",
      does: ["One-line pitch and an opening line for the top rubric item", "Deck outline: a full-sentence headline per slide", "Form answers within word limits", "12–15 likely judge questions, with answers"],
      asks: ["Slide limit", "Pitch length", "Form questions"], writes: ["PITCH.md"], time: "25 min" },
    { act: "build", cmd: "ship", icon: "📄", title: "One Idea Pack",
      tag: "Everything compiled into one document.",
      does: ["Writes a one-page SUMMARY.md", "Joins every file, with a cover and contents", "Outputs FINAL.md, FINAL.html and FINAL.pdf"],
      asks: ["PDF, Markdown or both?"], writes: ["SUMMARY.md", "FINAL.pdf"], time: "5 min" }
  ];
  var ACTS = { find: "🔍 Find it", shape: "🧭 Shape it", build: "🚀 Build & sell it" };

  var JURORS = [
    ["🧑", "Actual end user", "NG", "I'd check in by voice while waiting anyway."],
    ["👵", "Least-digital user", "NG", "A normal phone call works for me."],
    ["🩺", "Front-line worker", "G", "Entering vitals by token adds a step in rush hour."],
    ["👩‍⚕️", "Domain professional", "NG", "The doctor still approves every test."],
    ["📒", "Workaround user", "G", "My paper file already works for me."],
    ["🔎", "Root-cause analyst", "NG", "It hits report-only return visits."],
    ["📚", "'Already exists' researcher", "NG", "The voice check-in in the patient's own words is new."],
    ["🛡️", "Safety reviewer", "NG", "Red flags use fixed rules, not AI."],
    ["🖥️", "Systems person", "NG", "Works with only a token number (L0)."],
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
    ["Lock the core", "Motto, persona, journey, USPs. After lock, fixes go inside the core."],
    ["Fit existing systems", "No new hardware. Work alongside the software and process people already have."],
    ["Simple for the user", "No app download, no typing, works on the simplest device they own."],
    ["AI suggests, humans decide", "Safety-critical checks use fixed rules. Every AI step has a human check."],
    ["One full journey", "The MVP is one complete journey with one wow moment. Mock the rest and say so."],
    ["No unsourced numbers", "Every number has a link or is marked UNVERIFIED. Targets are labelled as targets."],
    ["Simple English", "Short sentences. Explain it the way you'd tell a friend."]
  ];

  var TIMELINE = [
    ["0:00", "/hack:start", "Fill in the brief, ideally before the statements drop."],
    ["0:05", "/hack:decode", "Paste the statements and decode every one."],
    ["0:20", "/hack:pick", "Score and trial the top ideas. The captain decides."],
    ["0:35", "/hack:users", "Persona, POV and motto."],
    ["0:45", "validate ‖ compete", "Split the team, and go talk to real people at the venue."],
    ["1:10", "/hack:stress", "Attack the idea and fix it inside the core."],
    ["~1:30", "/hack:lock 🔒", "Idea freeze. From here, you build.", true],
    ["1:40", "/hack:plan → /hack:verify", "One journey, then a trial of the solution."],
    ["−4 h", "Code freeze", "Record the backup demo video.", true],
    ["Before judging", "/hack:pitch → /hack:ship", "Deck, Q&A and FINAL.pdf."]
  ];

  var TREE = [
    ["d", ".hackathon/"], ["f", "├── STATE.md", "phase checklist, decisions"], ["f", "├── BRIEF.md", "rubric, limits, team"],
    ["f", "├── STATEMENTS.md", "every statement decoded"], ["f", "├── PICK.md", "scores + trial"], ["f", "├── USERS.md", "persona, motto"],
    ["f", "├── EVIDENCE.md", "sources, venue notes"], ["f", "├── COMPETE.md", "gap table"], ["f", "├── STRESS.md", "doubts + fixes"],
    ["f", "├── CORE.md", "🔒 the locked idea", true], ["f", "├── PLAN.md", "MVP, demo script"], ["f", "├── VERDICT.md", "trial + rubric score"],
    ["f", "├── PITCH.md", "deck + Q&A"], ["f", "├── SUMMARY.md", "one page"], ["f", "├── FINAL.pdf", "📄 everything", true], ["d", "└── court/", "full trial records"]
  ];

  var PROMPT = "You are my hackathon ideation partner. Run the Hack Kit process with me, one phase at a time, and keep a running \"Idea Pack\" summary after each phase.\n\n" +
    "Phases: start (brief, rubric, team, time) → decode (each statement: real problem, end user, least-digital user, hidden constraints, root cause, obvious idea vs smarter angle) → pick (weighted scoring + red flags + trial of top 2–3) → users (stakeholder views, POV, HMW, persona, motto) → validate (sourced facts, real complaints, venue interview script) → compete (existing solutions, gap table, coexistence with existing systems) → stress (role-play domain expert and sceptic, smallest fixes inside the core) → lock (freeze motto, journey, USPs, AI-vs-rules-vs-humans table) → plan (one-journey MVP, build/mock/cut, stack, demo script, AI test cases) → verify (trial of the solution + rubric score + claims check) → pitch (deck outline within slide limit, form answers, judge Q&A) → ship (one final document).\n\n" +
    "Rules: judge only whether the problem is real and the solution solves it for real users — never business viability. No unsourced numbers. AI suggests, humans decide. No app, no typing, works for the least-digital user. After lock, fixes stay inside the core. Ask me questions with numbered options when my answer matters. Simple English.\n\n" +
    "Trial = case file → prosecution 5 points → defense 5 points → 12 jurors (end user, least-digital user, front-line worker, domain professional, workaround user, root-cause analyst, already-exists researcher, safety reviewer, systems person, engineer, statement owner, sceptic) each voting GUILTY/NOT GUILTY with confidence 1–10, reason and fix → judge gives verdict, ratings /10, top 3 fail reasons, top 3 fixes, a 30-minute venue check, and \"If I were your team…\". GUILTY means \"it does not solve a real problem for its real users\".\n\n" +
    "Start with phase \"start\": ask me about the event.";

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
  var typedEl = $("#typed"), cmds = ["/hack:start", "/hack:decode", "/hack:pick --quick", "/hack:lock", "/hack:verify", "/hack:ship"];
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
      b.addEventListener("click", function () { stop(); show(i); });
      stations[i] = b; row.appendChild(b);
    });
    box.appendChild(row); actsEl.appendChild(box);
  });

  function show(i) {
    current = (i + PHASES.length) % PHASES.length;
    var p = PHASES[current];
    stations.forEach(function (s, k) { s.classList.toggle("on", k === current); s.classList.toggle("done", k < current); });
    rail.style.width = ((current + 1) / PHASES.length * 100) + "%";
    panel.textContent = "";
    var main = el("div");
    var ph = el("div", "phase", "Phase " + (current + 1) + " of 12 · " + ACTS[p.act].replace(/^\S+\s/, "") + " · ~" + p.time);
    main.appendChild(ph);
    var h = el("h3"); h.appendChild(document.createTextNode(p.icon + " " + p.title + " "));
    main.appendChild(h);
    var cmdLine = el("p", "mt0"); cmdLine.appendChild(code("/hack:" + p.cmd));
    if (p.trial) cmdLine.appendChild(el("span", "badge", "⚖️ TRIAL"));
    if (p.parallel) cmdLine.appendChild(el("span", "badge", "runs in parallel"));
    main.appendChild(cmdLine);
    main.appendChild(el("p", "tag", p.tag));
    var ul = el("ul"); p.does.forEach(function (d) { ul.appendChild(el("li", null, d)); }); main.appendChild(ul);
    var aside = el("aside");
    var a1 = el("div", "kv"); a1.appendChild(el("b", null, "It asks you")); p.asks.forEach(function (q) { a1.appendChild(el("span", "chip q", q)); });
    var a2 = el("div", "kv"); a2.appendChild(el("b", null, "It writes")); p.writes.forEach(function (w) { a2.appendChild(el("span", "chip w", w)); });
    var a3 = el("div", "kv"); a3.appendChild(el("b", null, "Then"));
    a3.appendChild(current < PHASES.length - 1 ? code("→ /hack:" + PHASES[current + 1].cmd) : el("span", null, "Build the demo, record a backup, rehearse the Q&A."));
    aside.appendChild(a1); aside.appendChild(a2); aside.appendChild(a3);
    panel.appendChild(main); panel.appendChild(aside);
    if (!reduce) { panel.classList.remove("flip"); void panel.offsetWidth; panel.classList.add("flip"); }
  }
  var playBtn = $("#playFlow");
  function stop() { clearInterval(playTimer); playTimer = null; playBtn.textContent = "▶ Play the flow"; playBtn.setAttribute("aria-pressed", "false"); }
  function play() {
    if (playTimer) return stop();
    if (current >= PHASES.length - 1) show(0);
    playBtn.textContent = "❚❚ Pause"; playBtn.setAttribute("aria-pressed", "true");
    playTimer = setInterval(function () { if (current >= PHASES.length - 1) return stop(); show(current + 1); }, 2600);
  }
  playBtn.addEventListener("click", play);
  $("#prevPhase").addEventListener("click", function () { stop(); show(current - 1); });
  $("#nextPhase").addEventListener("click", function () { stop(); show(current + 1); });
  document.addEventListener("keydown", function (e) {
    var t = e.target.tagName; if (t === "INPUT" || t === "TEXTAREA") return;
    var f = $("#flow").getBoundingClientRect();
    if (f.top > window.innerHeight || f.bottom < 0) return;
    if (e.key === "ArrowRight") { stop(); show(current + 1); }
    if (e.key === "ArrowLeft") { stop(); show(current - 1); }
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
    var b = el("div", "jcard back " + (d[2] === "NG" ? "ng" : "g"));
    b.appendChild(el("span", "stamp", d[2] === "NG" ? "NOT GUILTY" : "GUILTY"));
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
  function setTally(ng, g) {
    tally.textContent = "";
    tally.appendChild(el("span", "ng", ng + " NOT GUILTY")); tally.appendChild(document.createTextNode(" · ")); tally.appendChild(el("span", "g", g + " GUILTY"));
  }
  function resetTrial() {
    steps.forEach(function (s) { s.classList.remove("lit"); });
    jurorEls.forEach(function (j) { j.classList.remove("flipped"); });
    bars.forEach(function (b) { b[0].style.width = "0"; b[1].textContent = "–"; });
    verdict.classList.remove("show"); setTally(0, 0);
  }
  runBtn.addEventListener("click", function () {
    if (running) return; running = true; runBtn.disabled = true; resetTrial();
    RS.paused = true;
    var t = 0, gap = reduce ? 60 : 700, ng = 0, g = 0;
    steps.slice(0, 3).forEach(function (s, k) { setTimeout(function () { s.classList.add("lit"); }, t + k * gap); });
    t += 3 * gap;
    setTimeout(function () { steps[3].classList.add("lit"); RS.paused = false; }, t);
    JURORS.forEach(function (d, i) {
      setTimeout(function () {
        jurorEls[i].classList.add("flipped");
        if (d[2] === "NG") ng++; else g++;
        setTally(ng, g);
      }, t + 200 + i * (reduce ? 30 : 380));
    });
    t += 200 + JURORS.length * (reduce ? 30 : 380) + 400;
    setTimeout(function () {
      steps[4].classList.add("lit"); RS.paused = true;
      verdict.textContent = "";
      verdict.appendChild(document.createTextNode("NOT GUILTY"));
      verdict.appendChild(el("small", null, ng + " of 12 · avg confidence 7.3/10"));
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
