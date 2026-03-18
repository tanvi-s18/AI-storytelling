from typing import List
from models import PlotPoint


def format_plot_points_for_readme(plot_points: List[PlotPoint]) -> str:
    lines = []
    for p in plot_points:
        lines.append(f"{p.index}. {p.title}")
        lines.append(f"   Plot Point: {p.content}")
        lines.append(f"   Obstacle: {p.obstacle}")
        lines.append(f"   Clue: {p.clue}")
        lines.append(f"   Suspicion Shift: {p.suspicion_shift}")
        lines.append(f"   Tension Score: {p.tension_score}")
        lines.append("")
    return "\n".join(lines)