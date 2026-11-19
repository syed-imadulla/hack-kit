# STATEMENTS — Mock Social Good Hack (test run)

> Summary: 3 statements decoded · strongest looking: S2 (certificates), S1 (farm prices) · dropped: none yet

## Summary table
| # | Statement | One-line problem | End user | Obvious idea | Smarter angle | Biggest unknown |
|---|---|---|---|---|---|---|
| S1 | Farm prices | Small farmers sell without knowing prices and demand, so they get less | Small and marginal farmer | Mandi price app | Voice price alerts on a basic phone, with a "hold or sell" nudge | Do farmers act on price info, or are they forced to sell by debt and storage? |
| S2 | Certificates | Applications get rejected for missing or wrong documents, causing repeat visits | Low-literacy citizen applying for income/caste/residence certificates | Online application portal | Pre-check documents *before* submission, in the citizen's language, at the CSC counter or by phone | How many rejections are document problems vs officer discretion? |
| S3 | Reading levels | Teachers can't track each child's reading level in big classes | Government school teacher (and the child) | Reading app for kids | 2-minute voice reading check per child, grouping kids by level for the teacher | Do teachers have time and devices in class? |

---

## Statement S1: Farm prices
> Small and marginal farmers lose income because they sell produce without knowing current mandi prices and demand. Build a solution that helps them decide when and where to sell.

| Field | Notes |
|---|---|
| In one line | Farmers sell at the wrong time or place because they lack price information |
| Who posted it and why | Organiser (social good track); likely wants agri-tech with real rural reach |
| Real end user | Small and marginal farmer, 1–2 acres |
| How bad, how often, how many | Distress sales are common among smallholders [AI] (search snippet: [Indian Journal of Agricultural Marketing, 2025](https://ideas.repec.org/a/ags/injagm/400070.html), not opened); every harvest season |
| Operator | Farmer producer organisation (FPO) staff or agri extension worker |
| Least-digital user | Older farmer with a keypad phone, regional language only |
| Where it happens | Village to mandi; basic phones; patchy data |
| Hidden constraints | Debt and storage force sales regardless of price [AI]; Agmarknet data exists but is delayed or patchy [?] |
| Root cause guess (3 whys) | Low price → sold at the wrong time/place → no info, no storage, urgent cash need |
| Data situation | Agmarknet / data.gov.in public price feeds [AI] |
| Obvious idea | Mandi price app |
| Smarter angle | Voice alerts on a basic phone plus a "hold or sell" nudge linked to storage options |
| 24/36 h MVP | Farmer calls, says crop and village, hears the best nearby mandi price and travel trade-off |
| Unknowns to ask | Does information change behaviour when debt forces the sale? |
| Quick sources | Search snippets only, not opened |

## Statement S2: Certificates
> Citizens make repeated trips to government offices for certificates (income, caste, residence) because applications get rejected for missing or wrong documents. Reduce rejections and repeat visits.

| Field | Notes |
|---|---|
| In one line | Applications get rejected for document problems, so people make repeat trips |
| Who posted it and why | Likely a civic or e-governance sponsor that wants fewer rejections |
| Real end user | Low-literacy citizen (often a student or farmer needing an income/caste certificate) |
| How bad, how often, how many | Missing or wrong documents are a common rejection reason [AI] (search snippets from state portal FAQs and guides, not opened); certificates are needed for scholarships, jobs and schemes [AI] |
| Operator | CSC / e-Mitra / Seva Sindhu operator; tehsil clerk |
| Least-digital user | Elderly person who depends on the CSC operator |
| Where it happens | CSC counters, tehsil offices; e-District portals differ by state |
| Hidden constraints | State portals differ; officers verify in the field; name mismatches with Aadhaar [AI] |
| Root cause guess (3 whys) | Rejection → missing or mismatched documents → applicant didn't know the exact checklist → checklists are scattered and differ by state and certificate |
| Data situation | Public document checklists per state portal; no rejection data [?] |
| Obvious idea | Another online application portal |
| Smarter angle | A document pre-check before submission: a photo of each document, checked for the right type, name match and date, in the citizen's language |
| 24/36 h MVP | Citizen or operator photographs documents → the tool flags missing or mismatched ones → a checklist in Kannada/Hindi |
| Unknowns to ask | What share of rejections are document issues vs discretion? Would CSC operators use it? |
| Quick sources | Search snippets only, not opened |

## Statement S3: Reading levels
> Students in government schools fall behind in reading, and teachers can't track each child's level in large classes. Help teachers identify and support struggling readers.

| Field | Notes |
|---|---|
| In one line | Teachers can't track each child's reading level, so struggling readers fall behind |
| Who posted it and why | Education track; foundational literacy focus |
| Real end user | Class 3–5 government school teacher; the child |
| How bad, how often, how many | Only about a quarter of rural Class 3 children read at Class 2 level [AI] (ASER 2024, via news snippets, not opened) |
| Operator | Teacher |
| Least-digital user | Teacher without a smartphone in class; children with no devices |
| Where it happens | Classrooms of 40–60; limited devices and data |
| Hidden constraints | Child data privacy; teacher workload; school device rules |
| Root cause guess (3 whys) | Falling behind → no individual attention → no quick way to know each child's level |
| Data situation | ASER-style reading levels are public; speech data for children's voices is scarce |
| Obvious idea | A reading app for kids |
| Smarter angle | 2-minute voice reading check per child on the teacher's phone, then group by level |
| 24/36 h MVP | Child reads a passage → speech model scores fluency → teacher sees groups |
| Unknowns to ask | Can speech recognition handle children's voices in regional languages? |
| Quick sources | Search snippets only, not opened |

---

## Dropped
| # | Reason |
|---|---|
| — | None dropped (team asked: keep all three for scoring) |
