"""
industries/_template.py

Copy this file to create a new industry config.
Example: cp _template.py law_firms_uk.py
Then fill in all the fields below and run:
  python scripts/scraper.py --industry law_firms_uk
"""

INDUSTRY_NAME = "your_industry_name"       # e.g. law_firms_uk (no spaces)
INDUSTRY_LABEL = "Human Readable Label"    # e.g. Law Firms (UK)

CITIES = [
    "London",
    # Add more cities
]

KEYWORDS = [
    "keyword one",
    "keyword two",
    # What would someone type into Google Maps to find this business?
]

COUNTRY = "UK"  # or "Nigeria", "Germany" etc.

PRODUCT_DESCRIPTION = (
    "Describe what you are selling to this industry in 1-2 sentences. "
    "This goes directly into the AI outreach prompt."
)

SCORING_CONTEXT = """
Describe what makes a HIGH, MEDIUM, and LOW value lead in this industry.
The AI analyzer uses this to score businesses accurately.

High score (70-100): [what does a perfect lead look like?]
Medium score (40-69): [what does a warm lead look like?]
Low score (0-39): [when should we skip this business?]
"""

OUTREACH_ANGLE = (
    "What pain point should the cold email focus on for this industry? "
    "What keeps these business owners up at night?"
)

CATEGORY_MAP = {
    "keyword one": "category_label",
    "keyword two": "category_label_2",
}
