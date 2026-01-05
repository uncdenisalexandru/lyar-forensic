import re
import os
import matplotlib.pyplot as plt


class ForensicAnalyzer:
    def __init__(self):
        """Initialize linguistic markers database and reference baselines."""
        self.list_pronouns = ['i', 'me', 'my', 'mine', 'myself', "i'm", "i've", "i'd", "i'll", 'am']
        self.list_hedges = ['probably', 'maybe', 'perhaps', 'possibly', 'potentially', 'it seems', 'it appears',
                            'i think', 'i believe', 'i suppose', 'i guess', 'i assume', 'i imagine', 'kind of',
                            'sort of', 'somewhat', 'roughly', 'around', 'about', 'mainly', 'mostly',
                            'to the best of my knowledge', 'as far as i recall', 'i suspect']
        self.list_fillers = ['uh', 'um', 'er', 'ah', 'well', 'so', 'actually', 'literally',
                             'right', 'like', 'you know', 'i mean', 'let me see', 'how should i put it', 'you see',
                             'just']
        self.list_qualifiers = ['honestly', 'frankly', 'truthfully', 'to be honest', 'to tell you the truth',
                                'in all honesty', 'believe me', 'to be frank', 'i swear', 'hand on heart',
                                'to my recollection', 'for a fact', 'obviously', 'clearly', 'certainly']
        self.list_time_leaps = ['then', 'next', 'afterward', 'afterwards', 'after that', 'following that',
                                'subsequently', 'thereafter', 'later', 'later on', 'soon after', 'shortly after',
                                'suddenly', 'all of a sudden', 'out of nowhere', 'unexpectedly', 'at that point',
                                'eventually', 'finally', 'at last', 'after a while', 'some time later', 'fast forward',
                                'skipping ahead', 'long story short', 'anyway', 'basically', 'the next thing i knew',
                                'the next thing i remember', 'before i knew it']

        # Forensic Baselines for Deception Detection
        self.baselines = {
            'pronouns': 3.5,  # Low self-reference indicates distancing
            'hedges': 2.0,  # High hedging indicates uncertainty/evasiveness
            'time_leaps': 4.0,  # High temporal gaps indicate potential omissions
            'qualifiers': 0.5,  # Over-justifying truthfulness (convincing mode)
            'fillers': 2.5  # High cognitive load during fabrication
        }

    def _format_text(self, text):
        """Cleans text while preserving apostrophes for contractions."""
        lower = text.lower()
        return re.sub(r"[^\w\s']", '', lower)

    def _get_metrics(self, text):
        """Extracts statistical densities and identified keywords from source text."""
        formatted = self._format_text(text)
        words = re.findall(r'\b\w+\b', formatted)
        total_count = len(words)

        if total_count == 0: return None

        # Nested structure: 'densities' for math, 'found_words' for qualitative evidence
        results = {'densities': {}, 'found_words': {}}

        categories = {
            'p_den': self.list_pronouns,
            'h_den': self.list_hedges,
            'f_den': self.list_fillers,
            'q_den': self.list_qualifiers,
            't_den': self.list_time_leaps
        }

        for key, word_list in categories.items():
            # Build a safe Regex pattern for each category
            pattern = r'\b(' + '|'.join(re.escape(word) for word in word_list) + r')\b'
            matches = re.findall(pattern, formatted, re.IGNORECASE)

            # Calculate density percentage
            results['densities'][key] = (len(matches) / total_count * 100)
            # Store unique matches for evidence reporting
            results['found_words'][key] = list(set(matches))

        # Calculate weighted risk score
        results['risk_score'] = self._calculate_risk(results['densities'])
        results['total_words'] = total_count
        return results

    def _calculate_risk(self, res):
        """Weighted risk calculation based on forensic linguistics research."""
        score = 0
        if res['p_den'] < self.baselines['pronouns']: score += 25  # Linguistic Distancing
        if res['h_den'] > self.baselines['hedges']: score += 15  # Lack of Commitment
        if res['t_den'] > self.baselines['time_leaps']: score += 20  # Narrative Omission
        if res['q_den'] > self.baselines['qualifiers']: score += 30  # Manipulative Intent
        if res['f_den'] > self.baselines['fillers']: score += 10  # Cognitive Load
        return score

    def _get_status(self, score, baseline, is_below=False):
        """Determines the visual status label for each metric."""
        if is_below:
            return "[CRITICAL]" if score < baseline else "[OK]"   # pentru pronume, unde scorul trebuie sa fie cat mai mic
        else:
            return "[WARNING]" if score > baseline else "[OK]"  # pentru RESTUL

    def _get_conclusion(self, score):
        """Generates a qualitative forensic diagnostic based on the risk score."""
        if score >= 70: return "HIGH RISK: Strong indicators of deceptive content."
        if score >= 40: return "MODERATE RISK: Linguistic inconsistencies detected. Further interview recommended."
        return "LOW RISK: Statement appears linguistically consistent with truthful recall."

    def _get_highlighted_text(self, text, found_words_dict):
        """Applies ANSI color highlighting to detected 'Red Flag' words in console."""
        RED, YELLOW, CYAN, BOLD, RESET = "\033[91m", "\033[93m", "\033[96m", "\033[1m", "\033[0m"
        highlighted = text
        color_map = {'q_den': RED, 't_den': RED, 'h_den': YELLOW, 'p_den': CYAN, 'f_den': CYAN}

        all_words_to_color = []
        for key, words in found_words_dict.items():
            for w in words:
                all_words_to_color.append((w, color_map.get(key, RESET)))

        # Sort by length descending to prevent partial highlighting of phrases
        all_words_to_color.sort(key=lambda x: len(x[0]), reverse=True)

        for word, color in all_words_to_color:
            pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
            highlighted = pattern.sub(f"{BOLD}{color}\\1{RESET}", highlighted)
        return highlighted

    def print_report(self, text):
        """Displays a comprehensive forensic report in the terminal."""
        m = self._get_metrics(text)
        if not m: return

        dens = m['densities']
        data = [
            ("Pronoun Density", dens['p_den'], self.baselines['pronouns'], True),
            ("Hedge Density", dens['h_den'], self.baselines['hedges'], False),
            ("Time Leap Density", dens['t_den'], self.baselines['time_leaps'], False),
            ("Negative Qualifiers", dens['q_den'], self.baselines['qualifiers'], False),
            ("Filler Density", dens['f_den'], self.baselines['fillers'], False)
        ]

        print("\n" + "=" * 65)
        print("         LYAR FORENSIC LINGUISTIC ANALYSIS REPORT")
        print("=" * 65)
        print(f"{'INDICATOR':<25} | {'VALUE':<10} | {'BASELINE':<10} | {'STATUS':<12}")
        print("-" * 65)

        for name, val, base, is_below in data:
            status = self._get_status(val, base, is_below)
            base_str = f"< {base}%" if is_below else f"> {base}%"
            print(f"{name:<25} | {val:>9.2f}% | {base_str:<10} | {status:<12}")

        print("-" * 65)
        print(f"FINAL RISK SCORE: {m['risk_score']} / 100")
        print(f"CONCLUSION: {self._get_conclusion(m['risk_score'])}")
        print("-" * 65)
        print("FOR A VISUAL ANALYSIS GENERATE THE HTML FILE")
        print("-" * 65)


    def compare(self, text1, text2):
        """Compares two statements side-by-side to determine relative credibility."""
        m1, m2 = self._get_metrics(text1), self._get_metrics(text2)
        print("\n" + "=" * 65 + "\n             COMPARATIVE FORENSIC ANALYSIS\n" + "=" * 65)
        print(f"{'METRIC':<25} | {'ST. 1':<15} | {'ST. 2':<15}\n" + "-" * 65)
        print(f"{'Total Words':<25} | {m1['total_words']:<15} | {m2['total_words']:<15}")
        print(f"{'Risk Score':<25} | {m1['risk_score']:<15} | {m2['risk_score']:<15}\n" + "-" * 65)
        verdict = "Statement 1" if m1['risk_score'] < m2['risk_score'] else "Statement 2"
        print(f"VERDICT: {verdict} is LINGUISTICALLY MORE CREDIBLE.\n" + "=" * 65)

    def export_to_html(self, text, filename="Forensic_Report.html"):
        """Generates a professional HTML dashboard report including full metrics table and color legend."""
        m = self._get_metrics(text)
        if not m: return

        # 1. Prepare Text Highlighting
        highlighted_html = text
        # Define colors as a dictionary to reuse in legend
        colors = {
            'q_den': '#ffcccc',  # Light Red: Qualifiers
            't_den': '#ffd9b3',  # Light Orange: Time Leaps
            'h_den': '#ffffcc',  # Light Yellow: Hedges
            'p_den': '#ccf2ff',  # Light Blue: Pronouns
            'f_den': '#e6ccff'  # Light Purple: Fillers
        }

        all_words = []
        for key, words in m['found_words'].items():
            for w in words:
                all_words.append((w, colors.get(key, '#ffffff')))

        # Sort by length descending to prevent tag overlapping
        all_words.sort(key=lambda x: len(x[0]), reverse=True)

        for word, color in all_words:
            pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
            highlighted_html = pattern.sub(
                f'<span style="background-color: {color}; font-weight: bold; padding: 1px 3px; border-radius: 3px;">\\1</span>',
                highlighted_html)

        # 2. Generate HTML Table Rows
        dens = m['densities']
        metrics_data = [
            ("Pronoun Density", dens['p_den'], self.baselines['pronouns'], True),
            ("Hedge Density", dens['h_den'], self.baselines['hedges'], False),
            ("Time Leap Density", dens['t_den'], self.baselines['time_leaps'], False),
            ("Negative Qualifiers", dens['q_den'], self.baselines['qualifiers'], False),
            ("Filler Density", dens['f_den'], self.baselines['fillers'], False)
        ]

        table_rows = ""
        for name, val, base, is_below in metrics_data:
            status = self._get_status(val, base, is_below)
            base_str = f"&lt; {base}%" if is_below else f"&gt; {base}%"
            status_color = "#27ae60" if status == "[OK]" else "#e67e22" if status == "[WARNING]" else "#e74c3c"

            table_rows += f"""
            <tr>
                <td><strong>{name}</strong></td>
                <td>{val:.2f}%</td>
                <td>{base_str}</td>
                <td style="color: {status_color}; font-weight: bold;">{status}</td>
            </tr>
            """

        # 3. Construct Final HTML Content
        html_content = f"""
        <html><head><style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f4f4f9; color: #333; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            h1, h3 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .risk {{ padding: 20px; text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; border-radius: 6px; color: white; text-transform: uppercase; letter-spacing: 1px; }}
            .high {{ background: #e74c3c; box-shadow: 0 4px 10px rgba(231, 76, 60, 0.3); }} 
            .med {{ background: #f39c12; box-shadow: 0 4px 10px rgba(243, 156, 18, 0.3); }} 
            .low {{ background: #27ae60; box-shadow: 0 4px 10px rgba(39, 174, 96, 0.3); }}

            /* Legend Styles */
            .legend {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0; padding: 15px; background: #f8fafc; border-radius: 5px; border: 1px solid #e2e8f0; }}
            .legend-item {{ display: flex; align-items: center; font-size: 0.85em; font-weight: bold; }}
            .color-box {{ width: 18px; height: 18px; border-radius: 3px; margin-right: 8px; border: 1px solid #cbd5e1; }}

            .box {{ background: #fafafa; border: 1px solid #eee; padding: 25px; white-space: pre-wrap; line-height: 1.8; font-size: 1.1em; border-radius: 4px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.95em; }}
            th, td {{ padding: 12px 15px; border-bottom: 1px solid #edf2f7; text-align: left; }}
            th {{ background-color: #f8fafc; color: #64748b; text-transform: uppercase; font-size: 0.85em; }}
            .conclusion {{ font-style: italic; color: #475569; margin-top: 20px; padding: 15px; background: #f1f5f9; border-left: 4px solid #cbd5e1; }}
        </style></head><body><div class="container">
            <h1>LYAR Forensic Analysis Dashboard</h1>
            <p><strong>Analysis Date:</strong> 2026-01-05 | <strong>Total Word Count:</strong> {m['total_words']}</p>

            <div class="risk {'high' if m['risk_score'] >= 70 else 'med' if m['risk_score'] >= 40 else 'low'}">
                Risk Assessment Score: {m['risk_score']} / 100
            </div>

            <h3>Statistical Metrics</h3>
            <table>
                <thead>
                    <tr><th>Indicator</th><th>Measured Value</th><th>Baseline</th><th>Status</th></tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>

            <h3>Linguistic Evidence Legend</h3>
            <div class="legend">
                <div class="legend-item"><div class="color-box" style="background: {colors['q_den']};"></div> Qualifiers (Convincing Mode)</div>
                <div class="legend-item"><div class="color-box" style="background: {colors['t_den']};"></div> Time Leaps (Narrative Gaps)</div>
                <div class="legend-item"><div class="color-box" style="background: {colors['h_den']};"></div> Hedges (Evasiveness)</div>
                <div class="legend-item"><div class="color-box" style="background: {colors['p_den']};"></div> Pronouns (Self-Reference)</div>
                <div class="legend-item"><div class="color-box" style="background: {colors['f_den']};"></div> Fillers (Cognitive Load)</div>
            </div>

            <h3>Highlighted Text Evidence</h3>
            <div class="box">{highlighted_html}</div>

            <div class="conclusion">
                <strong>Conclusion:</strong> {self._get_conclusion(m['risk_score'])}
            </div>
        </div></body></html>"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n[SUCCESS] Comprehensive HTML report with legend saved: {filename}")

    def batch_process(self, folder_path):
        """Processes an entire directory of .txt files for risk ranking."""
        if not os.path.isdir(folder_path): return
        all_results = []
        files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        for file_name in files:
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
                metrics = self._get_metrics(f.read())
                if metrics: all_results.append(
                    {'filename': file_name, 'risk': metrics['risk_score'], 'words': metrics['total_words']})

        all_results.sort(key=lambda x: x['risk'], reverse=True)
        self._generate_batch_chart(all_results)

        print("\n" + "=" * 65 + f"\n{'RANK':<5} | {'FILENAME':<30} | {'RISK SCORE'}\n" + "-" * 65)
        for i, res in enumerate(all_results, 1):
            print(f"{i:<5} | {res['filename']:<30} | {res['risk']:>3} / 100")
        print("=" * 65)

    def _generate_batch_chart(self, results, output_path="batch_risk_analysis.png"):
        """Generates a PNG bar chart showing risk distribution across subjects."""
        filenames = [res['filename'] for res in results]
        scores = [res['risk'] for res in results]
        colors = ['#e74c3c' if s >= 70 else '#f39c12' if s >= 40 else '#27ae60' for s in scores]

        plt.figure(figsize=(10, 5))
        plt.bar(filenames, scores, color=colors)
        plt.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='High Risk')
        plt.ylabel('Risk Score')
        plt.title('Batch Risk Distribution Across Statements')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"[SUCCESS] Visual risk distribution chart saved: {output_path}")


# --- EXECUTION ENGINE ---
if __name__ == "__main__":
    analyzer = ForensicAnalyzer()
    while True:
        print("\n" + "=" * 65 + "\n         LYAR: INTELLIGENCE & FORENSICS\n" + "=" * 65)
        print("1. Analyze Statement | 2. Compare Statements | 3. Batch Process Folder | 4. Exit")
        choice = input("\nOption: ")
        try:
            if choice == "1":
                with open(input("File Path: ").strip(' "'), "r") as f:
                    content = f.read()
                analyzer.print_report(content)
                if input("Export HTML Report? (y/n): ").lower() == 'y': analyzer.export_to_html(content)
            elif choice == "2":
                with open(input("File 1 Path: ").strip(' "'), "r") as f1, open(input("File 2 Path: ").strip(' "'), "r") as f2:
                    analyzer.compare(f1.read(), f2.read())
            elif choice == "3":
                analyzer.batch_process(input("Folder path: ").strip(' "'))
            elif choice == "4":
                print("Closing LYAR engine...")
                break
        except Exception as e:
            print(f"System Error: {e}")