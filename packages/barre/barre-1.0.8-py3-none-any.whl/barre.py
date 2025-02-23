# barre.py
import sys,time
def b(i):
 t=len(i);s=str(t)
 for n,x in enumerate(i,1):print(f'\r[{"|"*int(40*n/t):40}] {n:>{len(s)}}/{t}',end='',flush=1);yield x
 print()