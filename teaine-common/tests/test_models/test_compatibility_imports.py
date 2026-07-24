from teaine_common.enum import ActivityTypeEnum
from teaine_common.models.record import Activity, Generation, Interaction, UserInfo


def test_legacy_enum_import_path_is_available() -> None:
    assert ActivityTypeEnum.live.value == "live"


def test_legacy_record_import_path_is_available() -> None:
    assert Activity.__name__ == "Activity"
    assert Generation.__name__ == "Generation"
    assert Interaction.__name__ == "Interaction"
    assert UserInfo.__name__ == "UserInfo"
