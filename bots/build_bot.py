import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"


# ── CV & Cover Letter ────────────────────────────────────────────────────────

CV_SYSTEM = """You are an expert career advisor and CV writer specialising in helping Australian university students land their first internships at top firms across all sectors — finance, consulting, law, tech, engineering, government, and beyond.

Your job:
1. Give concrete, actionable feedback on CV bullet points and structure
2. Write tailored, compelling cover letters specific to the target role and company
3. Provide LinkedIn profile optimisation advice (section by section)
4. Refine output based on user feedback

CV bullet point formula: Action verb + Task/Project + Quantified Result
Cover letter format: Hook (why this company specifically) → Value prop (what you bring) → Call to action
LinkedIn: Headline, About, Experience, Skills, Featured sections matter most

Australian context:
- Australian CV format: typically 1-2 pages, reverse chronological, no photo required
- Reference Australian firms and programs where relevant (Big 4, major law firms, tech companies like Atlassian/Canva, banks like Macquarie/ANZ)
- WGEA pay transparency norms — salary expectations are fair to include in cover letters for some sectors
- Many Australian grad programs open Feb–April; reference this when advising on timing

Be honest and direct. Don't sugarcoat weak points — give fixes.
Always ask for the target role and company before generating a cover letter."""


def cv_chat(messages: list[dict], user_profile: dict | None = None) -> str:
    system = CV_SYSTEM
    if user_profile:
        system += f"""

Student profile:
- Name: {user_profile.get('name', 'N/A')}
- Degree: {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')} ({user_profile.get('graduation_year', 'N/A')})
- Year: {user_profile.get('year_of_study', 'N/A')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience', [])}
- Target roles: {', '.join(user_profile.get('target_roles', []))}
- Target sector: {user_profile.get('target_sector', 'N/A')}
- Location: {user_profile.get('location', 'N/A')}

Use this profile as context. Always ask for the specific job description or company they are targeting before generating a cover letter."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return response.content[0].text


# ── Outreach / Cold Email ────────────────────────────────────────────────────

OUTREACH_SYSTEM = """You are a cold outreach strategist who has helped hundreds of Australian students land internships through targeted networking.

You write messages that get replies. Your approach for the Australian context:
- Keep messages under 150 words — busy professionals skim
- Australian networking culture is warmer and more direct than UK/US — match this tone
- Open with a specific, personalised hook (never "I hope this email finds you well")
- Lead with genuine interest and a specific reason for reaching out
- Name-drop shared Australian context where genuine (same university, same city, followed their work at [firm])
- End with a low-friction ask (15-minute call, not "let me know if there's an opening")
- Subject lines: specific, under 8 words
- LinkedIn messages: even shorter — under 100 words, no subject line needed

Scenarios you handle:
- cold_alumni: Reaching out to a uni alumnus at the target company
- cold_recruiter: Reaching out to a recruiter or hiring manager
- coffee_chat_followup: Following up after a coffee chat
- referral_ask: Asking someone to refer you for a role
- thank_you: Post-coffee-chat thank you note

When asked for a template: generate the message + subject line (if email) + a brief note on what makes it effective.
Give 2 variations (more formal / more conversational — Australian informal is warmer, not sloppy).
Provide real-time feedback when the user pastes a draft."""


def outreach_chat(messages: list[dict], user_profile: dict | None = None) -> str:
    system = OUTREACH_SYSTEM
    if user_profile:
        system += f"""

Student:
- Name: {user_profile.get('name', 'N/A')}
- Degree: {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience', [])}
- Target roles: {', '.join(user_profile.get('target_roles', []))}
- Target sector: {user_profile.get('target_sector', 'N/A')}"""

    # BUG FIX: was incorrectly using OUTREACH_SYSTEM instead of the enriched `system` variable
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def get_outreach_template(scenario: str, user_profile: dict, context: dict) -> str:
    """Generate a specific outreach template for a given scenario."""
    scenario_labels = {
        "cold_alumni": "cold message to a university alumnus",
        "cold_recruiter": "cold message to a recruiter or hiring manager",
        "coffee_chat_followup": "follow-up after a coffee chat",
        "referral_ask": "referral request",
        "thank_you": "thank-you note after a coffee chat or interview",
    }
    label = scenario_labels.get(scenario, scenario)

    prompt = f"""Write an Australian-style {label} template for this student.

Student: {user_profile.get('name', 'N/A')}, studying {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')}
Target role: {context.get('target_role', user_profile.get('target_roles', ['N/A'])[0] if user_profile.get('target_roles') else 'N/A')}
Target company: {context.get('company', 'N/A')}
Recipient: {context.get('recipient_name', 'N/A')} — {context.get('recipient_role', 'N/A')}
Additional context: {context.get('notes', 'none')}

Australian tone: warm, direct, not overly formal. Genuine and specific.

Provide:
1. Subject line (if email)
2. Version A (professional/formal — e.g. for senior bankers or partners)
3. Version B (warm/conversational — e.g. for analysts, associates, recent alumni)
4. A brief note on what makes each effective in the Australian context

Keep each message under 150 words."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ── Extra-Curricular Guide ───────────────────────────────────────────────────

def get_extracurricular_guide(target_role: str, user_profile: dict) -> str:
    """Recommend role-specific extra-curricular activities with Australian context."""
    prompt = f"""An Australian student is targeting {target_role} internships. Give them a guide to the most valuable extra-curricular activities for this specific path.

Student profile:
- Degree: {user_profile.get('degree', 'N/A')}
- Year: {user_profile.get('year_of_study', 'N/A')}
- Current skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience', [])}

For each recommended activity:
1. What it is and why it matters for {target_role} — in the Australian context
2. Specific Australian examples (named competitions, certifications, societies, platforms)
3. How to get started (concrete first step, including any Australian-specific resources)
4. How to present it on a CV

Include 4-6 activities ranked by impact. Be specific and Australian-focused:
- Finance: ASX-listed company pitch competitions, CFA Society student events, FINSIA, university Investment Society
- Consulting: MCA case competition, university consulting clubs, pro bono consulting
- Law: Moot court competitions, law review/journal, community legal centres, clerkship prep programs
- Tech: Atlassian hackathons, GovHack, university coding competitions, open source contributions
- Engineering: Engineers Australia student events, engineering design competitions, industry placements
- General: University societies relevant to the role, government graduate prep programs

Don't give generic advice — be specific to what will actually differentiate this student in Australia."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ── Weekly micro-tasks ───────────────────────────────────────────────────────

def generate_weekly_goals(user_profile: dict, recent_activity: dict) -> list[dict]:
    """Generate 3-5 specific weekly micro-tasks based on the user's current stage."""
    prompt = f"""Generate 3-5 specific weekly micro-tasks for this Australian student. Tasks must be concrete and completable in under 2 hours each.

Student:
- Target role: {', '.join(user_profile.get('target_roles', ['N/A']))}
- Target sector: {user_profile.get('target_sector', 'N/A')}
- Year: {user_profile.get('year_of_study', 'N/A')}
- Career stage: {user_profile.get('career_stage', 'exploring')}
- University: {user_profile.get('university', 'N/A')}

Recent activity:
- Applications sent: {recent_activity.get('applications', 0)}
- Contacts reached out to: {recent_activity.get('contacts', 0)}
- Coffee chats completed: {recent_activity.get('coffee_chats', 0)}
- CV last updated: {recent_activity.get('cv_updated', 'unknown')}

Reply with ONLY valid JSON array:
[
  {{"task": "specific task text", "category": "discover|build|prepare|networking", "estimated_mins": 30}},
  ...
]

Example good tasks:
- "Find 3 alumni from your university on LinkedIn who work at Macquarie Capital — send connection requests with personalised notes referencing your shared university"
- "Research MinterEllison's 2025 clerkship program — note the application open date and required documents"
- "Complete a free Atlassian product overview course to add to your LinkedIn skills section"
- "Write 3 new CV bullet points for your most recent role using the Action + Task + Result formula"

Example bad tasks: "Network more" or "Improve your CV" """

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()
    try:
        return json.loads(text)
    except Exception:
        return [{"task": "Update your CV with your most recent experience using the Action + Task + Result formula", "category": "build", "estimated_mins": 45}]
