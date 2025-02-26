import ast
from functools import partial
import inspect
import sys
import sysconfig
import xxhash
from .ast_node_visitor_with_context import AstNodeVisitorWithContext
from ..wrapper import Wrapper


class CallableTree(AstNodeVisitorWithContext):

    def __init__(self, callable, parameters=None, parent_callables=set()):
        args = None
        if isinstance(callable, (partial, Wrapper)):
            args = callable.args
            callable = callable.func
        code = inspect.getsource(callable)
        super().__init__(code)
        tree = ast.parse(code)
        callables = set()
        self.callable_names = []
        self.local_callable_names = []
        if parameters is None:
            parameters = set()
        elif isinstance(parameters, (list, tuple)):
            parameters = set(parameters)
        self.visit(tree, context={'locals': parameters})
        for c in self.local_callable_names:
            # useful for debugging print(f"Warning function changes for [{'.'.join(c)}] not tracked")
            pass

        module = sys.modules[callable.__module__]
        sys_paths = sysconfig.get_paths().values()

        for c in self.callable_names:
            object = module
            for n in c:
                if hasattr(object, n):
                    object = getattr(object, n)
                    try:
                        file = inspect.getfile(object)
                    except TypeError:
                        object = module
                        break

                    if any([file.startswith(p) for p in sys_paths]):
                        object = module
                        break
                elif n in __builtins__:
                    break
                else:
                    object = module
                    break

            if object is not module:
                callables.add(object)

        all_callables = callables
        union_callables = callables.copy()
        union_callables.update(parent_callables)
        for c in callables.difference(parent_callables):
            # useful for debugging print(f"Callable [{c.__name__}]\nModule [{c.__module__}]\nFile [{inspect.getfile(c)}]")
            t = CallableTree(c, parameters=set(inspect.signature(c).parameters.keys()), parent_callables=union_callables)
            all_callables.update(t.callables)

        self.callables = all_callables

        # get hash
        x = xxhash.xxh64()
        x.update(code)
        x.update(str(args))
        for c in sorted(self.callables, key=lambda x: x.__name__):
            x.update(inspect.getsource(c))
        self.hash = x.digest()

    def get_hash(self):
        return self.hash

    def visit_Call(self, node, context):
        function_name = None
        if isinstance(node.func, ast.Name):
            function_name = [node.func.id]
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                function_name = [node.func.value.id, node.func.attr]
            else:
                # useful for debugging print(f"Warning function changes for [{node.func.attr}] not tracked")
                pass

        if function_name:
            if function_name[0] not in context['locals']:
                self.callable_names.append(function_name)
            else:
                self.local_callable_names.append(function_name)
        super().generic_visit(node, context)
