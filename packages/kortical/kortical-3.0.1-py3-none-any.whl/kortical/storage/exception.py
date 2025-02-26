class ItemExistsException(Exception):
    def __init__(self, storage_type, item_name, namespace):
        message = f'Item {storage_type.join_path(namespace, item_name)} already exists. Specify "allow_overwrite=True" to overwrite'
        super().__init__(message)


class ItemNotFoundException(Exception):
    def __init__(self, storage_type, item_name, namespace):
        message = f'Item {storage_type.join_path(namespace, item_name)} not found in storage or cache.'
        super().__init__(message)


class ItemNotWriteableException(Exception):
    def __init__(self, storage_type, item_name, namespace, item):
        message = f'Item {storage_type.join_path(namespace,item_name)} of type {type(item)} could not be stored.\n' \
                  f'This may be because this type is not supported. ' \
                  f'Please try serializing it into a buffer beforehand as an alternative'
        super().__init__(message)
