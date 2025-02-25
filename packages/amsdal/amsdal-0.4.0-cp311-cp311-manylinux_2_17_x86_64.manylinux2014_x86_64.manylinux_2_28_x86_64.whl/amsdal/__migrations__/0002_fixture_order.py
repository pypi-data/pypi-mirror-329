from amsdal_models.migration import migrations
from amsdal_utils.models.enums import ModuleType


class Migration(migrations.Migration):
    operations: list[migrations.Operation] = [
        migrations.UpdateClass(
            module_type=ModuleType.CORE,
            class_name='Fixture',
            old_schema={
                'title': 'Fixture',
                'required': ['data', 'external_id'],
                'properties': {
                    'class_name': {'type': 'string', 'title': 'Class Name'},
                    'external_id': {'type': 'string', 'title': 'External ID'},
                    'data': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'anything'}},
                        'title': 'Data',
                    },
                },
                "primary_key": {"partition_key": ["partition_key"]},
                "table_name": "Fixture",
                'unique': [['external_id']],
            },
            new_schema={
                'title': 'Fixture',
                'required': ['data', 'external_id'],
                'properties': {
                    'class_name': {'type': 'string', 'title': 'Class Name'},
                    'order': {'type': 'number', 'title': 'Order'},
                    'external_id': {'type': 'string', 'title': 'External ID'},
                    'data': {
                        'type': 'dictionary',
                        'items': {'key': {'type': 'string'}, 'value': {'type': 'anything'}},
                        'title': 'Data',
                    },
                },
                "primary_key": {"partition_key": ["partition_key"]},
                "table_name": "Fixture",
                'unique': [['external_id']],
            },
        ),
    ]
