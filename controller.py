from typing import List
from pydantic import ValidationError

from llm_client import LLMClient
from prompts import (
    SYSTEM_PROMPT,
    CRIME_SETUP_PROMPT,
    SUSPENSE_FRAME_PROMPT,
    SUSPECTS_PROMPT,
    NEXT_PLOT_POINT_PROMPT,
    FINAL_REVEAL_PROMPT,
    RETELLING_PROMPT,
)
from models import CrimeSetup, SuspenseFrame, PlotPoint, StoryPackage
from config import NUM_PLOT_POINTS, MAX_RETRIES


def flatten_crime_setup_fields(data: dict) -> dict:
    for key in ["victim", "setting", "culprit"]:
        value = data.get(key)

        if isinstance(value, dict):
            if key == "victim":
                data[key] = value.get("name") or str(value)

            elif key == "setting":
                location = value.get("location", "")
                time = value.get("time", "")
                joined = ", ".join(part for part in [location, time] if part)
                data[key] = joined if joined else str(value)

            elif key == "culprit":
                data[key] = value.get("name") or str(value)

    return data


def flatten_suspects_list(items):
    flat = []

    for item in items:
        if isinstance(item, str):
            flat.append(item)

        elif isinstance(item, dict):
            name = item.get("name")
            role = item.get("role")
            motive = item.get("motive")

            if name and role:
                flat.append(f"{name}, {role}")
            elif name and motive:
                flat.append(f"{name}, suspected because {motive}")
            elif name:
                flat.append(name)
            else:
                flat.append(str(item))

        else:
            flat.append(str(item))

    return flat


def flatten_red_herrings_list(items):
    flat = []

    for item in items:
        if isinstance(item, str):
            flat.append(item)

        elif isinstance(item, dict):
            clue = item.get("clue")
            explanation = item.get("explanation")

            if clue and explanation:
                flat.append(f"{clue} ({explanation})")
            elif clue:
                flat.append(clue)
            else:
                flat.append(str(item))

        else:
            flat.append(str(item))

    return flat


class SuspenseMetaController:
    """
    Architecture mapping:
    1. Generate crime setup
    2. Generate suspense frame
    3. Generate suspects and red herrings
    4. Iteratively generate plot points with escalating suspense
    5. Generate final reveal
    6. Retell as polished story
    """

    def __init__(self, team_name: str, system_name: str):
        self.team_name = team_name
        self.system_name = system_name
        self.llm = LLMClient()

    def _mock_story(self) -> StoryPackage:
        crime_setup = CrimeSetup(
            crime_type="museum theft",
            victim="the Ashcroft Museum",
            setting="a storm-locked seaside town",
            culprit="Elena Ward, the deputy curator",
            motive="to cover gambling debts and frame a rival",
            hidden_method="she used a scheduled blackout and swapped the real artifact with a replica",
            key_secret="the security log was manually edited before the storm"
        )

        suspense_frame = SuspenseFrame(
            protagonist={
                "name": "Mara Ivers",
                "role": "junior investigative reporter",
                "trait": "persistent",
                "flaw": "acts before asking for help"
            },
            goal="prove who stole the museum's prized compass before the ferry resumes service",
            dire_stakes="if she fails, an innocent guard will be arrested and the real thief will disappear",
            countdown="the ferry leaves at dawn in 8 hours"
        )

        suspects = ["Elena Ward", "Tom Baines", "Victor Hale", "Nina Cross"]
        red_herrings = [
            "A muddy boot print near the east gallery",
            "A torn receipt from the guard's jacket pocket"
        ]

        plot_points = []
        for i in range(1, 16):
            plot_points.append(
                PlotPoint(
                    index=i,
                    title=f"Plot Point {i}",
                    content=f"Mara uncovers event {i}, which pushes the case forward.",
                    obstacle=f"Obstacle {i} increases pressure on Mara.",
                    clue=f"Clue {i} reveals part of the hidden method.",
                    suspicion_shift=f"Suspicion shifts after event {i}.",
                    tension_score=min(10, 4 + i // 2)
                    
                )
            )

        final_reveal = (
            "Mara proves Elena Ward engineered the blackout, edited the security log, "
            "and used the confusion to swap the compass with a replica."
        )

        retold_story = (
            "With the ferry due at dawn and the town trapped by a storm, reporter Mara Ivers "
            "races to uncover who stole the Ashcroft Compass."
        )

        return StoryPackage(
            team_name=self.team_name,
            system_name=self.system_name,
            template_name="Suspense Generation",
            crime_setup=crime_setup,
            suspense_frame=suspense_frame,
            suspects=suspects,
            red_herrings=red_herrings,
            plot_points=plot_points,
            final_reveal=final_reveal,
            retold_story=retold_story,
        )

    def generate_story(self) -> StoryPackage:
        if not self.llm.enabled:
            return self._mock_story()

        try:
            print("starting crime setup call...")
            crime_setup_data = self.llm.generate_json(SYSTEM_PROMPT, CRIME_SETUP_PROMPT)
            print("finished crime setup call")

            crime_setup_data = flatten_crime_setup_fields(crime_setup_data)
            crime_setup = CrimeSetup(**crime_setup_data)

            print("starting suspense frame call...")
            suspense_data = self.llm.generate_json(
                SYSTEM_PROMPT,
                SUSPENSE_FRAME_PROMPT.format(
                    crime_setup=crime_setup.model_dump_json(indent=2)
                )
            )
            print("finished suspense frame call")

            suspense_frame = SuspenseFrame(**suspense_data)

            print("starting suspects call...")
            suspects_data = self.llm.generate_json(
                SYSTEM_PROMPT,
                SUSPECTS_PROMPT.format(
                    crime_setup=crime_setup.model_dump_json(indent=2)
                )
            )
            print("finished suspects call")

            suspects = flatten_suspects_list(suspects_data.get("suspects", []))
            red_herrings = flatten_red_herrings_list(suspects_data.get("red_herrings", []))

            plot_points: List[PlotPoint] = []

            for idx in range(1, NUM_PLOT_POINTS + 1):
                print(f"starting plot point {idx} call...")

                existing_points = [p.model_dump() for p in plot_points]

                prompt = NEXT_PLOT_POINT_PROMPT.format(
                    crime_setup=crime_setup.model_dump_json(indent=2),
                    suspense_frame=suspense_frame.model_dump_json(indent=2),
                    suspects_block={
                        "suspects": suspects,
                        "red_herrings": red_herrings
                    },
                    existing_points=existing_points
                )

                success = False

                for attempt in range(MAX_RETRIES):
                    try:
                        point_data = self.llm.generate_json(SYSTEM_PROMPT, prompt)
                        point_data["index"] = idx
                        point = PlotPoint(**point_data)
                        plot_points.append(point)
                        success = True
                        print(f"finished plot point {idx} call")
                        break
                    except ValidationError as ve:
                        print(f"plot point {idx} validation failed on attempt {attempt + 1}: {ve}")
                        continue
                    except Exception as e:
                        print(f"plot point {idx} failed on attempt {attempt + 1}: {repr(e)}")
                        continue

                if not success:
                    print(f"using fallback plot point {idx}")
                    plot_points.append(
                        PlotPoint(
                            index=idx,
                            title=f"Fallback Plot Point {idx}",
                            content="The protagonist pushes the investigation forward under growing pressure.",
                            obstacle="A new complication narrows the time available.",
                            clue="A small inconsistency points back to the true culprit.",
                            suspicion_shift="Attention moves away from the obvious suspect.",
                            tension_score=min(10, 5 + idx // 2),
                        )
                    )

            print("starting final reveal call...")
            final_reveal = self.llm.generate_text(
                SYSTEM_PROMPT,
                FINAL_REVEAL_PROMPT.format(
                    crime_setup=crime_setup.model_dump_json(indent=2),
                    plot_points=[p.model_dump() for p in plot_points]
                )
            )
            print("finished final reveal call")

            print("starting retelling call...")
            retold_story = self.llm.generate_text(
                SYSTEM_PROMPT,
                RETELLING_PROMPT.format(
                    crime_setup=crime_setup.model_dump_json(indent=2),
                    suspense_frame=suspense_frame.model_dump_json(indent=2),
                    plot_points=[p.model_dump() for p in plot_points],
                    final_reveal=final_reveal
                )
            )
            print("finished retelling call")

            return StoryPackage(
                team_name=self.team_name,
                system_name=self.system_name,
                template_name="Suspense Generation",
                crime_setup=crime_setup,
                suspense_frame=suspense_frame,
                suspects=suspects,
                red_herrings=red_herrings,
                plot_points=plot_points,
                final_reveal=final_reveal,
                retold_story=retold_story,
            )

        except Exception as e:
            print("REAL ERROR:", e)
            return self._mock_story()