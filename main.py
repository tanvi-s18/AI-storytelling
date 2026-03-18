from controller import SuspenseMetaController
from storyteller import format_plot_points_for_readme
from validator import validate_plot_points
from utils import save_json, save_text


def main():

    from config import OPENAI_API_KEY
    print("API key loaded:", bool(OPENAI_API_KEY))
    print("First chars:", OPENAI_API_KEY[:7] if OPENAI_API_KEY else "NONE")
    team_name = "Bombastic Blobfish"
    system_name = "SuspenseSpin"

    controller = SuspenseMetaController(team_name=team_name, system_name=system_name)
    story = controller.generate_story()

    issues = validate_plot_points(story.plot_points)

    summary = []
    summary.append(f"Team Name: {story.team_name}")
    summary.append(f"System Name: {story.system_name}")
    summary.append(f"Template: {story.template_name}")
    summary.append("")
    summary.append("=== Crime Setup ===")
    summary.append(story.crime_setup.model_dump_json(indent=2))
    summary.append("")
    summary.append("=== Suspense Frame ===")
    summary.append(story.suspense_frame.model_dump_json(indent=2))
    summary.append("")
    summary.append("=== Suspects ===")
    summary.append(str(story.suspects))
    summary.append("")
    summary.append("=== Red Herrings ===")
    summary.append(str(story.red_herrings))
    summary.append("")
    summary.append("=== 15+ Plot Points ===")
    summary.append(format_plot_points_for_readme(story.plot_points))
    summary.append("")
    summary.append("=== Final Reveal ===")
    summary.append(story.final_reveal)
    summary.append("")
    summary.append("=== Retold Story ===")
    summary.append(story.retold_story)
    summary.append("")
    summary.append("=== Validation Issues ===")
    summary.append("\n".join(issues) if issues else "No major issues detected.")

    output_text = "\n".join(summary)

    save_text("latest_story.txt", output_text)
    save_json("latest_story.json", story.model_dump())

    print(output_text)


if __name__ == "__main__":
    main()