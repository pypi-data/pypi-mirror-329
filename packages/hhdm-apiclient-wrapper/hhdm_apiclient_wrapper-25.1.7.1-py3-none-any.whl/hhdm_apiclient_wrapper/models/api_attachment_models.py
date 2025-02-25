from .api_models import *

from enum import Enum


class ApiAttachmentModel:
    def __init__(self, id: str, signed_url: str, file_name: str, server_attached_file_state: str) -> None:
        self.id = id
        self.signed_url = signed_url
        self.file_name = file_name
        self.server_attached_file_state = server_attached_file_state


class ApiAddAttachedFileResponse:
    def __init__(self, attached_file_id: str, url: str, account_id: str, user_id: str, use_compression: bool) -> None:
        self.attached_file_id = attached_file_id
        self.url = url
        self.account_id = account_id
        self.user_id = user_id
        self.use_compression = use_compression
        self.is_valid = self.attached_file_id and self.url and self.account_id and self.user_id

    def deserialize(**json):
        return ApiAddAttachedFileResponse(
            json['AttachedFileId'],
            json['Url'],
            json['AccountId'],
            json['UserId'],
            json['UseCompression']
        )
    
    def serialize(self) -> Dict:
        return {
            'AttachedFileId': self.attached_file_id,
            'Url': self.url,
            'AccountId': self.account_id,
            'UserId': self.user_id,
            'UseCompression': self.use_compression
        }


class ApiPrepareUploadModel(IApiModel):
    def __init__(self, file_name: str, custom_property_attached_file_name: str | None, if_single_overwrite_existing: bool, auto_download: bool, use_compression: bool) -> None:
        self.file_name = file_name
        self.custom_property_attached_file_name = custom_property_attached_file_name
        self.if_single_overwrite_existing = if_single_overwrite_existing
        self.auto_download = auto_download
        self.use_compression = use_compression

    def serialize(self) -> Dict:
        return {
            'FileName': self.file_name,
            'CustomPropertyAttachedFileName': self.custom_property_attached_file_name,
            'IfSingleOverwriteExisting': self.if_single_overwrite_existing,
            'AutoDownload': self.auto_download,
            'UseCompression': self.use_compression
        }


class AddAttachmentStatus(Enum):
    SUCCESS = 0
    FAILED_TO_ADD = 1
    FAILED_TO_UPLOAD = 2
    FAILED_TO_UPDATE_SERVER_STATUS = 3


class AddAttachmentResult:
    def __init__(self, add_attachment_status: AddAttachmentStatus, add_attached_file_response: ApiAddAttachedFileResponse | None, entity_id: str, file_path: str | None, file_name: str | None, message: Exception | str | None = None) -> None:
        self.add_attachment_status = add_attachment_status
        self.add_attached_file_response = add_attached_file_response
        self.entity_id = entity_id
        self.file_path = file_path
        self.file_name = file_name
        self.message = message


class AddCollectionItemAttachmentResult(AddAttachmentResult):
    def __init__(self, add_attachment_status: AddAttachmentStatus, add_attached_file_response: ApiAddAttachedFileResponse | None, entity_id: str, collection_name: str, collection_item_id: str, file_path: str | None, file_name: str | None, message: Exception | str | None = None) -> None:
        super().__init__(add_attachment_status, add_attached_file_response, entity_id, file_path, file_name, message)
        self.collection_name = collection_name
        self.collection_item_id = collection_item_id
