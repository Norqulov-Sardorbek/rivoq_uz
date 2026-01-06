from django.contrib import admin
from .models import (
    Course,
    Module,
    Lesson,
    CourseComment,
    WhatWeOffer,
    WhoIsThisCourseFor,
    Note,
    CourseStudent
)

# =========================
# INLINE ADMINLAR
# =========================

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'duration', 'video_url')
    ordering = ('order',)


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    show_change_link = True


class WhatWeOfferInline(admin.TabularInline):
    model = WhatWeOffer
    extra = 1


class WhoIsThisCourseForInline(admin.TabularInline):
    model = WhoIsThisCourseFor
    extra = 1


# =========================
# COURSE ADMIN
# =========================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_started',
        'is_free',
        'price',
        'lessons_count_display',
        'total_duration_display',
        'average_rating_display',
        'created_datetime'
    )
    list_filter = ('is_started', 'is_free', 'created_datetime')
    search_fields = ('title', 'description', 'teachers')
    readonly_fields = (
        'lessons_count_display',
        'total_duration_display',
        'average_rating_display',
    )
    inlines = [ModuleInline, WhatWeOfferInline, WhoIsThisCourseForInline]
    ordering = ('-created_datetime',)

    def lessons_count_display(self, obj):
        return obj.lessons_count
    lessons_count_display.short_description = "Lessons count"

    def total_duration_display(self, obj):
        return f"{obj.total_duration} min"
    total_duration_display.short_description = "Total duration"

    def average_rating_display(self, obj):
        return round(obj.average_rating or 0, 1)
    average_rating_display.short_description = "Avg rating"


# =========================
# MODULE ADMIN
# =========================

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'course',
        'lessons_count',
        'total_duration',
        'created_datetime'
    )
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    inlines = [LessonInline]


# =========================
# LESSON ADMIN
# =========================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'module',
        'order',
        'duration',
        'created_datetime'
    )
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title')
    ordering = ('module', 'order')


# =========================
# COURSE COMMENT (FEEDBACK)
# =========================

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'user',
        'rating',
        'reaction',
        'created_datetime'
    )
    list_filter = ('rating', 'course')
    search_fields = ('user__email', 'course__title', 'comment')


# =========================
# WHAT WE OFFER
# =========================

@admin.register(WhatWeOffer)
class WhatWeOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')


# =========================
# WHO IS THIS COURSE FOR
# =========================

@admin.register(WhoIsThisCourseFor)
class WhoIsThisCourseForAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')


# =========================
# NOTES
# =========================

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'lesson',
        'user',
        'short_note',
        'created_datetime'
    )
    search_fields = ('user__email', 'lesson__title', 'note')

    def short_note(self, obj):
        return obj.note[:50] + "..." if len(obj.note) > 50 else obj.note
    short_note.short_description = "Note"


# =========================
# COURSE STUDENTS
# =========================

@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'student',
        'in_lesson',
        'created_datetime'
    )
    list_filter = ('course',)
    search_fields = ('student__email', 'course__title')
