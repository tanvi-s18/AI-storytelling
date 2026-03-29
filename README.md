# SuspenseSpin
Team Name: Bombastic Blobfish

Template: Suspense Generation

## Repository File Architecture
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
