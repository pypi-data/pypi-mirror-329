"""Handlers for !commands used by seapie.repl.loop()."""

import inspect
import textwrap
import sys
import seapie.helpers
import seapie.repl

def do_help():
    """Show the help message."""
    info = textwrap.dedent("""
        This >>> shell mimics a normal Python shell. Classes, functions, and so on can
        be can be defined and used like normal. Most built-in Python functions and
        features work as expected. New !commands and magic variables are listed below:

        ⚡  Commands - can be called the same way as !help
          (!h)elp      Show this help message
          (!s)tep      Execute code until next debug event. See !m section for events
          (!w)alk <e>  Execute code until expression <e> evaluates to True in an event
          (!u)p        Move one function call up in callstack, towards current line
          (!d)own      Move one function call down in callstack, towards script start
          (!g)oto <l>  Jump to a given line <l> in the current frame
          (!i)nfo      Show callstack with debug events and source code in current frame.
          (!c)ontinue  Detach the debugger from the code and resume normal execution
          (!p)retty    Toggle prettyprinting of the output
          (!m)ode      Toggle mode between full tracing (slow) and profiling (fast)
                       ├ Debugging events when tracing: call, return, line, exception
                       └ Debugging events when profiling: call, return

        🔮  Magic variables - new builtins, updated every event, try "print(_line_)"
          _line_       Next line's line number
          _source_     Next line's source code
          _path_       Next line's source file
          _return_     Object to be returned if _event_ is return
          _event_      Current debug event, one of call/return/line/exception
          _callstack_  List of frame names in the callstack
          _            Latest evaluated expression (updated on input, not on event)

        📝  Examples for !step and !walk - when !m is set to tracing
          Single step                  !s
          Step until line 8 in ok.py   !w _line_ == 8 and _path_ == '/mydir/abc.py'
          Until an exception event     !w _event_ == 'exception'
          Step forever                 !w False     # Will never eval to True
          No effect                    !w True      # Immediately evals to True
          Step until xyz.asd is found  !w xyz in locals() and hasattr(xyz, 'asd')

        📝  Examples for !step and !walk - when !m is set to profiling
          Step to next return or call  !s
          Step until specific call     !w _event_ == 'call' and _line_ == 123
          Step until specific return   !w _event_ == 'return' and _return_ == None
    """)
    print(info[1:-1]) # slice extra newlines with index

def do_step(f, event, orig_f):
    """Return True if repl working frame is at the top of stack, else print warning."""
    if f is orig_f:
        seapie.helpers.show_callstack(f, event, show_all_frames=False)
        return True
    print("💀  Return to top of callstack with !u before !s.")


def do_walk(f, orig_f, arg):
    """Execute forward based on a given condition."""
    if f is not orig_f:
        return print("💀  Return to top of callstack with !u before !w.")
    try:
        compile(arg, "<string>", "single")
    except (SyntaxError, ValueError, TypeError) as e:
        print(f"💀  See !help for !walk usage. Failed to set walk condition: {str(e)}")
    else:
        seapie.repl.loop.__defaults__[0][0] = arg  # Mutate a mutable default argument.
        print(f"🚶  Walk condition set. Stepping until bool(eval({repr(arg)})) is True")

def do_up(f, event):
    """Selects the next frame up in the callstack as the current working frame."""
    new_f = next((i.frame for i in inspect.stack()[2:] if i.frame.f_back == f), None) or f
    seapie.helpers.show_callstack(new_f, event)  # Show the change regardless
    return new_f

def do_down(f, event):
    """Selects the next frame down in the callstack as the current working frame."""
    new_f = f.f_back or f  # If there's a lower frame, use it; otherwise, stay
    seapie.helpers.show_callstack(new_f, event)  # Show the change regardless
    return new_f


def do_continue():
    """Completely detach seapie from the code and resume normal execution."""
    print("🔌  Detaching seapie")
    seapie.helpers.clear_trace()

def do_pretty():
    """Toggles prettyprinting of the output"""
    pretty = seapie.helpers.displayhook.__defaults__[0]  # The mutable default list.
    pretty[0] = not pretty[0]
    print("✨  Prettyprinting on") if pretty[0] else print("📄  Prettyprinting off")

def do_goto(frame, command_arg):
    """Jump to a given linenumber in the current frame."""
    try:
        frame.f_lineno = int(command_arg)
    except Exception as e:
        print(f"💀  Usage: !jump <line number>. Jump failed: {str(e)}")
    else:
        print("🚀  Jump succeeded. Next line to execute is", command_arg)

def do_mode():
    """toggles lite mode tracing"""
    if sys.getprofile() is None:
        sys.settrace(None)
        sys.setprofile(seapie.repl.loop)
        print("🏃  Debugging mode set to profiling only (calls and returns)")
        return
    if sys.gettrace() is None:
        sys.setprofile(None)
        sys.settrace(seapie.repl.loop)
        print("🐌  Debugging mode set to tracing (calls, returns, lines, exceptions)")
        return

def do_info(frame, event):
    """Shows callstack with events and source code in the current frame."""
    seapie.helpers.show_callstack(frame, event)
    print()
    seapie.helpers.show_source(frame)
