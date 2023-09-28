from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence
from RestrictedPython.PrintCollector import PrintCollector

safe_builtins["_print_"] = PrintCollector
safe_builtins["_getiter_"] = default_guarded_getiter
safe_builtins["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
# safe_builtins["help"] = lambda f: print(help(f))
safe_builtins.update(
    {
        i.__name__: i
        for i in [
            dict,
            dir,
            enumerate,
            filter,
            format,
            list,
            map,
            max,
            min,
            reversed,
            set,
            sum,
            type,
        ]
    }
)

restricted_globals = dict(
    __builtins__=safe_builtins,
    math=__import__("math"),
    itertools=__import__("itertools"),
    functools=__import__("functools"),
    random=__import__("random"),
)


if __name__ == "__main__":
    from RestrictedPython import compile_restricted

    code = compile_restricted("print(help(help)); result=printed")
    locals_dict = {}
    exec(code, restricted_globals, locals_dict)
    print(locals_dict["result"])
