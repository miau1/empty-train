#!/usr/bin/env python3
import inspect
import json
from opusfilter import filters, FilterABC
from pprint import pprint


def derive_filter_definition(filter_cls):
    filter_spec = inspect.getfullargspec(filter_cls.__init__)

    parameters = {}

    # pprint(filter_spec)
    for arg, default_val in zip(filter_spec.args[1:], filter_spec.defaults or []): # skipping `self`
        type_name = type(default_val).__name__
        # If there is no default value, we have to hard code types, and types like tuple
        # are not supported by the interface
        if type_name in ['NoneType', 'tuple']:
            type_name = 'str'
            if filter_cls.__name__ == 'SimilarityFilter':
                default_val = ' '.join([str(v) for v in list(default_val)])
            else:
                default_val = ''

        parameters[arg] = dict(
            type= type_name,
            default=default_val
        )

    if 'unit' in parameters.keys():
        parameters['unit']['allowed_values'] = ['char', 'word']
    if 'id_method' in parameters.keys():
        parameters['id_method']['allowed_values'] = ['langid', 'cld2', 'fasttext']

    return dict(
        type='bilingual',
        name=filter_cls.__name__,
        display_name=filter_cls.__name__.replace('Filter', ''),
        description=filter_cls.__doc__,
        command=f'opusfilter:{filter_cls.__name__}',
        parameters=parameters
    )

for filter_name, filter_cls in filters.__dict__.items():
    if isinstance(filter_cls, type) \
        and filter_cls.__module__ == filters.__name__ \
        and issubclass(filter_cls, FilterABC):
        with open(f'filters/{filter_name}.json', 'w') as fh:
            json.dump(derive_filter_definition(filter_cls), fh, indent=2)
