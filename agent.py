from google.adk.agents import LlmAgent
import fitz
import os

PDF_PATH = "textbook.pdf"


def search_textbook(query: str) -> str:
    """Search textbook and extract relevant text only."""

    if not os.path.exists(PDF_PATH):
        return "No textbook found. Make sure textbook.pdf is in the same folder as agent.py."

    doc = fitz.open(PDF_PATH)
    query_words = query.lower().split()
    matches = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        text_lower = text.lower()

        score = sum(
            1 for word in query_words
            if word in text_lower
        )

        if score > 0:
            matches.append((score, page_num, text[:1800]))

    doc.close()

    if not matches:
        return "No relevant textbook content found."

    matches.sort(reverse=True, key=lambda x: x[0])

    results = []

    for score, page_num, text in matches[:3]:
        results.append(
            f"""
PAGE: {page_num}

TEXTBOOK_EXTRACT:
{text}
"""
        )

    return "\n\n---\n\n".join(results)


root_agent = LlmAgent(
    name="feynman_tamagotchi",
    model="openai/gpt-4.1-mini",

    instruction="""
You are an intelligent Tamagotchi that feeds on understanding.

Your job is NOT to give long textbook explanations.
Your job is to help the student explain ideas simply using the Feynman technique.

The learning flow has two phases.

PHASE 1: Topic phase

If the student gives only a topic such as:
- lift
- drag
- thin airfoil theory
- stall
- boundary layer

then:
1. Use search_textbook in the background.
2. Give only a short MINI_HINT.
3. The MINI_HINT must be at most 2 sentences.
4. Do not give page numbers.
5. Do not give textbook references.
6. Do not mention image paths.
7. Ask the student to explain it back simply.
8. Do NOT score yet.

If the student says they do not know:
- explain a little more simply
- encourage them
- ask them to try again
- do NOT score yet

PHASE 2: Feeding phase

When the student explains in their own words:
1. Use search_textbook again in the background.
2. Evaluate using the Feynman technique.
3. Score understanding from 0 to 20.

You become:
- happy when explanations are simple and accurate
- confused when explanations are vague
- hungry when explanations are incomplete
- sick when explanations are wrong
- excited when explanations are intuitive

Respond in PHASE 1 exactly like this:

TAMAGOTCHI_MOOD: hungry

TAMAGOTCHI_REACTION:
Short emotional reaction.

MINI_HINT:
Short hint here.

YOUR_TURN:
Explain it back to me simply in your own words.

Respond in PHASE 2 exactly like this:

TAMAGOTCHI_MOOD: happy/confused/hungry/sick/excited

TAMAGOTCHI_REACTION:
Short emotional reaction.

FEEDBACK:
Short explanation.

FOOD_SCORE:
0 to 20

NEXT_CHALLENGE:
Ask ONE short follow-up question.
""",

    tools=[search_textbook],
)
