from dxcc import *
import pprint


call="A45WG"

d=dxcc_all()
d.read()
dx=d.find(call)
pprint.pprint(dx)