from django.db import migrations, models


def set_position_values(apps, schema_editor):
    MapPoint = apps.get_model("demencia", "MapPoint")
    Partner = apps.get_model("demencia", "Partner")
    Slider = apps.get_model("demencia", "Slider")
    MainMenuElement = apps.get_model("demencia", "MainMenuElement")
    LeftMenuElement = apps.get_model("demencia", "LeftMenuElement")

    model_list = [MapPoint, Partner, Slider, MainMenuElement, LeftMenuElement]
    for model in model_list:
        position = 0
        for instance in model.objects.all():
            position += 1
            instance.position = position
            instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('demencia', '0008_auto_20220127_0001'),
    ]

    operations = [
        migrations.RunPython(set_position_values)
    ]
