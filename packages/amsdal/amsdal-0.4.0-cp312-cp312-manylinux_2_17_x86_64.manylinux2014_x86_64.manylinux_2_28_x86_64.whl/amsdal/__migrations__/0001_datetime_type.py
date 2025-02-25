from amsdal_utils.models.enums import ModuleType

from amsdal_models.migration import migrations


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.CreateClass(
            module_type=ModuleType.TYPE,
            class_name='Date',
            new_schema={'title': 'Date', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
        migrations.CreateClass(
            module_type=ModuleType.TYPE,
            class_name='Datetime',
            new_schema={'title': 'Datetime', 'properties': {}, 'meta_class': 'TypeMeta'},
        ),
    ]
