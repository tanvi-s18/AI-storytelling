from typing import List
from models import PlotPoint


def validate_plot_points(plot_points: List[PlotPoint]) -> List[str]:
    issues = []

    if len(plot_points) < 15:
        issues.append("Story has fewer than 15 plot points.")

    clue_count = sum(1 for p in plot_points if p.clue.strip())
    if clue_count < 10:
        issues.append("Too few meaningful clues across plot points.")

    high_tension = sum(1 for p in plot_points if p.tension_score >= 7)
    if high_tension < 5:
        issues.append("Suspense escalation may be too weak.")

    repeated_titles = len(set(p.title for p in plot_points)) != len(plot_points)
    if repeated_titles:
        issues.append("Repeated plot point titles found.")

    return issues