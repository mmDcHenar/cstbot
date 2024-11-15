from django.db.models import IntegerChoices


class CourseType(IntegerChoices):
    GENERAL = 1, "general"
    FOUNDATIONAL = 2, "foundational"
    SPECIALIZED = 3, "specialized"
    OPTIONAL = 4, "optional"


class UnitType(IntegerChoices):
    THEORETICAL = 1, "theoretical"
    PRACTICAL = 2, "practical"


class PlaceType(IntegerChoices):
    GATE = 1, "gate"
    RESTAURANT = 2, "restaurant"
    DORM = 3, "dorm"
    FACULTY = 4, "faculty"
    BANK = 5, "bank"
    OFFICE_BUILDING = 6, "office_building"
    OTHER = 7, "other"
