# validator_service/validator.py

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date
import re
import json
import uuid
from django.db import connection

class ValidatorService:
    @staticmethod
    def validate(data, rules, custom_messages=None):
        errors = {}

        for field, rule in rules.items():
            value = data.get(field)
            rules_list = rule.split('|')

            # Check if the field is an array and handle accordingly
            if 'array' in rules_list:
                if not isinstance(value, list):
                    ValidatorService._add_error(
                        errors, field, 'array', {'_attribute': field}
                    )
                else:
                    # Validate each item in the array
                    for index, item in enumerate(value):
                        item_rules = ValidatorService._get_item_rules(field, rules_list)
                        item_errors = ValidatorService.validate_item(item, item_rules, data)
                        if item_errors:
                            errors[field] = errors.get(field, [])
                            errors[field].extend(item_errors)

            for r in rules_list:
                if r == 'required':
                    if not value:
                        ValidatorService._add_error(
                            errors, field, 'required', {'_attribute': field}
                        )
                elif r == 'accepted':
                    if value not in ['yes', 'on', '1', 1, True]:
                        ValidatorService._add_error(
                            errors, field, 'accepted', {'_attribute': field}
                        )
                elif r == 'active_url':
                    try:
                        URLValidator()(value)
                    except ValidationError:
                        ValidatorService._add_error(
                            errors, field, 'active_url', {'_attribute': field}
                        )
                elif r.startswith('after:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        after_date = datetime.strptime(r.split(':')[1], '%Y-%m-%d').date()
                        if input_date <= after_date:
                            ValidatorService._add_error(
                                errors, field, 'after', {'_attribute': field, '_date': r.split(':')[1]}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'after', {'_attribute': field, '_date': r.split(':')[1]}
                        )
                elif r.startswith('after_or_equal:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        after_date = datetime.strptime(r.split(':')[1], '%Y-%m-%d').date()
                        if input_date < after_date:
                            ValidatorService._add_error(
                                errors, field, 'after_or_equal', {'_attribute': field, '_date': r.split(':')[1]}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'after_or_equal', {'_attribute': field, '_date': r.split(':')[1]}
                        )
                elif r == 'alpha':
                    if not re.match(r'^[a-zA-Z]+$', value):
                        ValidatorService._add_error(
                            errors, field, 'alpha', {'_attribute': field}
                        )
                elif r == 'alpha_dash':
                    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
                        ValidatorService._add_error(
                            errors, field, 'alpha_dash', {'_attribute': field}
                        )
                elif r == 'alpha_num':
                    if not re.match(r'^[a-zA-Z0-9]+$', value):
                        ValidatorService._add_error(
                            errors, field, 'alpha_num', {'_attribute': field}
                        )
                elif r == 'array':
                    if not isinstance(value, list):
                        ValidatorService._add_error(
                            errors, field, 'array', {'_attribute': field}
                        )
                elif r.startswith('before:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        before_date = datetime.strptime(r.split(':')[1], '%Y-%m-%d').date()
                        if input_date >= before_date:
                            ValidatorService._add_error(
                                errors, field, 'before', {'_attribute': field, '_date': r.split(':')[1]}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'before', {'_attribute': field, '_date': r.split(':')[1]}
                        )
                elif r.startswith('before_or_equal:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        before_date = datetime.strptime(r.split(':')[1], '%Y-%m-%d').date()
                        if input_date > before_date:
                            ValidatorService._add_error(
                                errors, field, 'before_or_equal', {'_attribute': field, '_date': r.split(':')[1]}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'before_or_equal', {'_attribute': field, '_date': r.split(':')[1]}
                        )
                elif r.startswith('between:'):
                    min_val, max_val = map(int, r.split(':')[1].split(','))
                    if isinstance(value, (int, float)):
                        if not (min_val <= value <= max_val):
                            ValidatorService._add_error(
                                errors, field, 'between:numeric', {'_attribute': field, 'min': min_val, 'max': max_val}
                            )
                    elif isinstance(value, str):
                        if not (min_val <= len(value) <= max_val):
                            ValidatorService._add_error(
                                errors, field, 'between:string', {'_attribute': field, 'min': min_val, 'max': max_val}
                            )
                    elif isinstance(value, list):
                        if not (min_val <= len(value) <= max_val):
                            ValidatorService._add_error(
                                errors, field, 'between:array', {'_attribute': field, 'min': min_val, 'max': max_val}
                            )
                elif r == 'boolean':
                    if value not in [True, False, 1, 0, '1', '0']:
                        ValidatorService._add_error(
                            errors, field, 'boolean', {'_attribute': field}
                        )
                elif r == 'confirmed':
                    if value != data.get(f'{field}_confirmation'):
                        ValidatorService._add_error(
                            errors, field, 'confirmed', {'_attribute': field}
                        )
                elif r == 'date':
                    try:
                        datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        ValidatorService._add_error(
                            errors, field, 'date', {'_attribute': field}
                        )
                elif r.startswith('date_equals:'):
                    try:
                        input_date = datetime.strptime(value, '%Y-%m-%d').date()
                        equals_date = datetime.strptime(r.split(':')[1], '%Y-%m-%d').date()
                        if input_date != equals_date:
                            ValidatorService._add_error(
                                errors, field, 'date_equals', {'_attribute': field, '_date': r.split(':')[1]}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'date_equals', {'_attribute': field, '_date': r.split(':')[1]}
                        )
                elif r.startswith('date_format:'):
                    if value is None:
                        # Only add the 'required' error if the field is not already marked as required
                        if 'required' not in rules_list:
                            ValidatorService._add_error(
                                errors, field, 'required', {'_attribute': field}
                            )
                    else:
                        try:
                            datetime.strptime(value, r.split(':')[1])
                        except ValueError:
                            ValidatorService._add_error(
                                errors, field, 'date_format', {'_attribute': field, 'format': r.split(':')[1]}
                            )
                elif r.startswith('different:'):
                    if value == data.get(r.split(':')[1]):
                        ValidatorService._add_error(
                            errors, field, 'different', {'_attribute': field, '_other': r.split(':')[1]}
                        )
                elif r.startswith('digits:'):
                    if not (value.isdigit() and len(value) == int(r.split(':')[1])):
                        ValidatorService._add_error(
                            errors, field, 'digits', {'_attribute': field, '_digits': r.split(':')[1]}
                        )
                elif r.startswith('digits_between:'):
                    min_digits, max_digits = map(int, r.split(':')[1].split(','))
                    if not (value.isdigit() and min_digits <= len(value) <= max_digits):
                        ValidatorService._add_error(
                            errors, field, 'digits_between', {'_attribute': field, 'min': min_digits, 'max': max_digits}
                        )
                elif r == 'email':
                    try:
                        validate_email(value)
                    except ValidationError:
                        ValidatorService._add_error(
                            errors, field, 'email', {'_attribute': field}
                        )
                elif r.startswith('ends_with:'):
                    if not any(value.endswith(suffix) for suffix in r.split(':')[1].split(',')):
                        ValidatorService._add_error(
                            errors, field, 'ends_with', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r.startswith('exists:'):
                    try:
                        parts = rule.split(":")[1].split(',')
                        if len(parts) != 2:
                            ValidatorService._add_error(
                                errors, field, 'exists', {'_attribute': field}
                            )
                            continue

                        table_name, column = parts

                        if not ValidatorService.table_exists(table_name):
                            ValidatorService._add_error(
                                errors, field, 'exists', {'_attribute': field, '_values': "Table Not Found"}
                            )
                            continue

                        if not ValidatorService.record_exists(table_name, column, item):
                            ValidatorService._add_error(
                                # errors, field, 'exists', {'_attribute': field, '_values': "Data Not Found"}
                                errors, field, 'exists', {'_attribute': field}
                            )
                    except ValueError as e:
                        ValidatorService._add_error(
                            # errors, field, 'exists', {'_attribute': field, '_values': "Data Not Found"}
                            errors, field, 'exists', {'_attribute': field}
                        )
                elif r == 'file':
                    if not hasattr(value, 'file'):
                        ValidatorService._add_error(
                            errors, field, 'file', {'_attribute': field}
                        )
                elif r == 'filled':
                    if not value:
                        ValidatorService._add_error(
                            errors, field, 'filled', {'_attribute': field}
                        )
                elif r.startswith('gt:'):
                    try:
                        if isinstance(value, (int, float)):
                            if value <= float(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gt:numeric', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, str):
                            if len(value) <= int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gt:string', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, list):
                            if len(value) <= int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gt:array', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'gt', {'_attribute': field, '_value': r.split(':')[1]}
                        )
                elif r.startswith('gte:'):
                    try:
                        if isinstance(value, (int, float)):
                            if value < float(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gte:numeric', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, str):
                            if len(value) < int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gte:string', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, list):
                            if len(value) < int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'gte:array', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'gte', {'_attribute': field, '_value': r.split(':')[1]}
                        )
                elif r == 'image':
                    if not hasattr(value, 'image'):
                        ValidatorService._add_error(
                            errors, field, 'image', {'_attribute': field}
                        )
                elif r.startswith('in:'):
                    if value not in r.split(':')[1].split(','):
                        ValidatorService._add_error(
                            errors, field, 'in', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r.startswith('in_array:'):
                    if value not in data.get(r.split(':')[1], []):
                        ValidatorService._add_error(
                            errors, field, 'in_array', {'_attribute': field, '_other': r.split(':')[1]}
                        )
                elif r == 'integer':
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'integer', {'_attribute': field}
                        )
                elif r == 'ip':
                    try:
                        from ipaddress import ip_address
                        ip_address(value)
                    except ValueError:
                        ValidatorService._add_error(
                            errors, field, 'ip', {'_attribute': field}
                        )
                elif r == 'ipv4':
                    try:
                        from ipaddress import IPv4Address
                        IPv4Address(value)
                    except ValueError:
                        ValidatorService._add_error(
                            errors, field, 'ipv4', {'_attribute': field}
                        )
                elif r == 'ipv6':
                    try:
                        from ipaddress import IPv6Address
                        IPv6Address(value)
                    except ValueError:
                        ValidatorService._add_error(
                            errors, field, 'ipv6', {'_attribute': field}
                        )
                elif r == 'json':
                    try:
                        json.loads(value)
                    except json.JSONDecodeError:
                        ValidatorService._add_error(
                            errors, field, 'json', {'_attribute': field}
                        )
                elif r.startswith('lt:'):
                    try:
                        if isinstance(value, (int, float)):
                            if value >= float(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lt:numeric', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, str):
                            if len(value) >= int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lt:string', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, list):
                            if len(value) >= int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lt:array', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'lt', {'_attribute': field, '_value': r.split(':')[1]}
                        )
                elif r.startswith('lte:'):
                    try:
                        if isinstance(value, (int, float)):
                            if value > float(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lte:numeric', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, str):
                            if len(value) > int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lte:string', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                        elif isinstance(value, list):
                            if len(value) > int(r.split(':')[1]):
                                ValidatorService._add_error(
                                    errors, field, 'lte:array', {'_attribute': field, '_value': r.split(':')[1]}
                                )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'lte', {'_attribute': field, '_value': r.split(':')[1]}
                        )
                elif r.startswith('max:'):
                    max_val = int(r.split(':')[1])
                    if isinstance(value, (int, float)):
                        if value > max_val:
                            ValidatorService._add_error(
                                errors, field, 'max:numeric', {'_attribute': field, '_max': max_val}
                            )
                    elif isinstance(value, str):
                        if len(value) > max_val:
                            ValidatorService._add_error(
                                errors, field, 'max:string', {'_attribute': field, '_max': max_val}
                            )
                    elif isinstance(value, list):
                        if len(value) > max_val:
                            ValidatorService._add_error(
                                errors, field, 'max:array', {'_attribute': field, '_max': max_val}
                            )
                elif r.startswith('min:'):
                    min_val = int(r.split(':')[1])
                    if isinstance(value, (int, float)):
                        if value < min_val:
                            ValidatorService._add_error(
                                errors, field, 'min:numeric', {'_attribute': field, '_min': min_val}
                            )
                    elif isinstance(value, str):
                        if len(value) < min_val:
                            ValidatorService._add_error(
                                errors, field, 'min:string', {'_attribute': field, '_min': min_val}
                            )
                    elif isinstance(value, list):
                        if len(value) < min_val:
                            ValidatorService._add_error(
                                errors, field, 'min:array', {'_attribute': field, '_min': min_val}
                            )
                elif r.startswith('mimes:'):
                    if not hasattr(value, 'file'):
                        ValidatorService._add_error(
                            errors, field, 'mimes', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r.startswith('mimetypes:'):
                    if not hasattr(value, 'file'):
                        ValidatorService._add_error(
                            errors, field, 'mimetypes', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r == 'not_in':
                    if value in r.split(':')[1].split(','):
                        ValidatorService._add_error(
                            errors, field, 'not_in', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r == 'not_regex':
                    if re.match(r.split(':')[1], value):
                        ValidatorService._add_error(
                            errors, field, 'not_regex', {'_attribute': field}
                        )
                elif r == 'numeric':
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'numeric', {'_attribute': field}
                        )
                elif r == 'password':
                    # Implement password validation logic here
                    pass
                elif r == 'present':
                    if field not in data:
                        ValidatorService._add_error(
                            errors, field, 'present', {'_attribute': field}
                        )
                elif r == 'regex':
                    if not re.match(r.split(':')[1], value):
                        ValidatorService._add_error(
                            errors, field, 'regex', {'_attribute': field}
                        )
                elif r == 'required_if':
                    # Implement required_if logic here
                    pass
                elif r == 'required_unless':
                    # Implement required_unless logic here
                    pass
                elif r == 'required_with':
                    # Implement required_with logic here
                    pass
                elif r == 'required_with_all':
                    # Implement required_with_all logic here
                    pass
                elif r == 'required_without':
                    # Implement required_without logic here
                    pass
                elif r == 'required_without_all':
                    # Implement required_without_all logic here
                    pass
                elif r == 'same':
                    if value != data.get(r.split(':')[1]):
                        ValidatorService._add_error(
                            errors, field, 'same', {'_attribute': field, '_other': r.split(':')[1]}
                        )
                elif r.startswith('size:'):
                    size_val = int(r.split(':')[1])
                    if isinstance(value, (int, float)):
                        if value != size_val:
                            ValidatorService._add_error(
                                errors, field, 'size:numeric', {'_attribute': field, '_size': size_val}
                            )
                    elif isinstance(value, str):
                        if len(value) != size_val:
                            ValidatorService._add_error(
                                errors, field, 'size:string', {'_attribute': field, '_size': size_val}
                            )
                    elif isinstance(value, list):
                        if len(value) != size_val:
                            ValidatorService._add_error(
                                errors, field, 'size:array', {'_attribute': field, '_size': size_val}
                            )
                elif r.startswith('starts_with:'):
                    if not any(value.startswith(prefix) for prefix in r.split(':')[1].split(',')):
                        ValidatorService._add_error(
                            errors, field, 'starts_with', {'_attribute': field, '_values': r.split(':')[1]}
                        )
                elif r == 'string':
                    if not isinstance(value, str):
                        ValidatorService._add_error(
                            errors, field, 'string', {'_attribute': field}
                        )
                elif r == 'timezone':
                    try:
                        from pytz import timezone
                        timezone(value)
                    except Exception:
                        ValidatorService._add_error(
                            errors, field, 'timezone', {'_attribute': field}
                        )
                elif r == 'unique':
                    try:
                        model, column = r.split(':')[1].split(',')
                        model_class = ValidatorService.get_model_class(model)
                        if model_class.objects.filter(**{column: value}).exists():
                            ValidatorService._add_error(
                                errors, field, 'unique', {'_attribute': field}
                            )
                    except (ValueError, TypeError):
                        ValidatorService._add_error(
                            errors, field, 'unique', {'_attribute': field}
                        )
                elif r == 'uploaded':
                    if not hasattr(value, 'file'):
                        ValidatorService._add_error(
                            errors, field, 'uploaded', {'_attribute': field}
                        )
                elif r == 'url':
                    try:
                        URLValidator()(value)
                    except ValidationError:
                        ValidatorService._add_error(
                            errors, field, 'url', {'_attribute': field}
                        )
                elif r == 'uuid':
                    try:
                        uuid.UUID(value)
                    except ValueError:
                        ValidatorService._add_error(
                            errors, field, 'uuid', {'_attribute': field}
                        )

        if errors:
            return errors
        return None

    @staticmethod
    def _add_error(errors, field, error_type, tokens):
        if field not in errors:
            errors[field] = []
        errors[field].append({
            'error_type': error_type,
            'tokens': tokens
        })

    @staticmethod
    def get_model_class(model_name):
        from django.apps import apps
        return apps.get_model(model_name)
    
    @staticmethod
    def table_exists(table_name):
        """Check if the table exists in the database."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", [table_name])
            return cursor.fetchone()[0]
        
    def record_exists(table_name, column, value):
        # Check if the value is empty
        if value is None or value == '':
            print(f"Value is empty for column {column} in table {table_name}")  # Debugging print
            return False  # or raise an exception, depending on your needs

        with connection.cursor() as cursor:
            query = f"SELECT COUNT(*) FROM {table_name} WHERE {column} = %s"
            cursor.execute(query, [value])
            print("1111111111111111111",table_name)
            print("1111111111111111111",column)
            print("1111111111111111111",value)
            return cursor.fetchone()[0] > 0  # Return True if record exists, False otherwise
        
    @staticmethod
    def _get_item_rules(field, rules_list):
        """Get the rules for array items based on the field name."""
        item_rules = []
        for rule in rules_list:
            if rule.startswith(f"{field}.*"):
                item_rules.append(rule.split('.', 1)[1])  # Get the rule after the '.*'
        return item_rules

    @staticmethod
    def validate_item(item, rules, data):
        """Validate a single item against the provided rules."""
        errors = []
        for rule in rules:
            if rule.startswith('exists:'):
                try:
                    parts = rule.split(":")[1].split(',')
                    if len(parts) != 2:
                        errors.append({
                            'error_type': 'exists',
                            'tokens': {'_attribute': field}
                        })
                        continue

                    table_name, column = parts
                    item_value = item.get(column)  # Get the value from the item
                    print("item_valueitem_valueitem_valueitem_value",item_value)
                    # Check if the value is empty before calling record_exists
                    if item_value is None or item_value == '':
                        errors.append({
                            'error_type': 'exists',
                            'tokens': {'_attribute': field}
                        })
                        continue

                    if not ValidatorService.table_exists(table_name):
                        errors.append({
                            'error_type': 'exists',
                            'tokens': {'_attribute': "Table Not Found"}
                        })
                        continue

                    if not ValidatorService.record_exists(table_name, column, item):
                        errors.append({
                            'error_type': 'exists',
                            'tokens': {'_attribute': field}
                        })

                except ValueError as e:
                    errors.append({
                        'error_type': 'invalid_rule',
                        'tokens': {'message': str(e)}
                    })
        return errors