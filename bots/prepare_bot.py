import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"


# ── Coffee Chat Prep ─────────────────────────────────────────────────────────

def prep_coffee_chat(contact_info: str, user_profile: dict, target_role: str) -> str:
    """Generate tailored coffee chat preparation based on the interviewer's background."""
    prompt = f"""An Australian student is preparing for a coffee chat. Generate personalised preparation advice.

Student:
- Name: {user_profile.get('name', 'N/A')}
- Degree: {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')}
- Target role: {target_role}
- Skills/experience: {', '.join(user_profile.get('skills', []))}

Person they're meeting:
{contact_info}

Australian context: Australian professional culture is generally warmer and more direct than UK/US. First-name basis is standard. "Arvo drinks" and casual catch-ups are common. Hierarchy exists but is less rigid outside of investment banking/law.

Provide:

## Background Summary
3 key things to know about this person before the chat.

## Questions to Ask
5-7 specific, thoughtful questions tailored to this person's background and role. Not generic questions — reference specifics from their profile. Avoid questions easily answered on Google.

## Topics to Avoid
What NOT to ask or bring up (e.g. salary, "can you refer me", anything already obvious from their public profile)

## How to Open
Opening 2-3 sentences that feel natural and set a warm Australian tone.

## How to Keep It Going
2-3 techniques to keep the conversation flowing if it stalls.

## How to End & Ask for Next Steps
Exact phrasing to close without sounding transactional. How to ask for a referral or follow-on introduction in an Australian-friendly way.

## Rapport Tips
Specific things from their background you can connect on authentically — shared city, shared uni, industry events they've spoken at, articles they've published."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def generate_followup_strategy(chat_details: dict, user_profile: dict) -> str:
    """Generate a personalised follow-up strategy after a coffee chat."""
    prompt = f"""An Australian student just had a coffee chat. Help them follow up effectively.

Student: {user_profile.get('name', 'N/A')}, targeting {chat_details.get('target_role', 'N/A')}
They spoke with: {chat_details.get('contact_name', 'N/A')}, {chat_details.get('contact_role', 'N/A')} at {chat_details.get('contact_company', 'N/A')}
Outcome: {chat_details.get('outcome', 'N/A')}
Key topics discussed: {chat_details.get('topics_discussed', 'not specified')}

Australian tone: warm, direct, not overly formal. Keep it genuine and personal.

Generate:

## Thank-You Message
A personalised thank-you email or LinkedIn message (ready to send, under 100 words). Reference something specific from the conversation. Australian-friendly tone — don't be overly effusive.

## Follow-Up Timeline
Specific dates/timing for follow-up touchpoints over the next 3 months.

## How to Stay on Their Radar
2-3 low-key ways to stay in touch without being annoying (e.g. engaging with their posts, sharing relevant AU industry news, commenting on articles)

## How to Ask for a Referral
When and how to ask — exact phrasing when the time is right, calibrated to the Australian context."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ── Interview Prep ───────────────────────────────────────────────────────────

INTERVIEW_SYSTEM = """You are a senior interview coach preparing candidates for competitive internship interviews at top Australian and global firms. You are direct, rigorous, and give honest feedback.

You run structured mock interview sessions:
1. When asked to start, generate 5-8 role-specific questions for the interview type
2. Ask questions one at a time — wait for the candidate's answer before asking the next
3. After each answer, assess it using the rubric for this interview type (score 1-5 per dimension):

BEHAVIOURAL interviews — assess on:
- STAR Compliance: Situation/Task/Action/Result clearly structured
- Relevance: Does the example actually answer the question asked?
- Specificity: Concrete details, not vague generalisations
- Conciseness: No rambling; appropriate length (60-90 seconds spoken)
- Impact: Is the result/outcome clearly stated and meaningful?

CASE interviews — assess on:
- Framework Quality: Structured, MECE approach to the problem
- Numeracy: Mental maths accuracy and confidence
- Hypothesis-Driven: Does the candidate lead with a hypothesis, not just analyse?
- Communication: Can they walk the interviewer through their thinking clearly?
- Insight: Do they reach a meaningful recommendation, not just describe the problem?

TECHNICAL (Finance) — assess on:
- Conceptual Accuracy: DCF, LBO, M&A rationale, valuation multiples correct?
- Numerical Reasoning: Can they do rough mental maths on the fly?
- Practical Judgement: Do they understand when/why you'd use each technique?
- Communication: Can they explain complex concepts simply?

TECHNICAL (Tech/CS) — assess on:
- Correctness: Is the solution/approach technically sound?
- Clarity: Can they explain their reasoning step-by-step?
- Edge Cases: Do they consider boundary conditions and error handling?
- Code Quality (if applicable): Clean, readable, efficient approach?

TECHNICAL (Law) — assess on:
- Issue Spotting: Can they identify the key legal issues quickly?
- Legal Reasoning: IRAC structure (Issue, Rule, Application, Conclusion)
- Commercial Awareness: Understanding of how law applies to business context
- Communication: Clear, precise language without unnecessary jargon?

GROUP / ASSESSMENT CENTRE — assess on:
- Contribution: Quality and frequency of contributions
- Listening: Do they build on others' points?
- Leadership Signals: Do they help structure the group without dominating?
- Written Task Quality (if applicable): Clear, concise, structured under time pressure?

Format your assessment exactly like this after every answer:
---ASSESSMENT---
[List the 4-5 dimensions relevant to this interview type]
Dimension: X/5 — [one sentence of feedback]
...repeat for each dimension...
Overall: [2-3 sentences: most important improvement + what was done well]
---END---

At the end of the session provide:
---SUMMARY---
Overall Score: X.X/5
Strengths: [bullet list]
Areas to Improve: [bullet list]
Top Tip: [single most impactful thing to work on]
---END---

Australian context knowledge:
- Behavioural: STAR method, "why Australia/this firm", commercial awareness of AU market
- Case (Consulting): Common AU case topics — superannuation, mining/resources, healthcare reform, retail disruption, fintech
- Finance Technical: AU-specific — negative gearing, franking credits, ASX mechanics, RBA rate decisions
- Tech: Common at AU tech firms (Atlassian, Canva) — product thinking, system design, coding
- Law: Commercial awareness of AU legal market, clerkship dynamics, transactional vs. litigation
- Assessment Centre: Common in AU Big 4, law firms, government graduate programs

Be rigorous. A 5/5 should be genuinely excellent. Don't be sycophantic."""


def start_interview_session(role: str, company: str, interview_type: str,
                             interviewer_info: str = "", user_profile: dict | None = None) -> str:
    system = INTERVIEW_SYSTEM
    if user_profile:
        system += f"""

Candidate:
- Name: {user_profile.get('name', 'N/A')}
- Degree: {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience', [])}
- Target sector: {user_profile.get('target_sector', 'N/A')}

Tailor questions to their background where relevant. Reference their actual experience in follow-up probes."""

    if interviewer_info:
        system += f"\n\nInterviewer background (use to personalise where appropriate):\n{interviewer_info}"

    prompt = (
        f"Start a {interview_type} interview for a {role} internship"
        + (f" at {company}" if company else "")
        + ". Introduce yourself briefly as the interviewer, then ask the first question."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def interview_chat(messages: list[dict], user_profile: dict | None = None) -> str:
    system = INTERVIEW_SYSTEM
    if user_profile:
        system += f"""

Candidate:
- Name: {user_profile.get('name', 'N/A')}
- Degree: {user_profile.get('degree', 'N/A')} at {user_profile.get('university', 'N/A')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience', [])}
- Target sector: {user_profile.get('target_sector', 'N/A')}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def analyse_audio_transcript(transcript: str, context: dict) -> str:
    """Analyse a speech transcript and give communication coaching feedback."""
    prompt = f"""Analyse this spoken answer transcript and give communication coaching feedback.

Context:
- Type: {context.get('type', 'interview answer')} (coffee chat / interview)
- Role: {context.get('role', 'N/A')}
- Question/topic: {context.get('question', 'N/A')}

Transcript:
\"\"\"{transcript}\"\"\"

Provide feedback on:

## Content Quality
Was the answer substantive? Did it address the question? Key points missing?

## STAR Structure (if interview answer)
Did they give a clear Situation → Task → Action → Result? Where did it break down?

## Tone & Confidence
Did they sound confident? Any hedging language ("kind of", "I think maybe", "sort of")? Too formal / too casual for Australian professional norms?

## Rapport & Curiosity Signals
Did they sound genuinely interested? Any moments that built connection?

## Filler Words & Pacing
List any filler words detected (um, uh, like, you know, sort of, basically). Was the pace appropriate?

## Structure & Clarity
Was it well-organised? Clear beginning, middle, end? Easy to follow?

## Top 2 Improvements
The two most impactful changes they could make for next time.

## What Was Strong
Acknowledge genuine strengths — be specific, not generic."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def parse_scores_from_response(response_text: str) -> dict | None:
    """Extract structured scores from the assessment block if present."""
    if "---ASSESSMENT---" not in response_text:
        return None
    try:
        block = response_text.split("---ASSESSMENT---")[1].split("---END---")[0].strip()
        scores = {}
        for line in block.split("\n"):
            line = line.strip()
            # Match lines like "Content: 4/5 —" or "STAR Compliance: 3/5 —"
            if ":" in line and "/5" in line:
                parts = line.split(":")
                dim_name = parts[0].strip().lower().replace(" ", "_")
                score_part = parts[1].strip()
                # Extract the number before /5
                score_str = score_part.split("/")[0].strip()
                try:
                    scores[dim_name] = int(score_str)
                except ValueError:
                    pass
        # Also look for legacy format keys
        if "content" not in scores and "star_compliance" not in scores:
            return None
        return scores if scores else None
    except Exception:
        return None


# ── Internship Success Guide ─────────────────────────────────────────────────

def get_internship_guide(role: str, company: str, user_profile: dict) -> str:
    """Generate personalised advice for making the most of an Australian internship."""
    prompt = f"""An Australian student has just landed an internship as a {role}{f' at {company}' if company else ''}.

Student: {user_profile.get('degree', 'N/A')} student at {user_profile.get('university', 'N/A')}

Give them a comprehensive guide to making the most of their internship and securing a return offer.
Apply Australian workplace culture norms throughout (casual Fridays are standard, first-name basis is universal, "arvo drinks" happen, flat hierarchy exists outside banking/law, feedback culture is direct but constructive).

## First Week: First Impressions
Specific actions in the first 5 days. What to do, what to avoid. Australian-specific norms.

## Building Internal Relationships
How to network within the firm — who to meet, how to approach them, what to ask.
In Australia, grabbing a coffee with colleagues is completely normal to suggest early.

## Delivering Great Work
What "excellent intern" looks like in this specific role/sector. Be specific to {role}.

## Getting a Return Offer
The factors that most determine return offer decisions in this industry in Australia.
What interns typically get wrong.

## Professionalism & Culture
Specific norms for this role/sector in Australia. What to observe in week 1.
How Australian workplace culture differs from what students might expect.

Be specific to {role}. Not generic advice — real, actionable guidance for this industry in Australia."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
