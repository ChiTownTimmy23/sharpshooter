from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Any, Optional
from datetime import datetime   

class NameDisplay(BaseModel):
    value: str
    isEmphasized: Optional[bool] = None

class Competition(BaseModel):
    competitionId: int
    name: str
    nameDisplay: List[NameDisplay]
    startTime: datetime


class DraftStatAttribute(BaseModel):
    id: int
    value: str
    sortValue: str


class DKDraftable(BaseModel):
    draftableId: int
    firstName: str
    lastName: str
    displayName: str
    shortName: str
    playerId: int
    playerDkId: int
    position: str
    rosterSlotId: int
    salary: int
    status: str
    isSwappable: bool
    isDisabled: bool
    newsStatus: Optional[str] = None
    playerImage50: str
    playerImage160: str
    altPlayerImage50: str
    altPlayerImage160: str
    competition: Optional[Competition] = None
    competitions: List[Competition]
    draftStatAttributes: List[DraftStatAttribute]
    playerAttributes: List[Any]
    teamLeagueSeasonAttributes: List[Any]
    playerGameAttributes: List[Any]
    teamId: int
    teamAbbreviation: str
    draftAlerts: List[Any]
    playerGameHash: str
    externalRequirements: Dict[str, Any]


class DKDraftablesResponse(BaseModel):
    draftables: List[DKDraftable]