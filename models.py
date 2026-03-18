from pydantic import BaseModel, Field
from typing import List


class Character(BaseModel):
    name: str
    role: str
    trait: str
    flaw: str


class CrimeSetup(BaseModel):
    crime_type: str
    victim: str
    setting: str
    culprit: str
    motive: str
    hidden_method: str
    key_secret: str


class SuspenseFrame(BaseModel):
    protagonist: Character
    goal: str
    dire_stakes: str
    countdown: str


class PlotPoint(BaseModel):
    index: int
    title: str
    content: str
    obstacle: str
    clue: str
    suspicion_shift: str
    tension_score: int = Field(ge=1, le=10)


class StoryPackage(BaseModel):
    team_name: str
    system_name: str
    template_name: str
    crime_setup: CrimeSetup
    suspense_frame: SuspenseFrame
    suspects: List[str]
    red_herrings: List[str]
    plot_points: List[PlotPoint]
    final_reveal: str
    retold_story: str