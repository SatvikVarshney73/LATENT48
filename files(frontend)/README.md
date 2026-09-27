# Cycle Search

Local search interface for the campus cycle-theft tracking pipeline
(Granica x IIT Guwahati Hackathon). A student enters their registered
cycle ID and gets a ranked shortlist of campus locations where their
cycle is most likely to be — with photo evidence and a visual
similarity score from CLIP.

This app does **not** run the CLIP model itself. All the embedding +
matching happens in the Colab notebook; this app just reads the
resulting similarity table and photos, and lets a student query it.

## 1. Export data from the Colab notebook

At the end of Step 6 (embeddings + matching) in the notebook, after
`all_sims` and `cycle_ids` exist, add and run this cell:

```python
# --- Export for the Cycle Search app ---
export_df = sightings_df[["sighting_id", "day", "location", "time", "image_path"]].copy()
for i, cid in enumerate(cycle_ids):
    export_df[cid] = all_sims[:, i]

export_df.to_csv("data/similarity_matrix.csv", index=False)
print("saved data/similarity_matrix.csv with columns:", list(export_df.columns))

import shutil
shutil.make_archive("cycle_search_data", "zip", "data")
files.download("cycle_search_data.zip")
```

This downloads `cycle_search_data.zip`, which contains
`similarity_matrix.csv` plus every sighting photo, with the same
relative paths the CSV points to.

## 2. Put the data in this repo

Unzip `cycle_search_data.zip` and merge its contents into this
repo's `data/` folder, so it looks like:

```
cycle-search-app/
└── data/
    ├── similarity_matrix.csv
    ├── registrations/
    │   └── CYC-001/ ...
    └── sightings/
        └── Day1/
            ├── ADMIN_0935_SJ_01.jpg
            └── ...
```

The `image_path` column in `similarity_matrix.csv` already points to
`data/sightings/Day1/<file>.jpg`, so as long as the folder structure
matches, the app will find the photos automatically.

## 3. Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) —
open it, type a cycle ID like `CYC-005`, and the top matching
locations will show up with photos and scores.

## 4. Notes for submission

- `CONF_THRESHOLD` at the top of `app.py` should match whatever value
  you settled on in the notebook, so the "Confident match" tag stays
  consistent between the notebook and the demo.
- Real registration/sighting photos are not committed to this repo by
  default — add your own `data/` folder (or a small sample, per the
  hackathon's "data sample + schema" submission requirement) before
  pushing.
