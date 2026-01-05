# LYAR: Forensic Linguistic Analysis
LYAR (Linguistic Yield Analysis & Risk) is a professional Object-Oriented Python tool designed for Forensic Statement Analysis. By utilizing advanced NLP techniques and RegEx-driven pattern matching, LYAR identifies linguistic markers associated with deception, cognitive load, and information withholding.

------------------------------------------------------------------------------

Key Features:

- Single Statement Analysis: Deep dive into a single text with real-time risk scoring.
- Comparative Analysis: Side-by-side credibility assessment of two different versions of the same event.
- Batch Processing: Analyze entire directories of statements and rank them by risk level.
- Visual Intelligence: Automated generation of risk distribution charts using Matplotlib.
- Professional Reporting: Export comprehensive HTML dashboards with color-coded "Red Flag" highlighting.
- Forensic Highlighting: Terminal-based ANSI highlighting for immediate context inspection.

-------------------------------------------------------------------------------

The Science Behind LYAR

The tool is based on established forensic linguistics protocols, such as Reality Monitoring (RM) and Scientific Content Analysis (SCAN). It tracks five critical indicators:

1. Pronoun Density (Self-Reference): Truthful statements usually have higher "I/Me" usage. A drop indicates Linguistic Distancing.
2. Hedges: Words like "maybe" or "I think" indicate a lack of commitment to the statement.
3. Time Leaps: Narrative "bridges" (e.g., "basically", "then") often hide omitted details or "missing time".
4. Negative Qualifiers: Phrases like "to be honest" or "frankly" are manipulative attempts to bolster credibility.
5. Fillers: Indicates increased Cognitive Load as the brain struggles to construct a fabricated narrative.

-------------------------------------------------------------------------------
Installation

Clone the repository: git clone https://github.com/yourusername/lyar-forensic-tool.git >> cd lyar-forensic-tool

Install dependencies: pip install matplotlib

-------------------------------------------------------------------------------
Usage

Run the main engine: python lyar.py

Menu Options:

Option 1: Paste a file path to see a detailed forensic report of a witness statement.
Option 2: Compare a suspect's first interview with their second one to find discrepancies.
Option 3: Point to a folder containing 50+ statements to find the top 3 most suspicious ones instantly.

--------------------------------------------------------------------------------
Terminal Report

The tool provides a structured table and a color-coded visual analysis:

Cyan: Foundational markers (Pronouns/Fillers)
Yellow: Low-to-mid risk markers (Hedges)
Red: High-risk manipulative markers (Qualifiers/Time Leaps)

HTML Dashboard: The exported HTML report provides a high-level summary for non-technical investigators, including a risk score from 0-100 and a conclusion

--------------------------------------------------------------------------------
DISCLAIMER

This tool is intended for research and educational purposes. Forensic linguistic analysis should always be interpreted by a qualified professional in a legal context

Author
Unc Denis-Alexandru
