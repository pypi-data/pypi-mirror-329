from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class DeviceInformationObject:
    device_type: str
    device_model: str
    operating_system: str
    os_version: str
    processor: str
    screen_resolution: Optional[str] = None
    ram: Optional[str] = None
    storage_capacity: Optional[str] = None
    serial_number: Optional[str] = None
    carrier: Optional[str] = None
    ip_address: Optional[str] = None
    location_x: Optional[str] = None
    location_y: Optional[str] = None


@dataclass
class Country:
    id: str
    name: str
    flag: Optional[str] = None


@dataclass
class NotificationTypeSettings:
    email: bool = True
    push: bool = True
    in_app: bool = True

    @staticmethod
    def from_json(data: Dict) -> "NotificationTypeSettings":
        return NotificationTypeSettings(
            email=data.get("email", True),
            push=data.get("push", True),
            in_app=data.get("inApp", True),
        )


@dataclass
class NotificationSettings:
    summary: NotificationTypeSettings
    tags: NotificationTypeSettings
    activity: NotificationTypeSettings

    @staticmethod
    def from_json(data: Dict) -> "NotificationSettings":
        return NotificationSettings(
            summary=NotificationTypeSettings.from_json(data.get("summery", {})),
            tags=NotificationTypeSettings.from_json(data.get("tags", {})),
            activity=NotificationTypeSettings.from_json(data.get("activety", {})),
        )


@dataclass
class Birthday:
    day: int
    month: int
    year: int


@dataclass
class Gender:
    value: str


@dataclass
class TimeZone:
    id: str
    name: str
    abbreviation: str


@dataclass
class ProfileImage:
    background: str
    image: str

@dataclass
class Address:
    full_name: str
    street: str
    post_code: str
    city: str
    country: str
    phone_number: Optional[str] = None

    @staticmethod
    def from_json(data: dict) -> "Address":
        """
        Converts JSON data to an Address instance.
        """
        return Address(
            full_name=data["fullName"],
            street=data["street"],
            post_code=data["postCode"],
            city=data["city"],
            country=data["country"],
            phone_number=data.get("phoneNumber"),
        )


@dataclass
class User:
    full_name: str
    user_name: str
    email: str
    uid: str
    user_token: str
    creation_date: datetime
    login_devices: List[DeviceInformationObject]
    profile_image: ProfileImage
    access_level: int
    joined_organizations: List[str] = field(default_factory=list)
    user_preference_meta_data: Dict[str, str] = field(default_factory=dict)
    role: Optional[str] = None
    country: Optional[Country] = None
    notification_settings: Optional[NotificationSettings] = None
    post_code: Optional[int] = None
    birthday: Optional[Birthday] = None
    gender: Optional[Gender] = None
    time_zone: Optional[TimeZone] = None
    address: Optional[Address] = None
    last_open_page_id: Optional[str] = None
    current_organization_id: Optional[str] = None

    @staticmethod
    def from_json(data: Dict) -> "User":
        """Populates a User instance from a JSON dictionary."""

        def transform_device_info(device: Dict) -> Dict:
            return {
                "device_type": device.get("deviceType"),
                "device_model": device.get("deviceModel"),
                "operating_system": device.get("operatingSystem"),
                "os_version": device.get("osVersion"),
                "processor": device.get("processor"),
                "screen_resolution": device.get("screenResolution"),
                "ram": device.get("ram"),
                "storage_capacity": device.get("storageCapacity"),
                "serial_number": device.get("serialNumber"),
                "carrier": device.get("carrier"),
                "ip_address": device.get("ipAddress"),
                "location_x": device.get("locationX"),
                "location_y": device.get("locationy"),
            }

        return User(
            full_name=data["fullName"],
            user_name=data["userName"],
            email=data["email"],
            uid=data["uid"],
            user_token=data["userToken"],
            creation_date=datetime.strptime(data["creationDate"], "%Y-%m-%dT%H:%M:%S"),
            login_devices=[
                DeviceInformationObject(**transform_device_info(device))
                for device in data.get("loginDevices", [])
            ],
            profile_image=ProfileImage(**data["profileImage"]),
            access_level=data["accessLevel"],
            joined_organizations=data.get("joinedorganizations", []),
            user_preference_meta_data=data.get("userPreferenceMetaData", {}),
            role=data.get("role"),
            country=Country(**data["country"]) if "country" in data else None,
            notification_settings=NotificationSettings.from_json(
                data["notificationSettings"]
            )
            if "notificationSettings" in data
            else None,
            post_code=data.get("postCode"),
            birthday=Birthday(**data["birthday"]) if "birthday" in data else None,
            gender=Gender(data["gender"]) if "gender" in data else None,
            time_zone=TimeZone(**data["timeZone"]) if "timeZone" in data else None,
            address=Address.from_json(data["adress"]) if "adress" in data else None,
            last_open_page_id=data.get("lastOpenPageId"),
            current_organization_id=data.get("currentorganizationId"),
        )
