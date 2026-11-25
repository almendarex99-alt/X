# Lee los tensores de los .pt (zip) sin des-serializar pickle: solo el bloque de datos float32.
import zipfile,numpy as np,sys,os
d=sys.argv[1];out={}
for f in sorted(os.listdir(d)):
    z=zipfile.ZipFile(os.path.join(d,f));names=[n for n in z.namelist() if '/data/' in n and not n.endswith('/')]
    raw=z.read(names[0]);a=np.frombuffer(raw,dtype='<f4')
    assert a.size==510*256,(f,a.size,names)
    out[f[:-3]]=a.reshape(510,1,256).copy();print(f,names,float(a.mean()),float(a.std()))
np.savez(sys.argv[2],**out)
