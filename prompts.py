SYSTEM_PROMPT = """
You are a story generation assistant for an AI story generation project.
You must generate structured crime-mystery content with suspense.
Be consistent across all outputs.
Keep plot points concrete and causally connected.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

CRIME_SETUP_PROMPT = """
Create a crime mystery setup in JSON with exactly these fields:
crime_type, victim, setting, culprit, motive, hidden_method, key_secret.

Important:
- Every field value must be a plain string.
- Do not use nested JSON objects.
- Do not return arrays.
- victim must be a single string like "Evelyn Harper, the museum curator"
- setting must be a single string like "Harper & Sons Museum in coastal Nova Scotia, just after sunset"
- culprit must be a single string like "Thomas Blake, the curator's professional rival"

Requirements:
- The culprit must not be obvious.
- The crime should support at least 15 plot points for solving it.
- The hidden method must connect to clues later.
- Make it non-trivial.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

SUSPENSE_FRAME_PROMPT = """
Given this crime setup:

{crime_setup}

Create a suspense frame in JSON with:
protagonist: {{name, role, trait, flaw}}
goal
dire_stakes
countdown

Requirements:
- The protagonist should be someone readers can care about.
- The goal must be urgent.
- The stakes must be severe if the goal is not achieved.
- The countdown should create time pressure.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

SUSPECTS_PROMPT = """
Given this crime setup:

{crime_setup}

Return JSON with exactly:
suspects: [strings]
red_herrings: [strings]

Important:
- Every suspect must be a plain string, not an object.
- Every red herring must be a plain string, not an object.
- Do not use nested JSON.
- Do not include fields like name, motive, clue, or explanation as nested keys.

Requirements:
- Include at least 3 suspects including the real culprit.
- Each suspect should appear to have means, motive, or opportunity.
- Include at least 2 misleading but plausible red herrings.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

NEXT_PLOT_POINT_PROMPT = """
You are generating the next plot point in a suspenseful crime mystery.

Crime setup:
{crime_setup}

Suspense frame:
{suspense_frame}

Suspects and red herrings:
{suspects_block}

Existing plot points:
{existing_points}


Generate the next plot point as JSON with:
index, title, content, obstacle, clue, suspicion_shift, tension_score


Requirements:
- This should advance the detective's attempt to solve the crime.
- Add or refine one clue.
- Increase or maintain suspense.
- Make success harder, narrower, or riskier.
- Avoid resolving the whole case too early.
- The plot point must be substantial.
- Keep continuity with previous events.
- tension_score must be an integer from 1 to 10 only.
- Do not use percentages.
- Do not use values above 10.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

FINAL_REVEAL_PROMPT = """
Given the following crime setup and plot points, write the final reveal.

Crime setup:
{crime_setup}

Plot points:
{plot_points}

Requirements:
- Explain who committed the crime.
- Explain how it was done.
- Explain why earlier clues mattered.
- Resolve the red herrings.
- Keep it coherent and satisfying.

IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""

RETELLING_PROMPT = """
Turn the structured plot points below into a fluent suspenseful mystery story.

Crime setup:
{crime_setup}

Suspense frame:
{suspense_frame}

Plot points:
{plot_points}

Final reveal:
{final_reveal}

Requirements:
- Keep all major facts consistent.
- Preserve suspense.
- Make the protagonist's danger and urgency clear.
- Write in polished prose.
- Do not remove major clues.

VERY IMPORTANT:
- Do NOT change the protagonist, setting, or core crime once defined.
- All outputs must remain consistent with the original crime setup.
- The culprit MUST remain the same unless explicitly specified.
"""