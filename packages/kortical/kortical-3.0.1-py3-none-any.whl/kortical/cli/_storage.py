import os
import sys
import yaml
import json

from kortical import api
from kortical.cli._cmd_registry import command
from kortical.helpers.print_helpers import print_error
from kortical.storage.exception import ItemExistsException, ItemNotFoundException, ItemNotWriteableException
from kortical.storage.persistent_cloud_storage import PersistentCloudStorage


@command("storage")
def command_storage(args):
    """
Controls storage in the Kortical Cloud.

usage:
    kortical storage [-h]
    kortical storage set --key=<key> (--value=<value> | --value-from-path=<path>) (--app-name=<app-name> | --shared) [--namespace=<namespace>] [--overwrite]
    kortical storage get --key=<key> (--app-name=<app-name> | --shared) [--namespace=<namespace>]
    kortical storage delete --key=<key> (--app-name=<app-name> | --shared) [--namespace=<namespace>]
    kortical storage list [--app-name=<app-name>]
    kortical storage clear --app-name=<app-name>


options:
    -h, --help         Display help.
    <key>              Item key (i.e the name used to access a piece of data).
    <value>            Item value (i.e the actual data retrieved when specifying a key).
    <app-name>         Refers to a piece of storage only accessible by the specified app.
    --shared           Refers to a piece of storage accessible by all apps.
    <namespace>        The namespace under which you want to manage storage.
    --overwrite        If storing an item which has the same key as an existing item, the old data is overwritten.


commands:
    set                Sets a key/value item in cloud storage.
    get                Retrieves a key/value item in cloud storage.
    delete             Deletes a key/value item in cloud storage.
    list               Returns a list of key/value items in cloud storage.
    clear              Clears all key/value items relevant to the specified app name.

    """

    storage_client = PersistentCloudStorage(args['--app-name'])

    if args['get']:
        try:
            if args['--namespace']:
                item = storage_client.get(name=args['--key'], namespace=args['--namespace'], shared=args['--shared'])
            else:
                item = storage_client.get(name=args['--key'], shared=args['--shared'])
            print(f'{json.dumps(item)}')
        except ItemNotFoundException:
            print_error(f'ERROR: Item not found.')
            sys.exit(1)
    elif args['set']:
        try:
            if args['--value']:
                if args['--namespace']:
                    storage_client.store(name=args['--key'],
                                         item=args['--value'],
                                         namespace=args['--namespace'],
                                         shared=args['--shared'],
                                         allow_overwrite=args['--overwrite'])
                else:
                    storage_client.store(name=args['--key'],
                                         item=args['--value'],
                                         shared=args['--shared'],
                                         allow_overwrite=args['--overwrite'])
            elif args['--value-from-path']:
                if not os.path.isfile(args['--value-from-path']):
                    print_error(f'The path provided {args["--value-from-path"]} is not a file!')
                    sys.exit(1)
                with open(args['--value-from-path'], 'r') as file:
                    if args['--namespace']:
                        storage_client.store(name=args['--key'],
                                             item=file.read(),
                                             namespace=args['--namespace'],
                                             shared=args['--shared'],
                                             allow_overwrite=args['--overwrite'])
                    else:
                        storage_client.store(name=args['--key'],
                                             item=file.read(),
                                             shared=args['--shared'],
                                             allow_overwrite=args['--overwrite'])
        except ItemNotWriteableException:
            print_error('ERROR: Item was not writeable')
            sys.exit(1)
        except ItemExistsException:
            print_error(f'ERROR: Item already exists. Please specify [--overwrite] to overwrite.')
            sys.exit(1)
    elif args['delete']:
        if args['--namespace']:
            storage_client.delete(name=args['--key'], namespace=args['--namespace'], shared=args['--shared'])
        else:
            storage_client.delete(name=args['--key'], shared=args['--shared'])

    elif args['list']:
        items = storage_client.list()
        print(yaml.dump(items, default_flow_style=False))

    elif args['clear']:
        storage_client.clear_storage()
