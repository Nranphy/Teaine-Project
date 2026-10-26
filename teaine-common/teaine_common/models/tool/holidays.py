from teaine_common.models.base import TeaineModel


class HolidayInfo(TeaineModel):
    date: str
    name: str
    type: str


class HolidayDateInfo(TeaineModel):
    date: str
    is_holiday: bool
    is_workday: bool
    holiday: HolidayInfo | None = None
    day_of_week: int


__all__ = ['HolidayDateInfo', 'HolidayInfo']
