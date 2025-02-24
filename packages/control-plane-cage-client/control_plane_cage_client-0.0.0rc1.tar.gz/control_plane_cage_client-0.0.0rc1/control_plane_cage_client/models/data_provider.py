from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_provider_settings import DataProviderSettings


T = TypeVar("T", bound="DataProvider")


@_attrs_define
class DataProvider:
    """Someone who provides Data

    Attributes:
        role (Union[Unset, str]):  Example: DataProvider.
        data_contract (Union[Unset, str]): ID of the data contract that describes the expected structure of the provided
            data.
        settings (Union[Unset, DataProviderSettings]):
    """

    role: Union[Unset, str] = UNSET
    data_contract: Union[Unset, str] = UNSET
    settings: Union[Unset, "DataProviderSettings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        data_contract = self.data_contract

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if data_contract is not UNSET:
            field_dict["dataContract"] = data_contract
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_provider_settings import DataProviderSettings

        d = src_dict.copy()
        role = d.pop("role", UNSET)

        data_contract = d.pop("dataContract", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, DataProviderSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = DataProviderSettings.from_dict(_settings)

        data_provider = cls(
            role=role,
            data_contract=data_contract,
            settings=settings,
        )

        data_provider.additional_properties = d
        return data_provider

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
