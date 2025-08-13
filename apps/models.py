from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, URLField, PositiveIntegerField
from django.db.models import IntegerField, TextChoices, ImageField, DecimalField
from django.db.models import Model, SET_NULL, DateField, ForeignKey, TimeField, CASCADE, DateTimeField, BooleanField
from parler.models import TranslatableModel, TranslatedFields


class CustomUserManager(UserManager):
    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    async def acreate_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class RoleType(TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher', 'Teacher'

    class GenderType(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    phone_number = CharField(max_length=20, unique=True)
    avatar = URLField()
    group = ForeignKey('apps.Group', on_delete=SET_NULL, null=True, blank=True, related_name='students')
    birthday = DateField(null=True, blank=True)
    role = CharField(max_length=100, choices=RoleType, null=True, blank=True)
    gender = CharField(max_length=100, choices=GenderType, null=True, blank=True)
    is_group = BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = ""
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []


class Room(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(max_length=100),
    )
    count = IntegerField(default=0)
    capacity = PositiveIntegerField()

    def __str__(self):
        return f"{self.safe_translation_getter('name', any_language=True)} ({self.capacity} ta)"


class Course(TranslatableModel):
    translations = TranslatedFields(
        name=CharField(max_length=100),
    )
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Group(TranslatableModel):
    class DayType(TextChoices):
        ODD_DAYS = 'odd days', 'Odd days'
        COUPLE_DAYS = 'couple days', 'Couple days'
        MONDAY = 'monday', 'Mondays'
        TUESDAY = 'tuesday', 'Tuesdays'
        WEDNESDAY = 'wednesday', 'Wednesdays'
        THURSDAY = 'thursday', 'Thursdays'
        FRIDAY = 'friday', 'Fridays'
        SATURDAY = 'saturday', 'Saturdays'

    translations = TranslatedFields(
        name=CharField(max_length=100),
    )
    teacher = ForeignKey('apps.User', on_delete=SET_NULL, null=True, blank=True, related_name='teaching_groups')
    time = TimeField()
    course = ForeignKey('apps.Course', on_delete=CASCADE, related_name='groups')
    room = ForeignKey('apps.Room', on_delete=CASCADE, related_name='groups')
    days = CharField(max_length=100, choices=DayType.choices)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Attendance(Model):
    student = ForeignKey('apps.User', on_delete=CASCADE, related_name="attendances")
    group = ForeignKey('apps.Group', on_delete=CASCADE, related_name="attendances")
    date = DateField()
    is_present = BooleanField(default=False)


class Media(Model):
    image = ImageField(upload_to='media/')
