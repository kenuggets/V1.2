# Launchpad Product Specification
**Version**: 1.0 · **Last updated**: March 2026

---

## 1. Vision & Mission

**Launchpad** is an AI-powered career platform for university students in Australia (and globally) targeting their first internship. It guides students through every stage of the career journey — from "I have no idea what I want" to signed offer — with deeply personalised coaching, real professional insights, and structured accountability tools.

**Mission**: Give every university student the same advantage as those with a connected mentor, regardless of their network or background.

**Long-term vision**: Begin with internships, expand to graduate roles, and eventually cover the full career arc from student to senior hire.

---

## 2. Target User

**Primary**: Australian university students (years 1–3/4) seeking their first internship.

**Characteristics**:
- No prior professional experience
- Unsure which career path fits them
- Understands they need to network and apply, but doesn't know how
- Active during Australian recruiting seasons (Feb–April for Big 4/banking/consulting programs)
- Uses mobile frequently but does initial research on desktop

**Out of scope (V1)**: Career changers, senior professionals, international job seekers.

---

## 3. Core Differentiators

Launchpad is differentiated on three equal pillars — none of which existing tools (LinkedIn, Handshake, Final Round AI, InterviewPal) deliver together:

1. **End-to-end journey** — Competitors own one slice (jobs, interviews, or networking). Launchpad owns the whole arc from confusion to offer.
2. **Student-specific depth** — Built for students with zero experience. No assumptions about prior work history.
3. **Personalised coaching** — Every output is tailored to the individual student's degree, year, target sector, and actual experience. Not generic templates.

---

## 4. User Journey & Site Flow

```
Landing page (public)
  └─ Sign up (email or Google/LinkedIn OAuth)
       └─ Onboarding (10-step questionnaire)
            └─ Tour (mandatory first visit, skippable, accessible from profile)
                 └─ Dashboard (home base — adaptive: engaging for new users, fast nav for experienced)
                      ├─ Discover
                      ├─ Build
                      ├─ Prepare
                      └─ Profile / Settings
```

### Career Stage Progression
Users move through 5 stages based on completed milestones:

| Stage | Level | Trigger |
|-------|-------|---------|
| Exploring | 0 | Default on signup |
| Building | 1 | Skills gap analysis completed |
| Applying | 2 | ≥1 application or outreach contact added |
| Preparing | 3 | ≥1 coffee chat or interview prep completed |
| Offer | 4 | Offer received badge earned |

Stage drives visible personalisation: dashboard messaging, weekly goal tone, and recommended next actions.

### Post-Offer Experience
When a user reaches Offer stage, the platform transitions to **Internship Success Mode**: first impressions, internal networking, professionalism, and how to secure a return offer. After completion, the platform gently surfaces the next career target to restart the journey.

---

## 5. Modules

### 5.1 Discover

**Purpose**: Help students understand what they want before they start applying.

#### Role Explorer
- Browse roles by sector (Finance, Consulting, Tech, Law, Accounting, etc.)
- Click into any role for a full profile: description, typical hours, average salary (AU$), exit opportunities, work-life balance rating, required skills
- Role data is **AI-generated first, human-edited for key facts** (salary, hours) before publication
- Australian-specific firms featured prominently: ANZ, CBA, NAB, Westpac, Macquarie, UBS, Goldman Sachs AU, BCG, McKinsey, Bain, Deloitte, PwC, KPMG, EY

#### Role Comparison
- Side-by-side comparison of 2–4 roles
- Dimensions: hours/week, base salary (AU$), exit opportunities, work-life balance, required skills, culture notes
- User can save comparisons to their profile

#### Day-in-the-Life
- Real stories from professionals describing an actual day in their role
- **Content strategy**: Founder-seeded initially (5–10 high-quality stories per priority role). Open submissions scale it. AI pre-screens quality; founder approves before publishing.
- Displayed per role under "From Professionals" section
- Separate from AI-generated role profile content

#### Skills Gap Analysis
- User inputs their current skills, experience, degree, and year of study
- Claude returns a personalised gap analysis: what they're missing, what they have, specific actions to close gaps
- Stored in DB per user + target role

#### Pathway Roadmap
- Personalised year-by-year career plan based on: degree, current year, target role, and gap analysis
- Example output: Y1: join societies, case competition teams; Y2: apply for insight programs, start networking; Y3: applications open Feb, target these 5 programs
- Includes Australian recruiting calendar for target sector (see Section 9)

> **MVP scope**: Role Explorer, Role Comparison, Skills Gap + Roadmap are required. Day-in-the-Life is V1 (requires founder content seeding).

---

### 5.2 Build

**Purpose**: Turn gaps into a strong application profile.

**All 4 sub-tools are MVP scope.**

#### CV & LinkedIn Builder
- Industry-specific CV templates
- AI bullet-point feedback: Claude rewrites weak bullets, suggests quantification, flags generic language
- Cover letter generator: tailored per role and company
- LinkedIn section-by-section optimisation advice

#### Cold Outreach Hub
- **5 templates**: cold alumni, cold recruiter, coffee chat follow-up, referral ask, thank-you note
- **Australian tone defaults**: warmer, more direct, less formal than UK/US. Shorter messages. Name-drop shared AU context (uni societies, AU sport, regional ties) where relevant
- Real-time AI feedback as the user drafts their message
- Contact tracker: name, role, company, LinkedIn URL, date contacted, reply status (sent / replied / no-response), lead warmth (warm/cold), follow-up date, notes

#### Application Tracker
- Log: company, role, URL, platform (LinkedIn/Seek/Handshake/direct), status, stage (applied / screening / interview / offer / rejected)
- Deadline and follow-up date fields
- Feedback notes field
- Visual status overview on Build page

#### Extra-Curricular Guide
- Role-specific activity recommendations with how-to guides
- Examples: case competitions (consulting), stock pitch competitions (finance/IB), Kaggle (data), open source (tech), pro bono consulting (law/strategy), accounting society (Big 4)
- Tailored to Australian university societies and competitions where possible

#### Weekly Goals + Accountability
- AI-generates 3–5 weekly goals every Monday based on current career stage and recent activity
- **Incomplete goal handling**: Claude surfaces a reflection prompt — "You didn't complete X last week — was it too ambitious, bad timing, or just busy?" — and adjusts next week's goals accordingly
- Streak tracking: days active in a row
- Milestone badges on key achievements (see Section 5.4)

---

### 5.3 Prepare

**Purpose**: Once a connection or interview is booked.

#### Coffee Chat Prep
- User pastes interviewer's LinkedIn bio or provides name/role/company
- Claude generates a **structured prep guide** using the following framework:
  1. **Background summary** — 3 things to know about this person
  2. **Questions to ask** — 4–6 tailored, non-generic questions
  3. **Topics to avoid** — based on role, seniority, and any signals in bio
  4. **How to open** — first 30 seconds
  5. **How to close** — asking for next steps without sounding transactional
  6. **Follow-up strategy** — message template + timing

**Worked examples** (informing system prompts):

> **IB example** — MD at Macquarie Capital, 15 years experience, ex-Goldman, posted on LinkedIn about deal flow in AU infrastructure sector
> - Ask about: career path from analyst to MD, what surprised them about the AU market vs. US
> - Avoid: asking about compensation, don't ask generic "what's your day like" questions
> - Close: "Would it be okay to reach out if I have more specific questions as I learn more about the space?"

> **Consulting example** — Senior Manager at BCG Sydney, ex-Bain, specialises in consumer retail
> - Ask about: how the AU consulting market differs from global offices, advice for building a case interview skill set while still studying
> - Avoid: asking for a referral directly in the first chat
> - Close: "I'd love to stay in touch as I continue preparing — is email the best way?"

#### Coffee Chat Tracker
- Log chats: contact, role, company, date, outcome (great / okay / no follow-up needed), thank-you sent (yes/no), follow-up notes

#### Interview Prep

**Standout format**: Behavioural (STAR). This is the most common format students fail. Launchpad goes deeper here than any other tool.

**Interview types supported**: Behavioural, Technical, Case, Group, Assessment Centre

**Scoring rubric** (type-dependent):

| Type | Dimensions |
|------|-----------|
| Behavioural | STAR compliance, Relevance, Specificity, Conciseness, Impact stated |
| Case | Framework quality, Numeracy, Hypothesis-driven approach, Communication |
| Technical | Correctness, Clarity, Edge case awareness |
| Group / AC | Contribution, Listening, Leadership signals, Written task quality |

- Questions tailored to: role, company, interview type, **and the user's own stated experience from their profile** — this is the primary personalisation surface for V1
- Question-by-question flow with scored feedback after each answer
- Overall session score + key improvement areas

#### Audio Coaching (Core Differentiator)
1. User clicks "Record Answer"
2. `MediaRecorder` captures audio; Web Speech API runs live transcript in parallel
3. On stop: transcript sent to `/api/prepare/audio-feedback` with context (role, question, type)
4. Claude analyses for: content quality, STAR structure, tone, filler words, confidence signals, conciseness, rapport
5. Feedback panel shows: transcript, dimension scores, highlighted filler words, specific improvement notes

#### Internship Success Guide
- Surfaced when offer badge is earned
- Covers: first impressions, dress code, internal networking, how to add value quickly, professionalism norms, how to ask for a return offer
- Australianised: casual Fridays, "arvo" drinks culture, flatter hierarchy outside of banking

---

### 5.4 Gamification Layer

**Philosophy**: Motivate through progress and recognition. No dark patterns, no guilt-tripping. Badges and streaks celebrate real milestones; they never block features or punish inaction.

#### Milestone Badges

| Slug | Badge | Trigger |
|------|-------|---------|
| `skills_gap_done` | Self-Aware | Completed skills gap analysis |
| `first_outreach` | First Outreach | Sent first cold message |
| `cv_started` | CV Builder | Started CV in the builder |
| `first_application` | First Application | Logged first job application |
| `first_coffee_chat` | Coffee Chat | Booked/logged first coffee chat |
| `first_interview_prep` | Interview Ready | Completed first mock interview |
| `audio_practice` | Voice Coach | Used audio feedback feature |
| `offer_received` | Offer Received | Offer stage reached |

#### Streaks
- Day streak: active on the platform on consecutive days
- Longest streak tracked for profile display

#### Career Progress Bar
- 5-step visual bar on dashboard: Exploring → Building → Applying → Preparing → Offer
- Current stage highlighted; completed stages shown in green

#### Weekly Goals Panel
- Dashboard card showing this week's 3–5 AI-suggested micro-tasks with checkboxes
- Incomplete goals trigger a reflection prompt the following Monday

---

## 6. Design System

**Aesthetic**: Dark, minimalist, premium. Mature SaaS — not startup-y.

### Colour Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--navy` | `#060606` | Page background |
| `--navy-light` | `#0f0f0f` | Input backgrounds |
| `--navy-card` | `#131313` | Card backgrounds |
| `--white` | `#f8fafc` | Primary text, buttons |
| `--muted` | `#8a8a8a` | Secondary text, labels |
| `--border` | `rgba(255,255,255,0.07)` | Subtle borders |
| `--border-strong` | `rgba(255,255,255,0.14)` | Active/hover borders |
| `--green` | `#4ade80` | Success states |
| `--gold` | `#f59e0b` | Warning, badges |
| `--red` | `#f87171` | Error states |

### Typography

| Role | Font | Weight |
|------|------|--------|
| Hero headlines | Cormorant (serif) | 600 italic |
| Section headings (h2) | DM Sans | 600 |
| UI labels, nav (h3) | Syne | 700 |
| Body, inputs | DM Sans | 400–500 |

### Key Components
- **`.feature-card`**: CSS conic-gradient glow border on hover (mouse-tracking via `glow.js`)
- **`.stat-card`**: Icon + large number + label, used on dashboard stats row
- **`.milestone-badge`**: Earned (full colour) vs. locked (dimmed) state
- **`.pill`**: Coloured status chips (green/gold/indigo/muted)
- **`.progress-wrap / .progress-fill`**: Horizontal progress bar for scores
- **Globe hero**: Three.js wireframe sphere on landing page (`globe.js`)

---

## 7. Tech Stack

### Backend

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.115+ |
| Database | SQLite 3 (file: `career_assistant.db`) |
| ORM | Raw SQLite3 with helper functions in `database.py` |
| AI | Anthropic API — `claude-sonnet-4-6` |
| Automation | Playwright 1.50+ (semi-automated job pre-fill) |
| Python | 3.13 |

### Frontend

| Component | Technology |
|-----------|-----------|
| Framework | Vanilla HTML/CSS/JavaScript (no build tooling) |
| 3D | Three.js 0.160 (CDN) |
| Speech | Web Speech API (browser-native) |
| State | localStorage for session; server DB for persistent data |
| Fonts | Google Fonts (Cormorant, DM Sans, Syne) |

### Infrastructure (current / target)
- **Local**: `uvicorn main:app --reload` at `http://127.0.0.1:8000`
- **Static files**: served by FastAPI from `/static/`
- **Target deploy**: Render, Railway, or Fly.io with persistent SQLite volume

### Environment Variables (`.env`)
```
ANTHROPIC_API_KEY=
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=
INDEED_EMAIL=
INDEED_PASSWORD=
```

---

## 8. Database Schema

### `users`
```
id, name, email, password_hash, degree, university, year_of_study,
target_sector, career_stage, skills, experience, target_roles,
location, personality_notes, created_at
```

### `role_profiles`
```
id, title, sector, description, typical_hours, avg_salary_aud,
exit_opportunities, work_life_balance, skills_required, day_in_life,
human_reviewed (bool), last_updated
```

### `testimonials`
```
id, role, submitter_name, submitter_company, submitter_years_exp,
content, approved (bool), ai_screened (bool), created_at
```

### `skills_gaps`
```
id, user_id, target_role, gap_analysis (JSON), roadmap (JSON), created_at
```

### `outreach_contacts`
```
id, user_id, name, role, company, linkedin_url, date_contacted,
reply_status, lead_warmth, follow_up_date, notes
```

### `applications`
```
id, user_id, job_title, company, url, platform, status, stage,
deadline, feedback, follow_up_date, created_at
```

### `coffee_chats`
```
id, user_id, contact_name, contact_role, contact_company,
scheduled_date, outcome, thank_you_sent, follow_up_notes
```

### `interview_sessions`
```
id, user_id, role, company, interview_type, questions (JSON),
answers (JSON), scores (JSON), overall_score, created_at
```

### `milestones`
```
id, user_id, badge_slug, badge_name, badge_description, earned_at
```

### `weekly_goals`
```
id, user_id, week_start, goals (JSON array of {task, category, estimated_mins, completed})
```

### `streaks`
```
id, user_id, current_streak, longest_streak, last_active_date
```

---

## 9. Australian Recruiting Calendar

| Month | Event |
|-------|-------|
| February | Big 4 graduate and vacation programs open (Deloitte, PwC, KPMG, EY) |
| Feb–March | Investment bank internship applications open (Macquarie, UBS, Goldman AU, JPMorgan) |
| March | Consulting firm applications open (BCG, McKinsey, Bain, Oliver Wyman) |
| April | Most major programs close. Assessment centres begin |
| May–June | Offers and rejection waves |
| July | Mid-year intake internship programs (smaller cohort) |
| August–September | Early applications for following year begin at some firms |
| October–November | Some grad programs (tech, government) open for following year |

This calendar surfaces in the Roadmap feature and as contextual nudges in weekly goals.

---

## 10. AI Cost Control Strategy

### Cache Layer
- Role profiles cached in `role_profiles` table on first generation — subsequent loads skip the AI call
- Outreach templates cached per scenario type — regenerated only on explicit user request
- Roadmaps cached per user + target role in `skills_gaps` table

### Rate Limits (by tier)

| Feature | Free | Paid |
|---------|------|------|
| Role Explorer / CV feedback | Unlimited | Unlimited |
| Interview mock sessions | 3/week | Unlimited |
| Audio coaching sessions | 2/week | Unlimited |
| Coffee chat prep | 5/month | Unlimited |
| Outreach feedback | 10/month | Unlimited |
| Weekly goals generation | Auto (Monday) | Auto + manual refresh |

---

## 11. Monetisation

### Freemium Model
- **14-day full-access trial** on signup (no credit card required)
- After trial: hybrid gating
  - **Always free**: Role Explorer, CV bullet feedback, Application Tracker, basic Outreach templates
  - **Usage-gated free**: Mock interviews (3/week), audio coaching (2/week), coffee chat prep (5/month)
  - **Paid only**: Unlimited AI calls, advanced interview scoring, priority response times

### Pricing (indicative)
- Student plan: ~AU$15/month or AU$79/semester
- Annual: AU$99/year

### University B2B
- **Offering**: White-labelled Launchpad instance with university branding + cohort analytics dashboard
- **Analytics for careers services**: anonymised data — which sectors students target, application rates, offer conversion, most-used features
- **Pricing**: Per-institution licence, pitched to university careers services

---

## 12. Authentication & Privacy

### Auth (V1)
- Email + password (bcrypt hashed)
- Google OAuth and LinkedIn OAuth
- Server-side sessions (JWT or signed cookie) replacing the current localStorage userId approach

### Privacy Commitments (non-negotiable)
- Students share highly sensitive data: interview answers, salary expectations, personal struggles
- No selling or sharing of personal data with third parties, including employers
- CV and interview data is never used to train AI models
- Clear privacy policy surfaced at signup

### Data Retention
- Inactive accounts (no login for 12 months): flagged as inactive
- Auto-purge after 12 months of inactivity, with one email warning sent 30 days prior
- Users can delete their account and all associated data at any time

---

## 13. Notifications

### Email
- Weekly goals reminder (Monday morning)
- Follow-up reminder when `follow_up_date` is due (outreach contacts + coffee chats)
- Streak warning if inactive for 2 days during active recruiting season
- Offer / milestone celebration email

### Push (PWA)
- Same triggers as email, delivered as browser push notifications
- Opt-in only, prompted after 3rd login

---

## 14. Frontend Pages

| File | Purpose | MVP? |
|------|---------|------|
| `index.html` | Landing page — globe hero, 3-step framework, feature details, CTA | Yes |
| `signup.html` | Account creation (email + OAuth) | Yes |
| `onboarding.html` | 10-step profile questionnaire | Yes |
| `tour.html` | First-visit walkthrough (mandatory, skippable, accessible from profile) | Yes |
| `dashboard.html` | Home: goals, streak, stats, badges, quick nav | Yes |
| `discover.html` | Role explorer, comparison, skills gap, roadmap | Yes |
| `build.html` | CV, outreach, contacts, applications, extra-curricular | Yes |
| `prepare.html` | Coffee chat prep, mock interview, audio coaching | Yes |
| `profile.html` | Edit profile, all badges, settings | Yes |
| `cv.html` | Legacy CV bot chat | No |
| `email.html` | Legacy email bot chat | No |
| `interview.html` | Legacy interview chat | No |
| `application.html` | Legacy auto-apply UI | No |

---

## 15. API Surface

| Router | Prefix | Key Endpoints |
|--------|--------|---------------|
| `user.py` | `/api/user` | Save profile, get by email, get by id |
| `discover.py` | `/api/discover` | Role list, compare, skills-gap, roadmap, simulate |
| `build.py` | `/api/build` | CV chat, outreach chat/template, contacts CRUD, applications CRUD, weekly goals |
| `prepare.py` | `/api/prepare` | Coffee chat prep, interview start/chat, audio feedback, follow-up, internship guide |
| `gamification.py` | `/api/gamification` | Dashboard stats, streaks, milestones |
| `testimonials.py` | `/api/testimonials` | Submit, list by role |
| `application.py` | `/api/application` | Job search, confirm/skip (semi-automated pre-fill) |

---

## 16. Roadmap

### MVP (current state)
- Core backend: all 11 DB tables, 3 specialist bots, all routers wired
- Frontend: all 9 core pages built with full design system
- Gamification: streaks, badges, weekly goals, career stage progress bar
- Globe hero on landing page (Three.js)
- Basic session via localStorage (temporary)

### V1 (next milestone)
- Proper auth: email + Google/LinkedIn OAuth, server-side sessions
- Deep personalisation: interview questions tailored to user's own profile experience
- Australian content layer: AU firms, AU salary data, AU recruiting calendar in roadmap
- Day-in-the-Life: founder-seeded professional stories for 10 priority roles
- Email notifications: follow-up reminders, weekly goal nudges
- 14-day trial flow: trial counter, paywall UI, Stripe integration
- Testimonial moderation: AI pre-screening + admin approval UI
- Mobile-responsive polish: tested on iOS Safari and Android Chrome

### V2 (growth phase)
- Native mobile app (React Native or Flutter)
- University B2B: white-label + cohort analytics dashboard
- Cross-device sync (full server-side session state)
- PWA push notifications
- Peer features: anonymised benchmarking ("students at your uni targeting IB average X applications")
- LinkedIn profile import for onboarding auto-fill
- Role content expansion: Law, Government, Startups, Non-profit

---

## 17. Success Metrics

**North star**: Offer rate — the percentage of active Launchpad users who land an internship.

**Supporting metrics**:
- Week-4 retention
- Features used per session (are students engaging with multiple modules?)
- Coffee chat prep → coffee chat logged conversion rate
- Mock interview sessions → application submitted correlation
- NPS after first week

**12-month target**: Measurable lift in offer rate vs. a control group of non-users.

---

## 18. Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Start server
py -3.13 -m uvicorn main:app --reload

# Open in browser
http://127.0.0.1:8000
```

### End-to-end test checklist
1. Landing page: globe renders, glow effect on feature cards works
2. Sign up → complete onboarding → redirected to tour → dashboard
3. Discover: compare 2 AU roles, generate a personalised roadmap
4. Build: generate a CV bullet, add an outreach contact, log an application
5. Prepare: paste a LinkedIn bio, get coffee chat prep, run a mock behavioural interview
6. Dashboard: streak increments, weekly goals appear, badge awarded on milestone action
7. DB check: `career_assistant.db` has records in all 11 tables
