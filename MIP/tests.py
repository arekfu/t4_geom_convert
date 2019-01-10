import mip
from mip import surfacecard
from mip import cellcard
from mip import datacard

# fname = "input_slab"
# fname = "0_ITERSDR.i"
# fname = "1_DEMO-HCLL-V2.m5"
# fname = "2_HCLL_ENEA_MCNP_WP13SYS02_T06.txt"
fname = "3_AllOutput.i"
fname = "4_CLITE_V2_REV150304_MOD.m"

input = mip.MIP(fname)

# surfaces = input.cards(blocks='s', skipcomments=True)
# for ss in surfaces:
#     print(ss.position)
#     print(ss.content())
#     print(ss.parts())
#     print('*'*60)

cells = input.cards(blocks='c', skipcomments=True)
for cc in cells:
    # print(cc.position)
    # print(cc.content())
    # print(cc.parts())
    name, mat, geom, opts = cellcard.split(cc.content())
    print(name)
    print(mat)
    print(geom)
    print(opts)
    print('*'*60)


# data = input.cards(blocks='d', skipcomments=True)
# for dat in data:
#     dd = datacard.split(dat.content())
#     if (dd[0] == "m"):
#         print(dd)
#         ZAid = dd[-1].split()[0]
#         abond = dd[-1].split()[1]
#         print(int(ZAid)//1000)
#         print(int(ZAid)%1000)
#         print(abond)
