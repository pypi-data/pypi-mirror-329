"""Helpers used by seapie.repl and seapie.commands. Not intended for direct use."""

import builtins
import inspect
import os
import platform
import shutil
import traceback
import pprint
import contextlib
import pathlib
import sys

import seapie.commands
import seapie.helpers
import seapie.repl

def get_term_width():
    return shutil.get_terminal_size()[0]

def displayhook(obj, pretty=[True]):  # Mutable default must be one of [True]/[False]
    """Used with sys.displayhook. Implements prettyprinting and mimics the _ in repl."""
    if obj is not None:
        pprint.pp(obj, width=get_term_width()) if pretty[0] else print(obj)
        builtins._ = obj  # Store the new value as _.

def should_not_trace(f, event):
    """True when exit/own-set_trace/unhandled-exc in process or event not in c/l/r/e."""
    if f.f_code in (exit.__call__.__code__, seapie.set_trace.__code__):
        return True  # Dont trace exit() process. Don't trace own breakpoint.
    if event not in ("call", "line", "return", "exception") or hasattr(sys, "last_exc"):
        return True  # Only trace these events. Don't trace unhandled exc process.

def show_callstack(f, current_event, show_all_frames=True):
    """Shows current callstack with working frame marked with ->."""
    print("Callstack (currently selected frame marked):") if show_all_frames else None
    for idx, i in enumerate(inspect.stack()[3:]): # 3 is seapie frames to hdie
        selector = "👈" if (f == i.frame and show_all_frames) else ""
        event = "call" if idx != 0 else current_event  # Show call event for all but the first frame.
        inf = f"'{event}' event on line {i.lineno} in '{i.function}' at {os.path.basename(i.filename)}"
        print(f'  <{inf}> {selector}'[:get_term_width()])
        if not show_all_frames:
            break

def show_traceback(hide, repl_tb):
    """Show tb w/o seapie. hide: # of seapie frames. repl_tb: show exc from repl."""
    ex_type, ex, ex_tb = sys.exc_info() # Capture exception info if any
    print("Traceback (most recent call last):", file=sys.stderr)  # Show tb header.
    # Show frames of the original source without seapie frames or seapie repl frames.
    print(*traceback.format_list(traceback.extract_stack(sys._getframe(hide))), end="")
    if repl_tb:  # If True, show frames of exception generated in seapie repl.
        # [2:] hides seapie frames. 2 happens to be the right num where the arg is True.
        print("".join(traceback.format_list(traceback.extract_tb(ex_tb)[2:])), end="")
    if ex_type is not None:  # Show "TypeError: wrong type" or such if exception exists.
        print(f"{ex_type.__name__}{': ' + str(ex) if str(ex) else ''}", file=sys.stderr)

def show_source(f, context=9):
    """Print source lines surrounding the current line in the given frame."""
    print("Source lines (selected frame):")  # show header
    try:
        lines = pathlib.Path(f.f_code.co_filename).read_text().splitlines()
    except Exception:
        print(f"  Can't read source: {pathlib.Path(f.f_code.co_filename).name}")
        return
    start = max(f.f_lineno - context, 1)  # Ensure start is at least 1.
    end = min(f.f_lineno + context, len(lines))  # Ensure end doesn't hit EOF.
    for lineno in range(start, end + 1):
        marker = "👈" if lineno == f.f_lineno else " "
        lno_str = str(lineno).rjust(len(str(end)) + 2)  # Align line numbers.
        print(f"{lno_str} {lines[lineno - 1].rstrip()} {marker}"[:get_term_width()])

def update_magic_variables(f, event, arg):
    """Based on current working frame, update magic vars in builtins for use in repl."""
    cl = ""  # Source line.
    with contextlib.suppress(Exception):
        cl = pathlib.Path(f.f_code.co_filename).read_text().splitlines()[f.f_lineno - 1]
    builtins._line_ = f.f_lineno
    builtins._source_ = cl
    builtins._path_ = f.f_code.co_filename
    builtins._return_ = arg if event == "return" else None
    builtins._event_ = event  # [2:] To hide seapie from callstack.
    builtins._callstack_ = list(reversed([i.function for i in inspect.stack()[2:]]))

def walk_handler(walk, orig_f):
    """for use in repl"""
    """Attempts to eval walk condition. Return True if conditions is not met (true to step), clears the mutable default on exception, returns None if condition is met"""
    try:
        return bool(eval(walk[0], orig_f.f_globals, orig_f.f_locals))
    except Exception as e:
        tip, problem = {
            NameError: ("'!w x in locals() and <condition>'", "x"),
            AttributeError: ("""'!w hasattr(x, "y") and <condition>'""", "x.y"),
            IndexError: ("'!w len(x) > y and <condition>'", "x[y]"),
            KeyError: ("'!w y in x and <condition>'", "x[y]"),
            ZeroDivisionError: ("'!w x != 0 and <condition>'", "y/x")
        }.get(type(e), None)
        exc_name = type(e).__name__
        print(f"Removing walk condition due to error: {exc_name}: {e}")
        if tip is not None:
            print(f"Tip: use {tip} to avoid transient {exc_name}s on {problem}")
        walk[0] = None

def clear_trace():
    """Stop all tracing and profiling, clear _ from displayhook, clear magic vars."""
    sys.settrace(None)   # Stop tracing in general.
    [setattr(f, "f_trace", None) for f in inspect.stack()]  # Clear trace in all frames.
    d = ["_", "_line_", "_source_", "_path_", "_return_", "_event_", "_callstack_"]
    [delattr(builtins, i) for i in d if hasattr(builtins, i)]  # Clear magic vars.
    sys.setprofile(None)  # Stop profiling if it was set when clear_trace was called.
    sys.displayhook = sys.__displayhook__  # Reset displayhook to default.

def set_trace(show_banner=True):
    """Roughly equivalent to pdb.set_trace. Call this to start a repl (>>> ... ...)."""
    if sys.gettrace() is seapie.repl.loop or sys.getprofile() is seapie.repl.loop:
        return  # Don't trace own breakpoint or repl loop.
    if sys.gettrace() is not None or sys.getprofile() is not None:
        raise RuntimeError("Can't trace. Another tracer or profiler already in use.")
    sys.displayhook = displayhook  # Displayhook for prettyprinting and _ in repl.
    with contextlib.suppress(ImportError):
        import readline  # Needed for line editing if available.
    if hasattr(sys, "ps1"):
        print("Warning: using seapie outside of scripts can cause undefined behaviour.")
    if show_banner:
        #print(f"🥧  seapie {seapie.__version__} on {platform.system()}{sys.version}")
        #print('Type "!h" or "!help" for seapie help.')



        version = sys.version.split()[0]  # Extract Python version
        compiler = platform.python_compiler()  # Get compiler info
        os_name = sys.platform  # Get OS name

        print(f"🥧  seapie {seapie.__version__} (Python {version}) [{compiler}] on {os_name}")
        print('Type "!help" or "!h" for seapie help.')

    sys.settrace(seapie.repl.loop)  # Start the actual tracing. This must be done last.
    frame = sys._getframe(1)  #  Trace is set last as after it this func loses control.
    while frame:  # The control is returned to this function after tracing is stopped.
        frame.f_trace = seapie.repl.loop
        frame = frame.f_back  # Loop will update magic variables. No need to do it here.
