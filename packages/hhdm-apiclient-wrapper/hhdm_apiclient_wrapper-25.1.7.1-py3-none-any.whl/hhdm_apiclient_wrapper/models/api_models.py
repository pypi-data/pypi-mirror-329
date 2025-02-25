from enum import Enum
from typing import Dict, Generic, List, TypeVar

T = TypeVar('T')


class ApiGetResult(Generic[T]):
    def __init__(self, return_value: T, success: bool, message: str | None, status_code: int | None = None) -> None:
        self.return_value = return_value
        self.success = success
        self.message = message
        self.status_code = status_code


class ApiGetOptions:
    def __init__(self, parameters_to_include: List[str]) -> None:
        self.parameters_to_include = parameters_to_include


class IApiModel:
    def serialize(self) -> Dict:
        pass


class ParameterUpdateModel:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
    
    def serialize(self) -> Dict:
        return {
            'Name': self.name,
            'Value': self.value
        }


class CreateModel(IApiModel):
    def __init__(
            self,
            copy_from_last: bool = False,
            copy_all: bool = False,
            index: int | None = None,
            parameter_updates: List[ParameterUpdateModel] = [],
            copy_from_id: str | None = None) -> None:
        self.copy_from_last = copy_from_last
        self.copy_all = copy_all
        self.index = index
        self.parameter_updates = parameter_updates
        self.copy_from_id = copy_from_id

    def serialize(self) -> Dict:
        return {
            'CopyFromId': self.copy_from_id,
            'CopyFromLast': self.copy_from_last,
            'CopyAll': self.copy_all,
            'Index': self.index,
            'ParameterUpdates': list([param.serialize() for param in self.parameter_updates])
        }


class UpdateModel(IApiModel):
    def __init__(self, last_modified_time_max_allowed_value: str | None, parameter_updates: List[ParameterUpdateModel], collection_update_models: Dict[str, List[IApiModel]] = {}) -> None:
        self.last_modified_time_max_allowed_value = last_modified_time_max_allowed_value
        self.parameter_updates = parameter_updates
        self.collection_update_models = collection_update_models
    
    def serialize(self) -> Dict:
        return {
            'LastModifiedTimeMaxAllowedValue': self.last_modified_time_max_allowed_value,
            'ParameterUpdates': list([param.serialize() for param in self.parameter_updates]),
            'CollectionUpdateModels': {k: [x.serialize() for x in v] for k, v in self.collection_update_models.items()}
        }


class AssociatedModelSearchMode(Enum):
    ACCOUNT = 0
    CHAMPIONSHIP = 1
    EVENT = 2
    CAR = 3
    EVENT_CAR = 4


class AssociatedModelSeachObject(IApiModel):
    def __init__(self, associated_model_search_mode: AssociatedModelSearchMode, account_id: str, championship_id: str, event_id: str, car_id: str) -> None:
        self.associated_model_search_mode = associated_model_search_mode
        self.account_id = account_id
        self.championship_id = championship_id
        self.event_id = event_id
        self.car_id = car_id
    
    def serialize(self) -> Dict:
        return {
            'AssociatedModelSearchMode': self.associated_model_search_mode.value,
            'AccountId': self.account_id,
            'ChampionshipId': self.championship_id,
            'EventId': self.event_id,
            'CarId': self.car_id
        }


class AssociationCreateModel(CreateModel):
    def __init__(
            self,
            copy_from_last: bool = False,
            copy_all: bool = False,
            index: int | None = None,
            parameter_updates: List[ParameterUpdateModel] = [],
            copy_from_id: str | None = None,
            **associations_to_add) -> None:
        super().__init__(copy_from_last, copy_all, index, parameter_updates, copy_from_id)
        self.associations_to_add = associations_to_add

    def serialize(self) -> Dict:
        return {
            **super().serialize(),
            **self.associations_to_add
        }


class AssociationUpdateModel(UpdateModel):
    def __init__(self, last_modified_time_max_allowed_value: str, parameter_updates: List[ParameterUpdateModel], collection_update_models: Dict[str, List] = {}, **associations) -> None:
        super().__init__(last_modified_time_max_allowed_value, parameter_updates, collection_update_models)
        self.associations = associations

    def serialize(self) -> Dict:
        return {
            **super().serialize(),
            **self.associations
        }
