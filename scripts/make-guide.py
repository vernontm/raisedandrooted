#!/usr/bin/env python3
"""
Build the full multi-page lead-magnet guide PDF:
"The Real Numbers Behind Your Child's Future" — Raised & Rooted Academy.

Page 1 is the branded ebook cover (image); the rest is typeset content
(research + comparison + 10 routines + enrollment questions + sources).
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Table, TableStyle, Image,
                                KeepTogether, NextPageTemplate, ListFlowable, ListItem)
from reportlab.lib.styles import ParagraphStyle

HERE = os.path.dirname(__file__)
A = os.path.join(HERE, "..", "assets")
F = os.path.join(HERE, "fonts")
OUT = os.path.join(A, "raised-and-rooted-free-guide.pdf")
COVER = os.path.join(A, "guide-cover-ebook.png")
LOGO = os.path.join(A, "logo-green-transparent.png")

# ---- Brand palette ----
GREEN_DEEP = HexColor("#2f4a32")
GREEN = HexColor("#4a6b46")
SAGE = HexColor("#7a9b6e")
CREAM = HexColor("#f7f3ea")
CREAM_DEEP = HexColor("#efe8d8")
TAN = HexColor("#e3dcc8")
TERRA = HexColor("#c77d4a")
TERRA_DEEP = HexColor("#a8602f")
INK = HexColor("#29302a")
MUTED = HexColor("#6b6f64")
GOLD = HexColor("#c79a3f")
RULE = HexColor("#ddd6c4")

# ---- Fonts ----
_fonts = {
    "FrR": "Fraunces-Regular.ttf", "Fr": "Fraunces-SemiBold.ttf",
    "FrB": "Fraunces-Bold.ttf", "FrI": "Fraunces-Italic.ttf",
    "NS": "NunitoSans-Regular.ttf", "NSsb": "NunitoSans-SemiBold.ttf",
    "NSb": "NunitoSans-Bold.ttf", "NSeb": "NunitoSans-ExtraBold.ttf",
}
for name, fn in _fonts.items():
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, fn)))
pdfmetrics.registerFontFamily("NS", normal="NS", bold="NSb", italic="NS", boldItalic="NSb")
pdfmetrics.registerFontFamily("Fr", normal="Fr", bold="FrB", italic="FrI", boldItalic="FrI")

W, H = letter
ML = MR = 62
HEADER_Y = H - 66
FOOTER_Y = 54

# ---- Paragraph styles ----
def style(name, **kw):
    return ParagraphStyle(name, **kw)

st_eyebrow = style("eyebrow", fontName="NSeb", fontSize=9.5, textColor=TERRA_DEEP,
                   leading=14, spaceAfter=8, tracking=2)
st_h1 = style("h1", fontName="FrB", fontSize=27, textColor=GREEN_DEEP, leading=31, spaceAfter=14)
st_h2 = style("h2", fontName="Fr", fontSize=16, textColor=GREEN_DEEP, leading=20,
              spaceBefore=14, spaceAfter=7)
st_body = style("body", fontName="NS", fontSize=10.7, textColor=INK, leading=16.5, spaceAfter=10)
st_body_c = style("bodyc", parent=st_body, alignment=TA_CENTER)
st_lead = style("lead", fontName="NS", fontSize=12.5, textColor=MUTED, leading=19, spaceAfter=12)
st_li = style("li", fontName="NS", fontSize=10.7, textColor=INK, leading=15.5, spaceAfter=6)
st_quote = style("quote", fontName="FrI", fontSize=14, textColor=GREEN, leading=20,
                 spaceBefore=4, spaceAfter=6)
st_card_num = style("cardnum", fontName="FrB", fontSize=27, textColor=TERRA_DEEP, leading=30)
st_card_lbl = style("cardlbl", fontName="NS", fontSize=8.7, textColor=INK, leading=12)
st_card_src = style("cardsrc", fontName="NSb", fontSize=7, textColor=SAGE, leading=9)
st_th = style("th", fontName="NSeb", fontSize=9.5, textColor=CREAM, leading=12)
st_th_us = style("thus", parent=st_th, textColor=HexColor("#fff7ee"))
st_td = style("td", fontName="NS", fontSize=9.3, textColor=INK, leading=12.5)
st_td_b = style("tdb", fontName="NSb", fontSize=9.3, textColor=GREEN_DEEP, leading=12.5)
st_td_us = style("tdus", fontName="NSb", fontSize=9.3, textColor=TERRA_DEEP, leading=12.5)
st_routine_h = style("rh", fontName="Fr", fontSize=14, textColor=GREEN_DEEP, leading=18, spaceAfter=3)
st_tip = style("tip", fontName="NSsb", fontSize=10, textColor=GREEN, leading=15, spaceAfter=4)
st_small = style("small", fontName="NS", fontSize=9, textColor=MUTED, leading=14, spaceAfter=6)
st_cta_h = style("ctah", fontName="FrB", fontSize=22, textColor=CREAM, leading=26, spaceAfter=10,
                 alignment=TA_CENTER)
st_cta_b = style("ctab", fontName="NS", fontSize=11, textColor=HexColor("#e9efe3"), leading=17,
                 alignment=TA_CENTER, spaceAfter=8)


# ---- Page furniture ----
def cover_page(c, doc):
    c.saveState()
    c.setFillColor(GREEN_DEEP)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    iw, ih = 1536, 2048
    h = H
    w = h * iw / ih
    c.drawImage(COVER, (W - w) / 2, 0, width=w, height=h, mask="auto")
    c.restoreState()


def content_page(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # header
    c.drawImage(LOGO, ML, H - 56, width=30, height=30, mask="auto", preserveAspectRatio=True)
    c.setFont("NSeb", 8)
    c.setFillColor(GREEN_DEEP)
    c.drawString(ML + 40, H - 46, "RAISED & ROOTED ACADEMY")
    c.setFont("NSb", 8)
    c.setFillColor(SAGE)
    c.drawRightString(W - MR, H - 46, "KATY, TX")
    c.setStrokeColor(RULE)
    c.setLineWidth(1)
    c.line(ML, HEADER_Y, W - MR, HEADER_Y)
    # footer
    c.line(ML, FOOTER_Y, W - MR, FOOTER_Y)
    c.setFont("NS", 8)
    c.setFillColor(MUTED)
    c.drawString(ML, 40, "The Real Numbers Behind Your Child's Future")
    c.drawRightString(W - MR, 40, str(doc.page))
    c.restoreState()


# ---- Reusable flowables ----
def hr(space_before=4, space_after=10, color=RULE, width=1):
    t = Table([[""]], colWidths=[W - ML - MR], rowHeights=[0.1])
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), width, color),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([Spacer(1, space_before), t, Spacer(1, space_after)])


def stat_cards(cards):
    row = []
    for num, label, src in cards:
        cell = [Paragraph(num, st_card_num), Spacer(1, 4),
                Paragraph(label, st_card_lbl), Spacer(1, 6),
                Paragraph(src, st_card_src)]
        row.append(cell)
    cw = (W - ML - MR) / 3
    t = Table([row], colWidths=[cw, cw, cw], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM_DEEP),
        ("BOX", (0, 0), (0, 0), 0, CREAM),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LINEAFTER", (0, 0), (-2, -1), 6, CREAM),
    ]))
    return t


def compare_table():
    head = [Paragraph("What matters to you", st_th),
            Paragraph("Typical public classroom", st_th),
            Paragraph("A micro school like ours", st_th_us)]
    rows = [
        ("Group size", "20–30+ students per teacher", "~6–10 students, low ratio"),
        ("Pace of learning", "Set to the middle of the room", "Set to your child"),
        ("Real-world skills", "Rarely taught directly", "Built into the week"),
        ("Is your child truly known?", "Often one of dozens", "Known by name, daily"),
        ("Character & confidence", "Incidental", "Intentional & modeled"),
        ("Family involvement", "Limited", "Partnership by design"),
    ]
    data = [head]
    for a, b, cc in rows:
        data.append([Paragraph(a, st_td_b), Paragraph(b, st_td), Paragraph(cc, st_td_us)])
    t = Table(data, colWidths=[(W - ML - MR) * 0.40, (W - ML - MR) * 0.31, (W - ML - MR) * 0.29])
    style_cmds = [
        ("BACKGROUND", (0, 0), (1, 0), GREEN_DEEP),
        ("BACKGROUND", (2, 0), (2, 0), TERRA),
        ("BACKGROUND", (2, 1), (2, -1), HexColor("#f5e9dd")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 0), (-1, -2), 0.6, RULE),
        ("ROWBACKGROUNDS", (0, 1), (1, -1), [CREAM, CREAM_DEEP]),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def callout(title, body):
    inner = [Paragraph(title, style("cot", fontName="NSeb", fontSize=10, textColor=TERRA_DEEP,
                                    leading=14, spaceAfter=4)),
             Paragraph(body, style("cob", fontName="NS", fontSize=10, textColor=INK, leading=15))]
    t = Table([[inner]], colWidths=[W - ML - MR])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#eef2e8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 13), ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
        ("LINEBEFORE", (0, 0), (0, -1), 3, SAGE),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 12)])


def routine(num, title, why, tip):
    head = Paragraph(f'<font name="FrB" color="#c77d4a">{num}</font>&nbsp;&nbsp;{title}', st_routine_h)
    why_p = Paragraph(why, st_body)
    tip_p = Paragraph(f'<font name="NSeb" color="#2f4a32">Try this:</font> {tip}', st_tip)
    return KeepTogether([head, why_p, tip_p, Spacer(1, 13)])


def cta_box(children):
    t = Table([[children]], colWidths=[W - ML - MR])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREEN_DEEP),
        ("LEFTPADDING", (0, 0), (-1, -1), 30), ("RIGHTPADDING", (0, 0), (-1, -1), 30),
        ("TOPPADDING", (0, 0), (-1, -1), 26), ("BOTTOMPADDING", (0, 0), (-1, -1), 26),
    ]))
    return t


def checklist(items):
    flow = []
    for it in items:
        row = Table([[Paragraph("✓", style("ck", fontName="NSeb", fontSize=11, textColor=GREEN)),
                      Paragraph(it, st_li)]], colWidths=[18, W - ML - MR - 18])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                 ("TOPPADDING", (0, 0), (-1, -1), 2),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        flow.append(row)
    return flow


# ---- Build the story ----
def build():
    S = []
    P = lambda t, s=st_body: S.append(Paragraph(t, s))
    sp = lambda h=6: S.append(Spacer(1, h))

    # Page 1: cover (drawn by template); switch to content afterward
    S += [NextPageTemplate("content"), Spacer(1, 1), PageBreak()]

    # --- Welcome ---
    P("A LETTER TO PARENTS", st_eyebrow)
    P("You are about to make the biggest bet of your child's life.", st_h1)
    P("Not their first job. Not their college. The classroom they sit in tomorrow morning. "
      "Over thirteen years your child will spend more than <b>15,000 hours</b> inside a learning "
      "environment, and decades of research keep pointing to the same uncomfortable truth: the "
      "environment becomes the outcome.", st_body)
    P("The good news is that you have more leverage than anyone has told you, both in the school "
      "you choose and in a handful of small things you can do at home starting tonight. This short "
      "guide gives you two things: the real numbers behind how kids actually do in different "
      "settings, and ten simple routines that quietly build a confident, well-spoken child.", st_body)
    P("No jargon. No fear-mongering. Just what the data says, and what to do about it.", st_body)
    S.append(Paragraph("— The team at Raised &amp; Rooted Academy, Katy, TX", st_quote))
    S.append(hr(10, 12))
    P("WHAT'S INSIDE", st_eyebrow)
    S += checklist([
        "<b>Part 1:</b> The numbers no one shows you, public, private, and micro school outcomes.",
        "<b>Part 2:</b> What actually moves the needle for a child.",
        "<b>Part 3:</b> 10 simple at-home routines that build communication and confidence.",
        "<b>Part 4:</b> The questions to ask before you enroll anywhere.",
    ])
    S.append(PageBreak())

    # --- Part 1: the numbers ---
    P("PART ONE", st_eyebrow)
    P("The numbers no one shows you", st_h1)
    P("It is easy to assume that an average school produces an average result, and that average is "
      "good enough. The data tells a harder story, and it starts with how many children are "
      "competing for one teacher's attention.", st_body)
    sp(4)
    S.append(stat_cards([
        ("69%", "of U.S. 8th graders score below proficient in reading on the national assessment.",
         "NAEP, The Nation's Report Card, 2022"),
        ("20–30+", "students one teacher manages in a typical public classroom.",
         "Nat'l Center for Education Statistics"),
        ("15,000", "hours your child spends in a learning environment, across 13 years.",
         "Avg. U.S. school day × K–12"),
    ]))
    sp(14)
    P("Why smaller is not just nicer, it is measurably better", st_h2)
    P("The single most studied lever in education is attention, how much of it each child actually "
      "receives. When you shrink the group, you change what is possible in the room.", st_body)
    sp(4)
    S.append(stat_cards([
        ("98th", "percentile reached by the average student tutored one-to-one vs. a conventional class, the famous “2 Sigma” effect.",
         "Bloom, Educational Researcher, 1984"),
        ("+4 mo.", "additional progress, on average, that small-group tutoring adds over a single school year.",
         "Education Endowment Foundation"),
        ("~2×", "faster progress under high-dosage, small-group instruction in large-scale studies.",
         "Nickow, Oreopoulos & Quan, NBER, 2020"),
    ]))
    sp(16)
    P("Public, private, and micro school, side by side", st_h2)
    P("It is not only about test scores. The size and intent of a learning environment shape a "
      "child's confidence, habits, and the everyday skills that schooling is supposed to build.", st_body)
    sp(4)
    S.append(compare_table())
    sp(14)
    S.append(callout(
        "The part that follows your child for life",
        "Research consistently links stronger academic achievement and school engagement with higher "
        "high-school completion, college enrollment, and adult earnings. School choice is not a "
        "guarantee, but it is one of the few levers with that kind of long-range association, which is "
        "exactly why it deserves real thought rather than a default."))
    sp(2)
    P("And then there is the part report cards never measure: real-world ability. The capacity to "
      "speak clearly, think through a problem, handle money, and recover from a setback. Those skills "
      "predict a good life as reliably as any grade, and they are rarely taught on purpose.", st_body)
    S.append(PageBreak())

    # --- Part 2 ---
    P("PART TWO", st_eyebrow)
    P("What actually moves the needle", st_h1)
    P("If you strip away the noise, almost everything that helps a child comes down to three things "
      "working together. A good school maximizes all three. So can a good home.", st_body)
    sp(2)
    P("1. Attention", st_h2)
    P("A child who is seen is a child who can be taught. When an adult notices what a specific child "
      "understands and what they do not, learning stops being a guess. This is the entire advantage "
      "of a small group, and at home it is simply time and eye contact.", st_body)
    P("2. The right level of challenge", st_h2)
    P("Growth happens just past the edge of what a child can already do, not far beyond it and not "
      "below it. Pacing set to the middle of a room misses most children most of the time. Pacing set "
      "to the child keeps them in the zone where effort pays off.", st_body)
    P("3. Practice that matters", st_h2)
    P("Skills become real through reps in situations the child cares about, explaining an idea, making "
      "a decision, owning a responsibility. The routines in Part 3 are built to manufacture those reps "
      "in the ordinary moments you already have.", st_body)
    sp(4)
    S.append(callout(
        "The takeaway",
        "You cannot personally re-create a school at home, and you do not need to. You need a handful of "
        "small, repeatable habits that deliver attention, the right challenge, and real practice. Here "
        "are ten."))
    S.append(PageBreak())

    # --- Part 3: routines ---
    P("PART THREE", st_eyebrow)
    P("10 routines that build a confident, well-spoken child", st_h1)
    P("Each takes only a few minutes. None require special materials. Pick two to start this week, "
      "then add more once they feel automatic.", st_lead)
    sp(2)

    routines = [
        ("01", "The ten-minute talk-it-through dinner",
         "Conversation is a skill, and skills need reps. A short, device-free meal where everyone shares "
         "one high and one low gives your child daily practice in organizing thoughts and listening.",
         "Go around the table: “best part of your day, hardest part, and why.” Let them finish without correcting."),
        ("02", "Narrate the why",
         "Children build reasoning by hearing it. When you think out loud, you hand them the language of "
         "cause and effect long before they could invent it themselves.",
         "Next decision you make, say it aloud: “I'm choosing this because…” Then ask what they would choose."),
        ("03", "The “tell me more” habit",
         "Yes-or-no questions get yes-or-no kids. Open follow-ups stretch a child's expressive language "
         "and teach them that their ideas are worth expanding.",
         "Replace “How was school?” with “Tell me about one thing that surprised you today.”"),
        ("04", "Read aloud, then retell",
         "Re-telling a story in their own words is comprehension, sequencing, and vocabulary all at once, "
         "and it works at every age.",
         "After a few pages or a chapter, ask: “If you were telling this to a friend, what just happened?”"),
        ("05", "One real responsibility",
         "Confidence is built from competence, not compliments. A job a child genuinely owns tells them, "
         "every day, that they are capable and needed.",
         "Hand over one daily task completely, feeding a pet, setting the table, and let them own the outcome."),
        ("06", "The two-minute pitch",
         "Persuasion is poise under a little pressure. Letting your child make a case, with reasons, builds "
         "structure, eye contact, and the nerve to ask for things well.",
         "When they want something, say: “Give me your two-minute pitch, with three reasons.”"),
        ("07", "Name the feeling first",
         "A child who can name an emotion can manage it instead of being managed by it. Labeling is the "
         "first step of self-control and self-advocacy.",
         "In a hard moment, offer words: “It looks like you're frustrated. Is that it?” Then wait."),
        ("08", "Money out loud",
         "Numeracy and judgment grow when numbers attach to real choices. Small, regular money decisions "
         "teach trade-offs no worksheet can.",
         "Give a tiny weekly budget for one real choice and let them feel the trade-off, even the wrong one."),
        ("09", "Boredom on purpose",
         "Self-direction and creativity only appear in unfilled time. A bored child who is not rescued by a "
         "screen learns to start, and finish, their own ideas.",
         "Protect one screen-free, unstructured stretch a day. Answer “I'm bored” with “great, what will you make?”"),
        ("10", "The bedtime reflection",
         "Three small questions turn a day into a lesson and build the growth mindset that carries a child "
         "through hard things.",
         "At lights-out ask: “What went well, what was hard, and what will you try differently tomorrow?”"),
    ]
    for num, title, why, tip in routines:
        S.append(routine(num, title, why, tip))

    S.append(callout(
        "Do not do all ten",
        "Two routines done for a month beat ten done for a week. Consistency is the active ingredient, "
        "the same reason a small class works: the same child, seen and stretched, again and again."))
    S.append(hr(10, 16))

    # --- Part 4: questions ---
    P("PART FOUR", st_eyebrow)
    P("The questions to ask before you enroll anywhere", st_h1)
    P("Whether you are considering us, another micro school, a private school, or staying put, these "
      "questions cut through the marketing and reveal how a school actually treats your child.", st_body)
    sp(6)
    S += checklist([
        "What is the real student-to-teacher ratio, on an average day, not on paper?",
        "How exactly do you adjust when a child is ahead, or behind, the rest of the group?",
        "Is progress measured by mastery and understanding, or by a pacing calendar?",
        "Which real-world skills, communication, problem-solving, money sense, are taught on purpose, and when?",
        "How, and how often, will I actually know how my child is doing?",
        "How are character, confidence, and resilience developed here, specifically?",
        "What does a typical day look like, hour by hour?",
        "What happens when a child struggles socially or academically, walk me through it?",
    ])
    sp(8)
    S.append(callout(
        "A simple test",
        "If the answers are specific, your child is likely to be specific to them too. If the answers are "
        "vague, your child is likely to be one of many. You are not being difficult by asking. You are "
        "being a parent."))
    S.append(PageBreak())

    # --- About + CTA ---
    P("ABOUT THE SCHOOL", st_eyebrow)
    P("Raised &amp; Rooted Academy", st_h1)
    P("We are a micro school in Katy, Texas, built around a simple idea: a child who is truly known is "
      "a child who can thrive. With just a handful of students per teacher, we challenge each child at "
      "their own level, teach the real-world skills the average classroom skips, and partner closely "
      "with families. Rigorous academics, real attention, and roots that hold for a lifetime.", st_body)
    sp(2)
    inner = [
        Paragraph("Now enrolling for August 2026", st_cta_h),
        Paragraph("We keep enrollment small on purpose, which means spots are limited. If this guide "
                  "resonated, the best next step is a simple conversation about your child, specifically.",
                  st_cta_b),
        Spacer(1, 6),
        Paragraph('<font name="NSeb" color="#f7f3ea">Visit&nbsp; raisedandrootedacademy.com'
                  '&nbsp;&nbsp;·&nbsp;&nbsp; Call (281) 555-0140</font>',
                  style("ctac", fontName="NSeb", fontSize=11.5, textColor=CREAM, alignment=TA_CENTER)),
    ]
    S.append(cta_box(inner))
    sp(10)
    P("Reply to the email that delivered this guide and tell us about your child. We read every one.",
      st_small)
    S.append(PageBreak())

    # --- Sources ---
    P("SOURCES & A NOTE", st_eyebrow)
    P("Where these numbers come from", st_h1)
    sources = [
        "Reading proficiency: National Assessment of Educational Progress (NAEP), “The Nation's "
        "Report Card,” 2022. Roughly two-thirds of 4th and 8th graders scored below the "
        "“proficient” benchmark.",
        "Class size: U.S. National Center for Education Statistics (NCES), public-school class-size and "
        "pupil/teacher-ratio reporting.",
        "One-to-one instruction: Benjamin S. Bloom, “The 2 Sigma Problem,” Educational "
        "Researcher, 1984.",
        "Small-group tutoring gains: Education Endowment Foundation (EEF), Teaching and Learning "
        "Toolkit, “Small group tuition.”",
        "High-dosage tutoring effects: Nickow, Oreopoulos & Quan, “The Impressive Effects of "
        "Tutoring on PreK–12 Learning,” NBER Working Paper, 2020.",
        "Long-term outcomes: a broad body of economics-of-education research associating achievement and "
        "educational attainment with later earnings and life outcomes.",
    ]
    S.append(ListFlowable(
        [ListItem(Paragraph(s, st_li), leftIndent=12, value="•") for s in sources],
        bulletType="bullet", start="•", leftIndent=14))
    sp(8)
    P("A note on the numbers: figures are drawn from public, widely cited sources and are presented as "
      "approximate, rounded for clarity. Studies vary in method and population, and education statistics "
      "are updated over time. Treat these as a well-supported picture of the landscape rather than "
      "precise guarantees, and follow the citations above to read the originals.", st_small)
    sp(14)
    S.append(hr(0, 10))
    P('<font name="Fr" color="#2f4a32" size="13">Raised &amp; Rooted Academy</font>'
      '&nbsp;&nbsp;·&nbsp;&nbsp; A micro school in Katy, TX &nbsp;&nbsp;·&nbsp;&nbsp; '
      "© 2026. All rights reserved.", st_small)

    return S


def main():
    doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=ML, rightMargin=MR,
                          topMargin=86, bottomMargin=64, title="The Real Numbers Behind Your Child's Future",
                          author="Raised & Rooted Academy")
    full = Frame(0, 0, W, H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="full")
    content = Frame(ML, FOOTER_Y + 8, W - ML - MR, HEADER_Y - (FOOTER_Y + 8) - 10, id="content")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[full], onPage=cover_page),
        PageTemplate(id="content", frames=[content], onPage=content_page),
    ])
    doc.build(build())
    print(f"Saved {OUT}  ({os.path.getsize(OUT)//1024} KB)")


if __name__ == "__main__":
    main()
