# save as tools/build_splits.py (run from repo root)
import os, pathlib, shutil

DATA_ROOT = "/Users/sele/Desktop/AUS_FALL_25/Mobile_Apps/sign-language-gesture-recognition/dataset"  # folder containing user01/, user02/, ...
OUTS = [("train_videos", [f"user{u:02d}" for u in range(1,11)]),
        ("test_videos",  [f"user{u:02d}" for u in range(11,13)])]

label_map = {
 "G01":"Hi","G02":"Please","G03":"What","G04":"Arabic","G05":"University",
 "G06":"You","G07":"Eat","G08":"Sleep","G09":"Go","G10":"UAE"
}

def ensure(p): pathlib.Path(p).mkdir(parents=True, exist_ok=True)

for split_name, users in OUTS:
    for g, label in label_map.items():
        ensure(f"{split_name}/{label}")
    for u in users:
        for g in label_map:
            gdir = pathlib.Path(DATA_ROOT)/u/g
            if not gdir.exists(): continue
            for r in sorted(gdir.glob("R*.mp4")):
                # target file name: u_g_r.mp4 to keep provenance
                tgt = pathlib.Path(split_name)/label_map[g]/f"{u}_{g}_{r.stem}.mp4"
                if tgt.exists(): continue
                # symlink (fallback to copy if needed)
                try:
                    os.symlink(r.resolve(), tgt)
                except Exception:
                    shutil.copy2(r, tgt)
print("Done.")
