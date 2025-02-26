def clean_numpy_types_from_dict(unclean_dict):
    for k, v in unclean_dict.items():
        if hasattr(v, 'dtype'):
            try:
                if 'time' in dir(v):
                    python_v = v(0, 'D')
                else:
                    python_v = v.item()
                    print(f'Converted tag key [{k}] which is [{type(v)}] from a numpy to a python type [{type(python_v)}]')
                    unclean_dict[k] = python_v
            except:
                raise Exception(f'Could not convert value of key [{k}] which is [{type(v)}] from a numpy to a python type')
    return unclean_dict
