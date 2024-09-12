from typing import List, Optional
from pydantic import BaseModel, Field

class PlayerRating(BaseModel):
    acceleration_diff: Optional[int] = None
    acceleration_rating: int
    age: int
    age_diff: Optional[int] = None
    agility_diff: Optional[int] = None
    agility_rating: int
    archetype: str
    awareness_diff: Optional[int] = None
    awareness_rating: int
    bCVision_diff: Optional[int] = None
    bCVision_rating: int
    blockShedding_diff: Optional[int] = None
    blockShedding_rating: int
    breakSack_diff: Optional[int] = None
    breakSack_rating: int
    breakTackle_diff: Optional[int] = None
    breakTackle_rating: int
    carrying_diff: Optional[int] = None
    carrying_rating: int
    catchInTraffic_diff: Optional[int] = None
    catchInTraffic_rating: int
    catching_diff: Optional[int] = None
    catching_rating: int
    changeOfDirection_diff: Optional[int] = None
    changeOfDirection_rating: int
    college: str
    deepRouteRunning_diff: Optional[int] = None
    deepRouteRunning_rating: int
    finesseMoves_diff: Optional[int] = None
    finesseMoves_rating: int
    firstName: str
    fullNameForSearch: str
    height: int
    height_diff: Optional[int] = None
    hitPower_diff: Optional[int] = None
    hitPower_rating: int
    impactBlocking_diff: Optional[int] = None
    impactBlocking_rating: int
    injury_diff: Optional[int] = None
    injury_rating: int
    iteration: str
    jerseyNum: int
    jerseyNum_diff: Optional[int] = None
    jumping_diff: Optional[int] = None
    jumping_rating: int
    jukeMove_diff: Optional[int] = None
    jukeMove_rating: int
    kickAccuracy_diff: Optional[int] = None
    kickAccuracy_rating: int
    kickPower_diff: Optional[int] = None
    kickPower_rating: int
    kickReturn_diff: Optional[int] = None
    kickReturn_rating: int
    lastName: str
    leadBlock_diff: Optional[int] = None
    leadBlock_rating: int
    manCoverage_diff: Optional[int] = None
    manCoverage_rating: int
    mediumRouteRunning_diff: Optional[int] = None
    mediumRouteRunning_rating: int
    overall_diff: Optional[int] = None
    overall_rating: int
    passBlock_diff: Optional[int] = None
    passBlockFinesse_diff: Optional[int] = None
    passBlockFinesse_rating: int
    passBlockPower_diff: Optional[int] = None
    passBlockPower_rating: int
    passBlock_rating: int
    playAction_diff: Optional[int] = None
    playAction_rating: int
    playRecognition_diff: Optional[int] = None
    playRecognition_rating: int
    plyrAssetname: str
    plyrBirthdate: str
    plyrHandedness: str
    plyrPortrait: int
    plyrPortrait_diff: Optional[int] = None
    position: str
    powerMoves_diff: Optional[int] = None
    powerMoves_rating: int
    press_diff: Optional[int] = None
    press_rating: int
    primaryKey: int
    primaryKey_diff: Optional[int] = None
    pursuit_diff: Optional[int] = None
    pursuit_rating: int
    release_diff: Optional[int] = None
    release_rating: int
    runBlock_diff: Optional[int] = None
    runBlockFinesse_diff: Optional[int] = None
    runBlockFinesse_rating: int
    runBlockPower_diff: Optional[int] = None
    runBlockPower_rating: int
    runBlock_rating: int
    runningStyle_rating: str
    shortRouteRunning_diff: Optional[int] = None
    shortRouteRunning_rating: int
    signingBonus: int
    signingBonus_diff: Optional[int] = None
    spectacularCatch_diff: Optional[int] = None
    spectacularCatch_rating: int
    speed_diff: Optional[int] = None
    speed_rating: int
    spinMove_diff: Optional[int] = None
    spinMove_rating: int
    stamina_diff: Optional[int] = None
    stamina_rating: int
    status: str
    stiffArm_diff: Optional[int] = None
    stiffArm_rating: int
    strength_diff: Optional[int] = None
    strength_rating: int
    tackle_diff: Optional[int] = None
    tackle_rating: int
    team: str = Field(alias="ost")
    teamId: int
    teamId_diff: Optional[int] = None
    throwAccuracyDeep_diff: Optional[int] = None
    throwAccuracyDeep_rating: int
    throwAccuracyMid_diff: Optional[int] = None
    throwAccuracyMid_rating: int
    throwAccuracyShort_diff: Optional[int] = None
    throwAccuracyShort_rating: int
    throwOnTheRun_diff: Optional[int] = None
    throwOnTheRun_rating: int
    throwPower_diff: Optional[int] = None
    throwPower_rating: int
    throwUnderPressure_diff: Optional[int] = None
    throwUnderPressure_rating: int
    totalSalary: int
    totalSalary_diff: Optional[int] = None
    toughness_diff: Optional[int] = None
    toughness_rating: int
    trucking_diff: Optional[int] = None
    trucking_rating: int
    weight: int
    weight_diff: Optional[int] = None
    yearsPro: int
    yearsPro_diff: Optional[int] = None
    zoneCoverage_diff: Optional[int] = None
    zoneCoverage_rating: int

    class Config:
        populate_by_name = True


class RatingsResponse(BaseModel):
    count: int
    docs: List[PlayerRating]
