Iată o variantă actualizată și profesională pentru `README.md`. Am rescris complet secțiunile de „Usage” și „Features” pentru a reflecta faptul că aplicația are acum o **Interfață Grafică (GUI)**, **Bază de date**, **Sentiment Analysis**, **Audio**, și funcționează și în **Limba Română**.

Poți da copy-paste direct pe GitHub:

---

# 🕵️‍♂️ LYAR: Forensic Linguistic Intelligence Suite

**LYAR (Linguistic Yield Analysis & Risk)** is a professional, GUI-based Python application designed for Forensic Statement Analysis. By utilizing advanced NLP techniques, RegEx-driven pattern matching, and sentiment analysis, LYAR identifies linguistic markers associated with deception, cognitive load, emotional state, and information withholding.

Formerly a terminal-based tool, LYAR is now a complete desktop application built for investigators, HR professionals, journalists, and researchers.

## ✨ Key Features (Version 6.0)

* 🖥️ **Modern Graphical Interface:** Intuitive, tab-based desktop app (built with Tkinter) requiring no coding knowledge to operate.
* 🌍 **Bilingual Support:** Native analysis engines for both **English** and **Romanian** statements.
* 🎤 **Audio Transcription:** Direct support for `.wav` files. The app automatically transcribes speech to text and analyzes it instantly.
* 🧠 **Sentiment & Tone Analysis:** Evaluates the psychological tone of the text (Positive, Negative, Neutral) to detect defensiveness or artificial friendliness.
* 🗄️ **Case Database & History:** Built-in SQLite database that automatically saves all analyses with unique `CASE ID`s. Search, retrieve, or delete past cases easily.
* 📄 **Professional Reporting:** * Export "Police-Style" **PDF reports** ready for physical case files.
* Export **HTML Dashboards** with color-coded "Red Flag" highlighting.


* ⚖️ **A/B Comparative Analysis:** Side-by-side credibility assessment of two different versions of the same event.
* 📂 **Batch Processing:** Point the app to a folder of `.txt` files to process dozens of statements at once, generating a Matplotlib risk distribution chart.

---

## 🔬 The Science Behind LYAR

The tool is based on established forensic linguistics protocols, such as Reality Monitoring (RM) and Scientific Content Analysis (SCAN). It tracks five critical indicators:

1. **Pronoun Density (Self-Reference):** Truthful statements usually have higher "I/Me" usage. A drop indicates *Linguistic Distancing*.
2. **Hedges:** Words like "maybe" or "I think" indicate a lack of commitment to the statement.
3. **Time Leaps:** Narrative "bridges" (e.g., "basically", "then", "later") often hide omitted details or "missing time".
4. **Qualifiers:** Phrases like "to be honest" or "frankly" are manipulative attempts to bolster credibility.
5. **Fillers:** Indicates increased *Cognitive Load* as the brain struggles to construct a fabricated narrative.

---

## 🚀 Installation & Setup

LYAR is completely cross-platform and works on Windows, macOS, and Linux.

**1. Clone the repository:**

```bash
git clone https://github.com/YourUsername/LYAR-Forensics.git
cd LYAR-Forensics

```

**2. Install required dependencies:**
Ensure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt

```

*(Note: LYAR runs entirely locally. The only module requiring internet access is the Google Speech-to-Text engine for audio processing).*

**3. Run the application:**

```bash
python lyar.py

```

---

## 💡 Usage Guide

Upon launching the application, you will find four main tabs:

1. **Analyze & Audio:** Paste text directly, load a `.txt` file, or load a `.wav` file. Click **ANALYZE** to get a real-time risk score (0-100), sentiment evaluation, and export options (PDF/HTML).
2. **Compare (A vs B):** Load two different statements. The engine will compare their linguistic metrics and output a statistical verdict on which is more credible.
3. **Batch Processing:** Select a directory containing multiple text files. LYAR will scan all of them, display a ranked table, and pop up a visual bar chart highlighting the highest-risk statements.
4. **History / Database:** Browse your previously analyzed statements, filter by keywords, re-read full texts, or re-export lost PDF reports.

---

## ⚠️ DISCLAIMER

This tool is intended for **research, educational, and investigative support purposes only**. LYAR is a statistical stylometry tool, not a lie detector. Forensic linguistic analysis should always be corroborated with physical evidence and interpreted by a qualified professional in a legal context.

---

**Author:** Unc Denis-Alexandru

**Version:** 6.0 (GUI Release)
