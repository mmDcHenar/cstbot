from django.db.models import TextChoices


class UnitType(TextChoices):
    THEORETICAL = "theoretical", "Theoretical"
    PRACTICAL = "practical", "Practical"


class CourseType(TextChoices):
    GENERAL = "general", "General"
    FOUNDATIONAL = "foundational", "Foundational"
    SPECIALIZED = "specialized", "Specialized"
    OPTIONAL = "optional", "Optional"


class Group(TextChoices):
    GATE = "gate", "Gate"
    RESTAURANT = "restaurant", "Restaurant"
    DORM = "dorm", "Dorm"
    FACULTY = "faculty", "Faculty"
    BANK = "bank", "Bank"
    OFFICE_BUILDING = "office_building", "Office Building"
    OTHER = "other", "Other"


