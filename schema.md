# Data schema

## registrations.csv (input, from the Google Form)

| Column | Type | Description | Source |
|---|---|---|---|
| Timestamp | datetime | form submission time | observed |
| Name / Roll No. | string | cycle owner's identity | observed |
| Cycle Photos (Upload 3 images) | string | comma-separated Drive file IDs | observed |
| Declared colour / brand / marks | string | owner-reported cycle features | observed |

*(Exact column names come from the Google Form and may vary slightly —
see the actual header row in your export.)*

## data/registrations_index.csv (generated)

| Column | Type | Description | Source |
|---|---|---|---|
| cycle_id | string | assigned ID, e.g. `CYC-001` | inferred (assigned by pipeline, in form-submission order) |
| num_photos_downloaded | int | how many of the declared photos downloaded successfully | inferred |
| ...registration columns | — | carried over from registrations.csv | observed |

## data/sightings_index.csv (generated, before matching)

| Column | Type | Description | Source |
|---|---|---|---|
| sighting_id | string | `{day}_{filename}` | inferred (derived) |
| day | string | collection day folder, e.g. `Day1` | observed (folder structure) |
| image_path | string | local path to the sighting photo | observed |
| location | string | parsed from filename | observed (field-tagged) |
| time | string | `HH:MM`, parsed from filename | observed (field-tagged) |
| collector | string | who took the photo, parsed from filename | observed (field-tagged) |
| seq | int | sequence number at that location/time | observed (field-tagged) |

Filename convention: `LOCATION_HHMM_COLLECTOR_SEQ.jpg` (e.g.
`KAMENG_0230_SV_01.jpg`). Any file that doesn't match this pattern is
skipped and printed by the notebook, not silently dropped.

## data/similarity_matrix.csv (generated, feeds the search app)

| Column | Type | Description | Source |
|---|---|---|---|
| sighting_id, day, location, time, image_path | — | same as sightings_index.csv | observed |
| `<CYC-00N>` (one column per registered cycle) | float, 0-1 | cosine similarity between this sighting's CLIP embedding and that cycle's registered embedding | **inferred** (model output) |

This is a wide table: one row per sighting, one column per registered
cycle. The search app looks up a single cycle's column, sorts by it,
and shows the top 5 sightings as candidate locations.

## data/sightings_matched.csv / .parquet (generated, pipeline-level metric)

| Column | Type | Description | Source |
|---|---|---|---|
| ...sightings_index columns | — | as above | observed |
| matched_cycle_id | string or null | best-matching registered cycle, or null if below `CONF_THRESHOLD` | inferred |
| confidence | float | best similarity score for this sighting | inferred |
| top2_gap | float | gap between best and second-best match | inferred |

`CONF_THRESHOLD` (currently 0.75, set in the notebook) is a tuned
cutoff, calibrated by comparing same-cycle reference-photo similarity
as a baseline — it is not an absolute correctness guarantee.

## Synthetic data

None. Every row in every file above comes from a real Google Form
submission or a real field photograph; no synthetic rows have been
added to extend the dataset.
