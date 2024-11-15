import re

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from utils.types import UnitType, Group, CourseType


class Text(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False, blank=False)
    text = models.TextField()
    is_button = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"


class TGUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    full_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)

    is_banned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.full_name}"


class Course(models.Model):
    fa_title = models.CharField(max_length=64, null=False, blank=False)
    en_title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="Course English Title",
    )
    offering_semester = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ],
        verbose_name="Offering Semester",
    )
    credit = models.IntegerField(verbose_name="Course Credit")
    quiz_credit = models.IntegerField(default=0, verbose_name="Course Quiz Credit")
    prerequisite_courses = models.ManyToManyField(
        to="self",
        through="PrerequisiteCourse",
        symmetrical=False,
    )
    unit_type = models.CharField(max_length=64, choices=UnitType.choices, verbose_name="Unit Type")
    course_type = models.CharField(max_length=64, choices=CourseType.choices, verbose_name="Course Type")
    has_exam = models.BooleanField(default=True, verbose_name="Course Has Exam?")
    has_project = models.BooleanField(default=False, verbose_name="Course Has Project?")

    def __str__(self) -> str:
        return f"{self.fa_title}"


class PrerequisiteCourse(models.Model):
    class Meta:
        unique_together = ("course", "prerequisite_course")

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Course",
    )
    prerequisite_course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Prerequisite Course",
    )

    def __str__(self) -> str:
        return f"{self.course} {self.prerequisite_course}"


class Place(models.Model):
    name = models.CharField(max_length=64, verbose_name="Name")
    group = models.CharField(max_length=64, choices=Group.choices, verbose_name="Group")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    def __str__(self) -> str:
        return f"{self.name}"


class Phone(models.Model):
    name = models.CharField(max_length=64, verbose_name="Name")
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"^((0|00|\+)?98|0)?(\d{10})$"),
        ],
        verbose_name="Phone Number",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        phone_number_match = re.match(r"^((0|00|\+)?98|0)?(\d{10})$", str(self.phone_number))
        if phone_number_match:
            self.phone_number = "+98" + phone_number_match.group(3)

        super().save(*args, **kwargs)


class Link(models.Model):
    name = models.CharField(max_length=64, verbose_name="Name")
    address = models.URLField(verbose_name="URL Address")

    def __str__(self) -> str:
        return f"{self.name}"
