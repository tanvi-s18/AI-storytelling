# SuspenseSpin
Team Name: YOUR TEAM NAME  
Template: Suspense Generation

## Project Overview
SuspenseSpin is a crime-mystery story generation system that uses an iterative prompting
meta-controller. Instead of asking an LLM to write the whole story at once, the system:
1. Generates a crime setup
2. Builds a suspense frame around a protagonist, urgent goal, dire stakes, and countdown
3. Generates suspects and red herrings
4. Iteratively generates 15 plot points that escalate tension
5. Produces a final reveal
6. Retells the full story in fluent prose

## Why this matches the template
The suspense generation template requires an external iterative process that walks the LLM
through character creation, goal formation, rising obstacles, and a final retelling. This system
implements exactly that structure for a crime mystery.

## File Architecture
- `main.py`: entry point
- `controller.py`: iterative suspense meta-controller
- `llm_client.py`: API wrapper
- `prompts.py`: all prompts
- `models.py`: structured data classes
- `validator.py`: checks for minimum story requirements
- `storyteller.py`: formatting helper
- `utils.py`: save output files
- `outputs/`: generated runs

## How to Run
1. Create a virtual environment:
   `python -m venv venv`
2. Activate it:
   - Windows: `venv\\Scripts\\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install requirements:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`
5. Insert your OpenAI API key in `.env`
6. Run:
   `python main.py`

## If no API key is provided
The system falls back to a built-in mock story so the code still runs to completion.

## Expected Runtime
Typical run time with API:
- About 20 to 60 seconds depending on model speed and network latency

Typical run time without API:
- Under 2 seconds using fallback mode

## Cost
If using a paid OpenAI API model, cost depends on:
- number of prompts
- size of generated outputs
- model selected in `.env`

Cheaper model suggestion:
- `gpt-4o-mini`

## Exemplar Output
See `outputs/latest_story.txt` for:
- complete crime setup
- suspects and red herrings
- 15 labeled plot points
- final reveal
- retold story

## Notes on Plot Points
A plot point here is a substantial event that changes the state of the investigation.
The system generates at least 15 such plot points to satisfy the project requirement.

## Known Failure Cases
- weak or repetitive clues
- suspiciously obvious culprit
- tension plateau in middle plot points
- red herrings that distract too much or too little

## Architecture Explanation for Presentation
The code maps directly to the architecture diagram:
- Crime Generator -> `controller.py` + `prompts.py`
- Suspense Frame Generator -> `controller.py`
- Suspect/Red Herring Generator -> `controller.py`
- Iterative Plot Point Loop -> `controller.py`
- Story Validator -> `validator.py`
- Fluent Retelling Module -> `controller.py`