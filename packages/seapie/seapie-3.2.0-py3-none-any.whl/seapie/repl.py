"""the only function you should use from here is prompt.

there is global state and everything is monolitchic to simplify the structure
of the debugger; the amount of argument passing is reduced and there is no
need for a class. The top priority was to simlify prompt() and repl_loop()
"""

import codeop
import ctypes
import sys
import types

import seapie.commands
import seapie.helpers

def get_repl_input():
    """Reads a (multiline) input like Python interpreter does. Returns '!command' or compiled code."""
    lines = []
    while True:  # read input until it is completed or fails or we get a command
        exit() if sys.stdin.closed else None  # Check for closed status to avoid printing prompt unnecessarily when already closed
        lines.append(input(">>> " if not lines else "... "))
        if lines[0].startswith("!"):  # Got a command on first line.
            return lines[0]
        compiled = codeop.compile_command("\n".join(lines), "<seapie>", "single")
        if compiled:
            return compiled  # Compilation returns None of given start of valid code.

def loop(f, event, arg, walk=[None]):
    """args: frame, event, arg
    read-evaluate-print-loop that gets called when tracing code. this basically gets run between evey line
    under the hood the return value is ignored or used to set local trace function depending on the event.

    the mutable default walk is used to store the walk condition. it is a list with one element that is the condition
    it will always the either the value [None] or [condition] where condition is a string that can be compiled
    this is the same list every time the function is called, the mutable default is used to allow modifying
    the function state without using global variables
    """

    orig_f = f  # Save the original frame for later use if working frame changes.

    if seapie.helpers.should_not_trace(f, event):
        return  # Don't trace uncaught error process, exit() process, or own breakpoint. no need to check for set fast forward as the function is not use facing

    while True:  # This is the main repl (>>> ... ) loop. It's triggered between every line of source code

        seapie.helpers.update_magic_variables(orig_f, event, arg) # should these be updated only when code is stepped?
        if walk[0] and not seapie.helpers.walk_handler(walk, orig_f):  # if walk condition is set and evals to false, step
            return loop

        try:  # User input is read and all possible exceptions for the input are handled.
            inp = None  # clear rpevious input and default it to None in case of error
            inp = get_repl_input()  # input is either code or command
        except EOFError:  # Mimic EOF behaviour from ctrl+d  by user in input.
            exit(print())  # Print a newline before exit. Return value doesn't get printed.
        except KeyboardInterrupt:  # Mimic kbint from ctrl+c by user in input. this cant be handled the same as use giving raise kbit as input
            print()
            seapie.helpers.show_traceback(2, repl_tb=False)  # hide dynamic part of error from seapie input with None
        except (SyntaxError, ValueError, OverflowError, UnicodeDecodeError):  # Parsing fail in get_repl_input in compile. do we need to catch more?
            seapie.helpers.show_traceback(2, repl_tb=False)  # Hide the dynamic part of the tb from seapie by giving None, otherwise stuff from compiling is seen

        try:  # Try to exec user input if codetype was succesfully returned from input
            exec(inp, f.f_globals, f.f_locals) if type(inp) is types.CodeType else None
            ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(f), ctypes.c_int(1))
        except (MemoryError, SystemExit):  # Must reraise critical errors.
            raise
        except BaseException:  # Show trace for misc. exec_input errors like invalid syntax.
            seapie.helpers.show_traceback(2, repl_tb=True)

        if type(inp) is str:  # User input was a command command. Handle it.
            cmd_name, *cmd_arg = inp[1:].split(" ", 1) # Separate command from argument(s).
            if cmd_arg and cmd_name not in ("g", "w", "goto", "walk"):  # Check if command takes arguments.
                print("This command doesn't take arguments. Ignoring them.")
            if cmd_name in ("h", "help"):  # help
                seapie.commands.do_help()
            elif cmd_name in ("d", "down"):  # down
                f = seapie.commands.do_down(f, event)  # Update current working frame if able.
            elif cmd_name in ("u", "up"):  # up
                f = seapie.commands.do_up(f, event)  # Update current working frame if able.
            elif cmd_name in ("s", "step"):  # step
                if seapie.commands.do_step(f, event, orig_f):
                    return loop
            elif cmd_name in ("c", "continue"):  # run
                seapie.commands.do_continue()
                return None  # or return repl?
            elif cmd_name in ("g", "goto"):  # goto
                seapie.commands.do_goto(f, cmd_arg[0] if cmd_arg else None)
            elif cmd_name in ("i", "info"):  # info
                seapie.commands.do_info(f, event)
            elif cmd_name in ("p", "pretty"):  # prettyprint
                seapie.commands.do_pretty()
            elif cmd_name in ("w", "walk"):  # walk
                seapie.commands.do_walk(f, orig_f, cmd_arg[0] if cmd_arg else None)
            elif cmd_name in ("m", "mode"):
                seapie.commands.do_mode()
            else:
                print(f"Invalid command !{cmd_name}")
