# Generated by Django 3.2.9 on 2021-12-25 11:45

from django.db import migrations, transaction


def apply_seeding(apps, schema_editor):
    Settings = apps.get_model("demencia", "Settings")
    db_alias = schema_editor.connection.alias

    settings, created = Settings.objects.using(db_alias).get_or_create(pk=1)
    settings.meta_description = "О ДЕМЕНЦИИ Деменция — это синдром, обычно хронический или прогрессирующий, при котором происходит деградация когнитивных функций: памяти, мышления, понимания, речи и способности ориентироваться, считать, познавать и рассуждать."
    settings.main_section_additional = "Фонд «Память поколений» и «Cоюзмультфильм» выпустили мультфильм о диагностике когнитивных изменений"
    settings.about_section_term = "<p>Деменция &mdash; это синдром, обычно хронический или прогрессирующий, при котором происходит деградация когнитивных функций: памяти, мышления, понимания, речи и способности ориентироваться, считать, познавать и рассуждать. Деменция оказывает физическое, психологическое, социальное и экономическое воздействие не только на страдающих ею людей, но и на людей, осуществляющих уход, на их семьи и общество в целом.</p>"
    settings.about_section_info = "<p>Согласно оценкам экспертов Всемирной Организации Здравоохранения, деменцией в мире страдает более 55 миллионов человек в возрасте старше 65 лет.</p>\r\n<p>Ожидается, что к 2030 г. этот показатель вырастет до 78 миллионов, а к 2050 г. &ndash; до 139 миллионов. Согласно статистическим данным новый случай заболевания деменцией появляется каждые 3 секунды. Деменция &mdash; это болезнь, а не нормальное проявление старения.</p>"
    settings.map_section_info = "<p>Центры профилактик когнитивных расстройств у лиц старшего возраста возобновят свою работу после снятия ограничений, введенных в регионе в связи с угрозой распространения новой коронавирусной инфекции.</p>"
    settings.fund_section_info = "<p>Благотворительный фонд &laquo;Память поколений&raquo; был основан почти 6 лет назад 22 июня &ndash; в День памяти и скорби.</p>\r\n<p>Наш фонд помогает ветеранам Великой Отечественной войны и современных боевых действий (в Афганистане, Чечне, Сирии). Всего за время существования фонда мы помогли почти 16000 ветеранов.</p>\r\n<p>Это огромное множество операций, курсов реабилитации, современных протезов и слуховых аппаратов, дорогостоящих колясок и комплектов медикаментов, средств личной гигиены. Но, что важнее, это тысячи изменившихся к лучшему жизней людей</p>"
    settings.save()


def revert_seeding(apps, schema_editor):
    with transaction.atomic():
        Settings = apps.get_model("demencia", "Settings")
        db_alias = schema_editor.connection.alias
        settings = Settings.objects.using(db_alias).filter(pk=1).first()
        if settings:
            settings.meta_description = ""
            settings.main_section_additional = ""
            settings.about_section_term = ""
            settings.about_section_info = ""
            settings.map_section_info = ""
            settings.fund_section_info = ""
            settings.save()


class Migration(migrations.Migration):

    dependencies = [
        ("demencia", "0002_settings"),
    ]

    operations = [
        migrations.RunPython(apply_seeding, revert_seeding),
    ]
