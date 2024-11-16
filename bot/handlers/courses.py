from aiogram import Router
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from bot import callback_data as Q
from bot.keyboards import Keyboard as K
from bot.texts import get_message_text as _, get_button_text as __
from core.models import Course, PrerequisiteCourse
from utils.types import CourseType, UnitType

router = Router(name="courses")


@router.message(lambda e: e.text == __("courses"))
async def courses_menu(event: Message) -> None:
    await event.answer(_("courses_menu"), reply_markup=K.course())


@router.callback_query(Q.CoursesFilter.filter())
async def courses_filter(event: CallbackQuery, callback_data: Q.CoursesFilter) -> None:
    if callback_data.filter_by == "semester":
        if callback_data.value is not None:
            courses = [course async for course in Course.objects.filter(offering_semester=callback_data.value).all()]
            text = _("semester_courses_menu", offering_semester=callback_data.value)
        else:
            courses = None
            text = _("courses_by_semester_menu")

    elif callback_data.filter_by == "type":
        if callback_data.value is not None:
            courses = [course async for course in Course.objects.filter(course_type=callback_data.value).all()]
            text = _("type_courses_menu", course_type=__(CourseType(callback_data.value).label))
        else:
            courses = None
            text = _("courses_by_type_menu")

    else:
        courses = None
        text = _("courses_menu")

    await event.message.edit_text(text, reply_markup=K.course(filter_by=callback_data.filter_by, courses=courses))


@router.callback_query(Q.Course.filter())
async def course_details(event: CallbackQuery, callback_data: Q.Course) -> None:
    @sync_to_async
    def get_prerequisite_courses_text(_course: Course) -> str:
        prerequisite_courses = PrerequisiteCourse.objects.filter(course=_course).all()
        if prerequisite_courses:
            return "، ".join([p.prerequisite_course.fa_title for p in prerequisite_courses])
        return "-"

    course = await Course.objects.aget(id=callback_data.id)

    text = _(
        "course_details",
        fa_title=course.fa_title,
        en_title=course.en_title,
        offering_semester=(course.offering_semester if course.offering_semester is not None else "-"),
        credit=course.credit,
        quiz_credit=course.quiz_credit,
        prerequisite_courses=await get_prerequisite_courses_text(_course=course),
        unit_type=_(UnitType(course.unit_type).label),
        course_type=__(CourseType(course.course_type).label),
        has_exam="✅" if course.has_exam else "❌",
        has_project="✅" if course.has_project else "❌",
    )
    await event.message.edit_text(text, reply_markup=K.course(filter_by=callback_data.filter_by, course=course))
