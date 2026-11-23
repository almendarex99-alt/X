import os,sys,json
sys.path.insert(0,os.getcwd()); sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))); sys.argv=["x"]
import vid, core
from PIL import Image
TL=json.load(open("timeline.json")); fr=[]
os.makedirs("fr",exist_ok=True)
offs=[1.6,2.0,2.6,3.0,3.0,3.0,3.0]
for k in range(7):
    s=TL["scenes"][k]; e=TL["scenes"][k+1]["start"]; i=int((s["start"]+min(offs[k],(e-s["start"])*.8))*30); core.frame(i); fr.append(i)
sheet=Image.new("RGB",(270*7,480))
for k,i in enumerate(fr): sheet.paste(Image.open(f"fr/f{i:05d}.png").resize((270,480)),(k*270,0))
sheet.save("sheet.png")
import shutil; shutil.rmtree("fr",ignore_errors=True)
