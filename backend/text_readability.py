import textstat
import matplotlib.pyplot as plt

def calculate_readability(text):
    """
    Calculates readability scores and generates a matplotlib bar chart.
    Returns:
        scores: dict of individual readability scores
        overall_cat: string (Beginner / Intermediate / Advanced)
        fig: matplotlib figure
    """
    text = text.replace("<n>", " ").replace("\n", " ").strip()
    if not text:
        return {}, "⚠️ No valid text provided", None

    try:
        fk = textstat.flesch_kincaid_grade(text)
        gf = textstat.gunning_fog(text)
        smog = textstat.smog_index(text)

        num_words = len(text.split())
        if num_words < 50:
            smog = min(smog, (fk + gf) / 2)

        scores = {
            "Flesch-Kincaid Grade": fk,
            "Gunning Fog Index": gf,
            "SMOG Index": smog
        }

        avg_score = (fk + gf + smog) / 3
        if avg_score <= 4:
            overall_cat = "Beginner"
        elif avg_score <= 8:
            overall_cat = "Intermediate"
        else:
            overall_cat = "Advanced"

        raw_values = [fk, gf, smog]
        labels = ["Flesch-Kincaid", "Gunning Fog", "SMOG"]
        colors = ["green" if x <= 4 else "orange" if x <= 8 else "red" for x in raw_values]

        fig, ax = plt.subplots(figsize=(5, 3))
        bars = ax.bar(labels, raw_values, color=colors, width=0.5)
        ax.set_ylim(0, max(raw_values) * 1.1)
        ax.set_ylabel("Score")
        ax.set_title("Readability Scores")

        for bar, val in zip(bars, raw_values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + (max(raw_values) * 0.02),
                f"{val:.2f}",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        plt.tight_layout()
        return scores, overall_cat, fig

    except Exception as e:
        return {}, f"❌ Error calculating readability: {e}", None
