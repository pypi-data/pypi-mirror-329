from pandera import DataFrameModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ContractSchema(DataFrameModel):
    """Schema for individual contract entries"""
    # Required fields
    Startdate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    
    # Optional fields
    Enddate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EmploymentStatus: Optional[str] = Field(nullable=True, isin=['Workman', 'Employee', 'Director'])
    Contract: Optional[str] = Field(nullable=True, isin=[
        'Usually', 'FlexiVerbal', 'FlexiWritten', 'FlexiLiable', 'Sportsperson',
        'Housekeeper', 'Servant', 'Agriculture', 'Homework', 'HomeworkChildcare',
        'Physician', 'PhysicianTraining', 'PhysicianIndependant', 'ApprenticeFlemisch',
        'ApprenticeFrench', 'ApprenticeGerman', 'ApprenticeManager', 'ApprenticeIndustrial',
        'ApprenticeSocio', 'ApprenticeBio', 'ApprenticeAlternating', 'EarlyRetirement',
        'EarlyRetirementPartTime', 'FreeNOSS', 'FreeNOSSManager', 'FreeNOSSOther',
        'FreeNOSSSportingEvent', 'FreeNOSSHelper', 'FreeNOSSSocio', 'FreeNOSSEducation',
        'FreeNOSSSpecialCultures', 'FreeNOSSVolunteer', 'Horeca', 'HorecaExtraHourLiable',
        'HorecaExtraDayLiable', 'HorecaExtraHourForfait', 'HorecaExtraDayForfait',
        'HorecaFlexiVerbal', 'HorecaFlexiWritten', 'HorecaFlexiLiable', 'Construction',
        'ConstructionAlternating', 'ConstructionApprenticeYounger', 'ConstructionApprentice',
        'ConstructionGodfather', 'JobTrainingIBO', 'JobTrainingSchool', 'JobTrainingVDAB',
        'JobTrainingLiberalProfession', 'JobTrainingEntry', 'JobTrainingPFIWa',
        'JobTrainingABO', 'JobTrainingPFIBx', 'JobTrainingBIO', 'JobTrainingAlternating',
        'JobTrainingDisability', 'NonProfitRiziv', 'NonProfitGesco', 'NonProfitDAC',
        'NonProfitPrime', 'NonProfitLowSkilled', 'Artist', 'ArtistWithContract',
        'ArtistWithoutContract', 'Transport', 'TransportNonMobile', 'TransportGarage',
        'Aircrew', 'AircrewPilot', 'AircrewCabinCrew', 'Interim', 'InterimTemporary',
        'InterimsPermanent', 'External', 'ExternalApplicant', 'ExternalSubcontractor',
        'ExternalAgentIndependant', 'ExternalExtern', 'ExternalIntern', 'ExternalLegalPerson',
        'SalesRepresentative', 'SportsTrainer'
    ])
    CatRSZ: Optional[str] = Field(nullable=True, str_length={'min_value': 3, 'max_value': 3}, regex=r'^[0-9]*$')
    ParCom: Optional[str] = Field(nullable=True, str_length={'min_value': 3, 'max_value': 10}, regex=r'^[0-9. ]*$')
    DocumentC78: Optional[str] = Field(nullable=True, isin=[
        'Nihil', 'C783', 'C784', 'C78Activa', 'C78Start', 'C78Sine', 'C78ShortTerm',
        'WalloniaLongtermJobSeekers', 'WalloniaYoungJobSeekers', 'WalloniaImpulsionInsertion',
        'BrusselsLongtermJobSeekers', 'BrusselsReducedAbility'
    ])
    CodeC98: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    CodeC131A: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    CodeC131: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    Risk: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    SocialSecurityCard: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    WorkPermit: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    DateInService: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    Seniority: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    DateProfessionalExperience: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    ScaleSalarySeniority: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    StartProbationPeriod: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndProbationPeriod: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    FixedTerm: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    EndFixedTerm: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    DateOutService: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    ReasonOut: Optional[str] = Field(nullable=True)
    WorkingTime: Optional[str] = Field(nullable=True, isin=['Fulltime', 'PartTime'])
    SpecWorkingTime: Optional[str] = Field(nullable=True, isin=['Regular', 'Interruptions', 'SeasonalWorker'])
    Schedule: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 4})
    WeekhoursWorker: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    WeekhoursEmployer: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    WeekhoursWorkerAverage: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    WeekhoursEmployerAverage: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    WeekhoursWorkerEffective: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    WeekhoursEmployerEffective: Optional[float] = Field(nullable=True, ge=1.0, le=50.0)
    DaysWeek: Optional[float] = Field(nullable=True)
    DaysWeekFT: Optional[float] = Field(nullable=True)
    ReducingWorkingKind: Optional[str] = Field(nullable=True, isin=['Nihil', 'Paid', 'Unpaid'])
    ReducingWorkingKindDays: Optional[float] = Field(nullable=True)
    ReducingWorkingKindHours: Optional[float] = Field(nullable=True)
    PartTimeReturnTowork: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 4})
    ASRSchedule: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 2})
    ProffCat: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    Function: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    FunctionDescription: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 50})
    Office: Optional[int] = Field(nullable=True)
    Division: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    InvoicingDivision: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    CostCentre: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    ScaleSalaryPrisma: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    ScaleSalaryUse: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    ScaleSalaryDefinition: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    ScaleSalaryCategory: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    ScaleSalaryScale: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 100})
    ExcludeForDMFAdeclaration: Optional[str] = Field(nullable=True, isin=['N', 'Y'])
    AgricultureType: Optional[str] = Field(nullable=True, isin=[
        'Horticulture', 'HorticultureChicory', 'Agriculture',
        'HorticultureMushroom', 'HorticultureFruit'
    ])

    # Nested fields
    CareerBreak: Optional[Dict[str, Any]] = Field(nullable=True)
    ProtectedEmployee: Optional[Dict[str, Any]] = Field(nullable=True)
    Sportsperson: Optional[Dict[str, Any]] = Field(nullable=True)
    CertainWork: Optional[Dict[str, Any]] = Field(nullable=True)
    Student: Optional[Dict[str, Any]] = Field(nullable=True)
    ProgressiveWorkResumption: Optional[Dict[str, Any]] = Field(nullable=True)
    MethodOfRemuneration: Optional[Dict[str, Any]] = Field(nullable=True)
    InternationalEmployment: Optional[Dict[str, Any]] = Field(nullable=True)
    Dimona: Optional[Dict[str, Any]] = Field(nullable=True)
    SalaryCompositions: Optional[List[Dict[str, Any]]] = Field(nullable=True)

    class Config:
        strict = True
        coerce = True

class StudentSchema(DataFrameModel):
    """Schema for student entries"""
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    Exist: str = Field(nullable=False, isin=['N', 'Y'])
    SolidarityContribution: str = Field(nullable=False, isin=['N', 'Y'])

    class Config:
        strict = True
        coerce = True

class CertainWorkSchema(DataFrameModel):
    """Schema for certain work entries"""
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    Exist: str = Field(nullable=False, isin=['N', 'Y'])
    Description: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 250})

    class Config:
        strict = True
        coerce = True

class CareerBreakSchema(DataFrameModel):
    """Schema for career break entries"""
    Exist: str = Field(nullable=False, isin=['N', 'Y'])
    Kind: Optional[str] = Field(nullable=True, isin=[
        'Fulltime', 'PartTimeOneFifth', 'PartTimeOneQuarter', 'PartTimeOneThird',
        'PartTimeHalf', 'PartTimeThreeFifths', 'PartTimeOneTenth'
    ])
    Reason: Optional[str] = Field(nullable=True, isin=[
        'PalliativeCare', 'SeriouslyIll', 'Other', 'ParentalLeave', 'Crisis',
        'FamilyCare', 'EndOfCareer', 'SickChild', 'FamilyCareCorona',
        'ChildCareUnder8', 'ChildCareHandicapUnder21', 'CertifiedTraining'
    ])
    OriginallyContractType: Optional[str] = Field(nullable=True, isin=['Fulltime', 'PartTime'])
    WeekhoursWorkerBefore: Optional[float] = Field(nullable=True)
    WeekhoursEmployerBefore: Optional[float] = Field(nullable=True)
    StartDate: str = Field(nullable=False, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    EndDate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')

    class Config:
        strict = True
        coerce = True
