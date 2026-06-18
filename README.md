Lead Agent Pro

An AI powered B2B lead generation engine that scrapes local businesses, scores them intelligently, and sends personalized outreach automatically. Switch industries with a single flag and the entire pipeline adapts.
Currently supports UK clinics, salons, restaurants, med spas, and more.

How it works
The pipeline runs in five sequential steps. Each step is a separate script so you can run them independently or chain them together.
Step 1 scrapes business listings for your chosen industry and location using SerpAPI.
Step 2 enriches each result by extracting contact emails and WhatsApp numbers from their websites.
Step 3 uses GPT-4o-mini to analyze each business and assign a lead score based on how likely they are to need your service.
Step 4 generates a personalized outreach message for every qualified lead, tailored to their specific business context.
Step 5 opens the dashboard where you can review leads, scores, and outreach status in one place.
Setup
Clone the repo and install dependencies:
bashpip install -r requirements.txt
cp .env.example .env
psql $DATABASE_URL -f schema.sql
Open .env and fill in your four API keys (SerpAPI, OpenAI, Neon PostgreSQL, and Gmail SMTP). The .env.example file has instructions for each one.
Running the pipeline
Pass --industry to every script to tell it which market to work with:
bashpython scripts/scraper.py --industry clinics_uk
python scripts/enricher.py
python scripts/analyzer.py --industry clinics_uk
python scripts/outreach.py --industry clinics_uk
python dashboard/app.py
Then open http://localhost:8000 to view your dashboard.
Lead scoring
The analyzer scores every lead from 0 to 100 based on signals like whether they rely on manual booking, have a WhatsApp presence, or already use a chatbot.
A score of 70 or above means the business is a strong fit and worth contacting immediately. Scores between 40 and 69 are warm leads worth following up on. Anything below 40 is already well-automated and not worth the effort.
Adding a new industry
Copy the template, fill in the cities, keywords, and scoring guide for your new market, and the entire pipeline works as-is:
bashcp industries/_template.py industries/law_firms_uk.py
python scripts/scraper.py --industry law_firms_uk
Same pipeline, new market, zero rewiring.
Stack
Python, SerpAPI, GPT-4o-mini (OpenAI), PostgreSQL (Neon), FastAPI, Gmail SMTP
