#----------------------------------------------------
def itos(num,digs):
    return((str(num)).zfill(digs))

def ftos(num,digs,dec):
    tmpstring = ""
    fmtstring = "%"+"."+str(dec)+"f"
    tmpstring=fmtstring%num
    return((str(tmpstring).zfill(digs+dec+1)))

#----------------------------------------------------
