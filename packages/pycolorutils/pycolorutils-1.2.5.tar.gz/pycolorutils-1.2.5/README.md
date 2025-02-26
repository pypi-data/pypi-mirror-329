# PyColorUtils

A set of useful utilities for Python. Same vibe as [C-Utils](https://github.com/Pecacheu/C-Utils) and [Utils.js](https://github.com/Pecacheu/Utils.js).

Install via `pip install pycolorutils`

# Color Preset Strings
Format strings for console printing.

- `C.Rst` Reset
- `C.Br` Bright
- `C.Di` Dim
- `C.Un` Underscore
- `C.Bl` Blink
- `C.Rv` Reverse
- `C.Blk` Black
- `C.Red` Red
- `C.Grn` Green
- `C.Ylo` Yellow
- `C.Blu` Blue
- `C.Mag` Magenta
- `C.Cya` Cyan
- `C.Whi` White
- `C.BgBlk` BgBlack
- `C.BgRed` BgRed
- `C.BgGrn` BgGreen
- `C.BgYlo` BgYellow
- `C.BgBlu` BgBlue
- `C.BgMag` BgMagenta
- `C.BgCya` BgCyan
- `C.BgWhi` BgWhite

# Logging & Errors

- `msg(*m)` Like `print()` but automatically appends `C.Rst` to the end.
- `err(e: Any, ex: int=0)` Prints an error to the console (stderr) in red. If `ex` is non-zero, also exits with exit code.
- `warn(w: Any)` Prints a warning to the console (stderr) in yellow.
- `eInfo(e: Exception)` Returns a human-readable string for the exception.
- `onMsg = callable(m: str)` If defined, redirects output from `msg()`
- `onErr = callable(e: str)` If defined, redirects output from `err()`

# Main & Exit

- `execMain(main: callable)` Wraps `main` so that when it ends, all atexit functions are run, even if an exception or interrupt occurs.
- `atexit(f: callable)` Run `f` before exit. More reliable than builtin `atexit` module if `execMain()` is used, falls back on atexit otherwise.
- `exit(ex: int=0)` Overrides builtin `exit` to exit cleanly, with optional exit code.

# Misc

- `getDictKey(d: dict, val: Any)` Returns the first key in `d` whose value is `val`. Raises **ValueError** if not found.