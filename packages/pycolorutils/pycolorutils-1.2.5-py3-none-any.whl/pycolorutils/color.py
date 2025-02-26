#PyColorUtils; 2024 Pecacheu, MIT

import sys, os, atexit as ae
from traceback import print_exception

class C:
	Rst='\x1b[0m' #Reset
	Br='\x1b[1m' #Bright
	Di='\x1b[2m' #Dim
	Un='\x1b[4m' #Underscore
	Bl='\x1b[5m' #Blink
	Rv='\x1b[7m' #Reverse

	Blk='\x1b[30m' #Black
	Red='\x1b[31m' #Red
	Grn='\x1b[32m' #Green
	Ylo='\x1b[33m' #Yellow
	Blu='\x1b[34m' #Blue
	Mag='\x1b[35m' #Magenta
	Cya='\x1b[36m' #Cyan
	Whi='\x1b[37m' #White

	BgBlk='\x1b[40m' #BgBlack
	BgRed='\x1b[41m' #BgRed
	BgGrn='\x1b[42m' #BgGreen
	BgYlo='\x1b[43m' #BgYellow
	BgBlu='\x1b[44m' #BgBlue
	BgMag='\x1b[45m' #BgMagenta
	BgCya='\x1b[46m' #BgCyan
	BgWhi='\x1b[47m' #BgWhite
	onErr = onMsg = None #Callback

_Ex = []

def msg(*a):
	s=[str(d) for d in a]
	s=' '.join(s)+C.Rst+'\n'
	sys.stdout.write(s)
	if C.onMsg: C.onMsg(s)

def err(e,ex=0):
	e=f"{C.Rst+C.Red}{e}{C.Rst}\n"
	sys.stderr.write(e)
	if C.onErr: C.onErr(e)
	if ex: exit(ex)

def warn(w):
	w=f"{C.Rst+C.Ylo+C.Un}Warning: {w}{C.Rst}\n"
	sys.stderr.write(w)
	if C.onErr: C.onErr(w)

def exit(ex: int=0):
	_exit()
	sys.exit(ex)

def _exit():
	for f in _Ex: f()
	_Ex.clear()

def atexit(f: callable): _Ex.append(f)
ae.register(_exit)

def execMain(main: callable):
	try: main()
	except KeyboardInterrupt: pass
	except Exception as er: print_exception(er)
	_exit()

def eInfo(e: Exception):
	loc=note=''
	tb=getattr(e, '__traceback__', None)
	nl=getattr(e, '__notes__', None)
	if tb:
		while tb.tb_next: tb=tb.tb_next
		fn = os.path.split(tb.tb_frame.f_code.co_filename)[1]
		loc = f" @ {fn}:{tb.tb_lineno}"
	if nl:
		note = f" ({', '.join(nl)})"
	return f"{type(e).__name__}{loc}: {e}{note}"

def getDictKey(d: dict, val):
	return list(d.keys())[list(d.values()).index(val)]