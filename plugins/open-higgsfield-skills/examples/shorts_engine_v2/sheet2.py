import os,sys,json
sys.path.insert(0,os.getcwd()); sys.path.insert(1,os.path.dirname(os.path.abspath(__file__))); sys.argv=["x"]
import vid, core
from PIL import Image
TL=json.load(open("timeline.json")); fr=[]
os.makedirs("fr",exist_ok=True)
offs=[float(x) for x in os.environ.get("OFFS","3,3,2,4,3,3,3").split(",")]
for k in range(7):
    s=TL["scenes"][k]; i=int((s["start"]+offs[k])*30); core.frame(i); fr.append(i)
sheet=Image.new("RGB",(270*7,480))
for k,i in enumerate(fr): sheet.paste(Image.open(f"fr/f{i:05d}.png").resize((270,480)),(k*270,0))
sheet.save("sheet.png")
import shutil; shutil.rmtree("fr",ignore_errors=True)
