

SESSION_CONFIG_VALIDATIORS = {
    'frame_width': lambda val: validate_int_range(64, 512, val),
    'frame_height': lambda val: validate_int_range(64, 512, val),
    'frames_stacked': lambda val: validate_int_range(1, 12, val),
    'learning_rate': lambda val: validate_float_range(0.0, 1.0, val),
    'lr_decay': lambda val: validate_float_range(0.0, 1.0, val),
}

DENSE_LAYERS_CONFIG_VALIDATORS = {
    'Units': lambda val: validate_int_range(6, 5000, val),
    'Activation': lambda str: validate_string_in_set(['relu', 'sigmoid', 'linear'], str)
}

CONV_LAYERS_CONFIG_VALIDATORS = {
    'Filters': lambda val: validate_int_range(1, 128, val),
    'Kernel size': lambda val: validate_int_range(1, 12, val),
    'Strides': lambda val: validate_int_range(1, 5, val),
}

def validate_string_in_set(strings, value):
    value = str(value)
    if value not in strings:
        raise ValueError('Value must be on of: {}'.format(', '.join(strings)))
    return value

def validate_float_range(min, max, value):
    value = float(value)
    if not (min <= value <= max):
        raise ValueError('Value must be in range {0}:{1}'.format(min, max))
    return value

def validate_int_range(min, max, value):
    value = int(value)
    if not (min <= value <= max):
        raise ValueError('Value must be in range {0}:{1}'.format(min, max))
    return value

def build_validated(values, validators):
    assert all_values_have_validators(validators, values), 'Incorrect values for validation'

    result_dict = {}
    for value_name in values.keys():
        try:
            result_dict[value_name] = validators[value_name](values[value_name])
        except ValueError as error:
            raise ValueError('Validation failed for {0}, reason: {1}'.format(value_name, str(error)))
        except:
            raise ValueError('Validation failed for {0}'.format(value_name))
    return result_dict


def all_values_have_validators(validators, values):
    return set(values.keys()).issubset(set(validators.keys()))
