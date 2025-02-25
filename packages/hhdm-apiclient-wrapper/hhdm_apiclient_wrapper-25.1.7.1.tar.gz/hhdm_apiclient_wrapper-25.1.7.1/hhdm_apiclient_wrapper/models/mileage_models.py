from __future__ import annotations

from .api_models import *

from datetime import datetime
from typing import Dict, List


class ItemMileageRequest(IApiModel):
    def __init__(self, part_item_ids: List[str] = [], assembly_iteration_ids: List[str] = []) -> None:
        self.part_item_ids = part_item_ids
        self.assembly_iteration_ids = assembly_iteration_ids

    def serialize(self) -> Dict:
        return {
            'PartItemIds': self.part_item_ids,
            'AssemblyIterationIds': self.assembly_iteration_ids
        }


class MileageOfEvent:
    def __init__(self, event_id: str, end_date: datetime, number_of_laps: float, mileage_meters: float, time_used_hours: float) -> None:
        self.event_id = event_id
        self.end_date = end_date
        self.number_of_laps = number_of_laps
        self.mileage_meters = mileage_meters
        self.time_used_hours = time_used_hours

    @staticmethod
    def deserialize(**json) -> MileageOfEvent:
        return MileageOfEvent(
            json['EventId'],
            json['EndDate'],
            json['NumberOfLaps'],
            json['MileageMeters'],
            json['TimeUsedHours']
        )


class MileageRecordByEvent:
    def __init__(self, id: str, name: str, events: List[MileageOfEvent]) -> None:
        self.id = id
        self.name = name
        self.events = events

    @staticmethod
    def deserialize(**json) -> MileageRecordByEvent:
        return MileageRecordByEvent(
            json['Id'],
            json['Name'],
            [MileageOfEvent.deserialize(o) for o in json['Events']]
        )


class MileagesResult(Generic[T]):
    def __init__(self, part_item_mileages: List[T] = [], assembly_iteration_mileages: List[T] = [], retrieved_at: datetime = None) -> None:
        self.part_item_mileages = part_item_mileages
        self.assembly_iteration_mileages = assembly_iteration_mileages
        self.retrieved_at = retrieved_at

    @staticmethod
    def deserialize(**json) -> MileagesResult:
        return MileagesResult(
            [MileageRecordByEvent.deserialize(**p) for p in json['PartItemMileages']],
            [MileageRecordByEvent.deserialize(**p) for p in json['AssemblyIterationMileages']],
            json['RetrievedAt']
        )

