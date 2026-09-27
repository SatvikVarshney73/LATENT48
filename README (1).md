# LATENT48 — Cycle Search

**Granica × IIT Guwahati Hackathon — "Bring the Physical World to AI"**

## The problem

Cycles get stolen or misplaced on campus regularly, and there is no
shared record of where cycles have last been seen. A student who
loses their cycle has no way to check whether it's been spotted
somewhere else on campus — they can only ask around or walk to every
cycle stand themselves.

**User:** any student who registers a cycle on campus.
**Question:** "Has my cycle been seen anywhere recently, and where?"

## Our approach

1. **Registration** — students register their cycle through a Google
   Form: name/roll number, declared features (colour, brand, marks),
   and 3 reference photos. Responses land in a Google Sheet /
   `registrations.csv` + a Drive folder of photos.
2. **Sighting collection** — team members walk cycle stands around
   campus and photograph what's parked there, tagging each photo with
   location, time, and collector via the filename
   (`LOCATION_HHMM_COLLECTOR_SEQ.jpg`).
3. **Matching** — a Colab notebook downloads both sets of photos,
   builds a CLIP (ViT-B/32) visual embedding for every registered
   cycle and every sighting, and computes cosine similarity between
   them.
4. **Search** — a local Streamlit app lets a student type their
   cycle ID and see the top 5 campus locations ranked by visual
   similarity to their registered cycle, each with a photo and a
   confidence tag.

```
real problem → cycle registration + campus photo sweeps →
structured sighting data → CLIP similarity search → ranked location shortlist
```

## Repo structure

```
LATENT48/
├── README.md                     <- this file
├── schema.md                     <- data dictionary for the CSVs
├── notebook/
│   └── cycle_pipeline.ipynb      <- full pipeline: download, embed, match, export
└── cycle-search-app/
    ├── app.py                    <- Streamlit search interface
    ├── requirements.txt
    ├── README.md                 <- setup instructions for the app specifically
    └── data/
        ├── similarity_matrix.csv <- sighting × registered-cycle similarity scores
        └── sightings/Day1/       <- sample sighting photos (subset — see schema.md)
```

## How the matching works

Every photo (registration and sighting) is passed through a
pretrained CLIP model to get a 512-dimension embedding — a numeric
"visual fingerprint." A registered cycle's fingerprint is the average
of its 3 reference photos. Each sighting is compared against every
registered cycle's fingerprint using cosine similarity. The single
best match feeds a coarse `matched_cycle_id` / `confidence` field for
overall pipeline metrics, while the full similarity matrix (every
sighting × every cycle) feeds the search app, so a student sees a
ranked shortlist rather than a single guess.

**Known limitation:** CLIP is a general-purpose semantic model, not
fine-tuned for distinguishing near-identical bicycles. Similarity
scores cluster in a fairly narrow range and don't always separate the
correct cycle clearly from others — this is why the app shows a
ranked list with confidence tags instead of a single definitive
answer, and why the notebook includes a sanity-check step comparing
same-cycle photos to calibrate the confidence threshold.

## Running the pipeline

1. Open `notebook/cycle_pipeline.ipynb` in Google Colab.
2. Run cells top to bottom: install deps → upload `registrations.csv`
   → download registration + sighting photos from Drive → parse
   filenames → build embeddings and match → export
   `similarity_matrix.csv` for the app.
3. See `cycle-search-app/README.md` for running the search app
   locally with the exported data.

## What's observed vs. inferred vs. synthetic

- **Observed:** registration photos and metadata (student-submitted),
  sighting photos and their location/time/collector tags (collected
  in the field).
- **Inferred:** CLIP embeddings, similarity scores, and
  `matched_cycle_id` — all model output, not ground truth.
- **Synthetic:** none used; all data in this submission is real,
  field-collected observations.

See `schema.md` for the full column-level breakdown.
