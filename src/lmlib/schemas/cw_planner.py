from typing import Any, Dict, List, Optional, Union
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, ConfigDict


class CWVesselInput(BaseModel):
    """Vessel model matching CW ETA Planner API expectations."""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str
    name: str = ""
    capacity_weight_tons: float = Field(default=4500.0, alias="capacityWeightTons")
    max_monopiles: int = Field(default=3, alias="maxMonopiles")
    speed_knots: float = Field(default=14.0, alias="speedKnots")
    available_from_day: float = Field(default=0.0, alias="availableFromDay")
    compatible_grillage_types: List[str] = Field(default_factory=lambda: ["Type-A"], alias="compatibleGrillageTypes")
    operational_calendar: str = Field(default="24/7", alias="operationalCalendar")
    vessel_class: str = Field(default="TClass", alias="vesselClass")

    @classmethod
    def from_input(cls, item: Union[Dict[str, Any], "CWVesselInput", Any]) -> "CWVesselInput":
        if isinstance(item, cls):
            return item
        if isinstance(item, dict):
            data = item.copy()
            v_id = data.get("id") or data.get("ID") or data.get("vessel_id") or "VESSEL-01"
            name = data.get("name") or str(v_id)
            capacity = data.get("capacityWeightTons") or data.get("capacity_weight_tons") or data.get("capacity", 4500.0)
            max_mp = data.get("maxMonopiles") or data.get("max_monopiles") or 3
            speed = data.get("speedKnots") or data.get("speed_knots") or data.get("speed", 14.0)
            avail = data.get("availableFromDay") or data.get("available_from_day") or 0.0
            grillages = data.get("compatibleGrillageTypes") or data.get("compatible_grillage_types") or ["Type-A"]
            if isinstance(grillages, str):
                grillages = [grillages]
            calendar = data.get("operationalCalendar") or data.get("operational_calendar") or "24/7"
            v_class = data.get("vesselClass") or data.get("vessel_class") or "TClass"

            return cls(
                id=str(v_id),
                name=str(name),
                capacityWeightTons=float(capacity),
                maxMonopiles=int(max_mp),
                speedKnots=float(speed),
                availableFromDay=float(avail),
                compatibleGrillageTypes=list(grillages),
                operationalCalendar=str(calendar),
                vesselClass=str(v_class)
            )

        # Handle lmlib Vessel Pydantic model or arbitrary objects
        v_id = getattr(item, "ID", None) or getattr(item, "id", None) or getattr(item, "vessel_id", "VESSEL-01")
        name = getattr(item, "name", str(v_id))
        v_type = getattr(item, "vessel_type", "TClass")
        if hasattr(v_type, "value"):
            v_type = v_type.value

        return cls(
            id=str(v_id),
            name=str(name),
            capacityWeightTons=float(getattr(item, "capacityWeightTons", getattr(item, "capacity_weight_tons", 4500.0))),
            maxMonopiles=int(getattr(item, "maxMonopiles", getattr(item, "max_monopiles", 3))),
            speedKnots=float(getattr(item, "speedKnots", getattr(item, "speed_knots", 14.0))),
            availableFromDay=float(getattr(item, "availableFromDay", getattr(item, "available_from_day", 0.0))),
            compatibleGrillageTypes=list(getattr(item, "compatibleGrillageTypes", getattr(item, "compatible_grillage_types", ["Type-A"]))),
            operationalCalendar=str(getattr(item, "operationalCalendar", getattr(item, "operational_calendar", "24/7"))),
            vesselClass=str(v_type)
        )


class CWMonopileInput(BaseModel):
    """Monopile model matching CW ETA Planner API expectations."""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str
    weight_tons: float = Field(default=1350.0, alias="weightTons")
    length_m: float = Field(default=82.0, alias="lengthM")
    grillage_type: str = Field(default="Type-A", alias="grillageType")
    fabrication_yard_id: str = Field(default="FAB-01", alias="fabricationYardId")
    installation_site_id: str = Field(default="SITE-01", alias="installationSiteId")
    fabrication_completion_day: float = Field(default=0.0, alias="fabricationCompletionDay")
    target_installation_day: float = Field(default=100.0, alias="targetInstallationDay")
    origin_logistics_key: str = Field(default="NordenhamGermany", alias="originLogisticsKey")
    destination_logistics_key: str = Field(default="Argentia", alias="destinationLogisticsKey")
    voyage_profile: str = Field(default="DS", alias="voyageProfile")

    @classmethod
    def from_input(cls, item: Union[Dict[str, Any], "CWMonopileInput", Any]) -> "CWMonopileInput":
        if isinstance(item, cls):
            return item
        if isinstance(item, dict):
            data = item.copy()
            mp_id = data.get("id") or data.get("monopile_id") or "MP-001"
            weight = data.get("weightTons") or data.get("weight_tons") or data.get("design_weight_given", 1350.0)
            length = data.get("lengthM") or data.get("length_m") or data.get("mp_length", 82.0)
            grillage = data.get("grillageType") or data.get("grillage_type") or "Type-A"
            if hasattr(grillage, "value"):
                grillage = grillage.value
            fab_yard = data.get("fabricationYardId") or data.get("fabrication_yard_id") or data.get("fabricationYard", "FAB-01")
            site = data.get("installationSiteId") or data.get("installation_site_id") or data.get("installationSite", "SITE-01")
            fab_day = data.get("fabricationCompletionDay") or data.get("fabrication_completion_day") or 0.0
            target_day = data.get("targetInstallationDay") or data.get("target_installation_day") or 100.0
            origin = data.get("originLogisticsKey") or data.get("origin_logistics_key") or "NordenhamGermany"
            dest = data.get("destinationLogisticsKey") or data.get("destination_logistics_key") or "Argentia"
            voyage = data.get("voyageProfile") or data.get("voyage_profile") or "DS"

            return cls(
                id=str(mp_id),
                weightTons=float(weight),
                lengthM=float(length),
                grillageType=str(grillage),
                fabricationYardId=str(fab_yard),
                installationSiteId=str(site),
                fabricationCompletionDay=float(fab_day),
                targetInstallationDay=float(target_day),
                originLogisticsKey=str(origin),
                destinationLogisticsKey=str(dest),
                voyageProfile=str(voyage)
            )

        # Handle lmlib Monopile Pydantic model or arbitrary objects
        mp_id = getattr(item, "id", None) or getattr(item, "monopile_id", "MP-001")
        weight = getattr(item, "weightTons", getattr(item, "weight_tons", getattr(item, "design_weight_given", 1350.0)))
        length = getattr(item, "lengthM", getattr(item, "length_m", getattr(item, "mp_length", 82.0)))
        grillage = getattr(item, "grillageType", getattr(item, "grillage_type", "Type-A"))
        if hasattr(grillage, "value"):
            grillage = grillage.value

        return cls(
            id=str(mp_id),
            weightTons=float(weight),
            lengthM=float(length),
            grillageType=str(grillage),
            fabricationYardId=str(getattr(item, "fabricationYardId", getattr(item, "fabrication_yard_id", "FAB-01"))),
            installationSiteId=str(getattr(item, "installationSiteId", getattr(item, "installation_site_id", "SITE-01"))),
            fabricationCompletionDay=float(getattr(item, "fabricationCompletionDay", getattr(item, "fabrication_completion_day", 0.0))),
            targetInstallationDay=float(getattr(item, "targetInstallationDay", getattr(item, "target_installation_day", 100.0))),
            originLogisticsKey=str(getattr(item, "originLogisticsKey", getattr(item, "origin_logistics_key", "NordenhamGermany"))),
            destinationLogisticsKey=str(getattr(item, "destinationLogisticsKey", getattr(item, "destination_logistics_key", "Argentia"))),
            voyageProfile=str(getattr(item, "voyageProfile", getattr(item, "voyage_profile", "DS")))
        )


class CWEtaPlannerInputPayload(BaseModel):
    """Payload model for POST /api/v1/solver/run"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    reset_before_run: bool = Field(default=True, alias="resetBeforeRun")
    trip_count: Optional[int] = Field(default=None, alias="tripCount")
    departure_day_min: Optional[float] = Field(default=None, alias="departureDayMin")
    departure_day_max: Optional[float] = Field(default=None, alias="departureDayMax")
    discharge_duration_days: Optional[float] = Field(default=None, alias="dischargeDurationDays")
    vessels: Optional[List[CWVesselInput]] = None
    monopiles: Optional[List[CWMonopileInput]] = None

    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary with camelCase keys expected by API."""
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_input(cls, input_data: Optional[Union[Dict[str, Any], "CWEtaPlannerInputPayload", Any]] = None) -> "CWEtaPlannerInputPayload":
        if input_data is None:
            return cls()
        if isinstance(input_data, cls):
            return input_data

        if isinstance(input_data, dict):
            data = input_data.copy()
            reset_flag = data.pop("resetBeforeRun", data.pop("reset_before_run", True))
            trip_count = data.pop("tripCount", data.pop("trip_count", None))
            dep_min = data.pop("departureDayMin", data.pop("departure_day_min", None))
            dep_max = data.pop("departureDayMax", data.pop("departure_day_max", None))
            discharge = data.pop("dischargeDurationDays", data.pop("discharge_duration_days", None))

            vessels_raw = data.pop("vessels", None)
            vessels_list = [CWVesselInput.from_input(v) for v in vessels_raw] if vessels_raw is not None else None

            monopiles_raw = data.pop("monopiles", None)
            monopiles_list = [CWMonopileInput.from_input(m) for m in monopiles_raw] if monopiles_raw is not None else None

            return cls(
                resetBeforeRun=bool(reset_flag),
                tripCount=trip_count,
                departureDayMin=dep_min,
                departureDayMax=dep_max,
                dischargeDurationDays=discharge,
                vessels=vessels_list,
                monopiles=monopiles_list
            )

        # Handle custom objects or objects containing vessel/monopile lists
        reset_flag = getattr(input_data, "resetBeforeRun", getattr(input_data, "reset_before_run", True))
        vessels_raw = getattr(input_data, "vessels", None)
        vessels_list = [CWVesselInput.from_input(v) for v in vessels_raw] if vessels_raw is not None else None

        monopiles_raw = getattr(input_data, "monopiles", None)
        monopiles_list = [CWMonopileInput.from_input(m) for m in monopiles_raw] if monopiles_raw is not None else None

        return cls(
            resetBeforeRun=bool(reset_flag),
            tripCount=getattr(input_data, "tripCount", getattr(input_data, "trip_count", None)),
            departureDayMin=getattr(input_data, "departureDayMin", getattr(input_data, "departure_day_min", None)),
            departureDayMax=getattr(input_data, "departureDayMax", getattr(input_data, "departure_day_max", None)),
            dischargeDurationDays=getattr(input_data, "dischargeDurationDays", getattr(input_data, "discharge_duration_days", None)),
            vessels=vessels_list,
            monopiles=monopiles_list
        )


class CWPlannerStatusResponse(BaseModel):
    """Response model for GET /api/v1/status"""
    status: str
    service: Optional[str] = None
    endpoints: Optional[Dict[str, str]] = None


class CWPlannerRunResponse(BaseModel):
    """Response model for POST /api/v1/solver/run"""
    best_solver_name: Optional[str] = Field(default=None, alias="bestSolverName")
    best_score: Optional[str] = Field(default=None, alias="bestScore")
    schedule: Optional[Dict[str, Any]] = None
    raw_response: Optional[Dict[str, Any]] = None
