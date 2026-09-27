import os
import pandas as pd
import streamlit as st

# ---------- config ----------
DATA_PATH = "data/similarity_matrix.csv"
CONF_THRESHOLD = 0.75   # keep this in sync with the notebook's CONF_THRESHOLD
TOP_N = 5

st.set_page_config(page_title="Cycle Search", page_icon="🚲", layout="centered")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    meta_cols = ["sighting_id", "day", "location", "time", "image_path"]
    cycle_cols = [c for c in df.columns if c not in meta_cols]
    return df, cycle_cols


st.title("🚲 Cycle Search")
st.write(
    "Enter your registered cycle ID — we'll check it against campus sightings "
    "using visual similarity and show the top locations where your cycle may have been seen."
)

if not os.path.exists(DATA_PATH):
    st.error(
        f"`{DATA_PATH}` not found. Export similarity_matrix.csv and the sighting "
        f"photos from the notebook into the `data/` folder, then restart the app."
    )
    st.stop()

df, cycle_ids = load_data(DATA_PATH)

search_id = st.text_input("Cycle ID", placeholder="e.g. CYC-005").strip().upper()

if search_id:
    if search_id not in cycle_ids:
        st.error(f"'{search_id}' was not found among registered cycles.")
        st.caption("Registered IDs: " + ", ".join(cycle_ids))
    else:
        ranked = df[["sighting_id", "day", "location", "time", "image_path", search_id]].copy()
        ranked = ranked.rename(columns={search_id: "match_score"})
        ranked = ranked.sort_values("match_score", ascending=False).head(TOP_N)

        best = ranked.iloc[0]
        if best["match_score"] >= CONF_THRESHOLD:
            st.success(
                f"Your cycle is most likely at **{best['location']}** "
                f"(last seen {best['day']} at {best['time']})."
            )
        else:
            st.warning(
                "No sighting matched confidently — check the possible locations below manually."
            )

        st.subheader(f"Top {len(ranked)} suggested locations for {search_id}")

        for _, row in ranked.iterrows():
            confident = row["match_score"] >= CONF_THRESHOLD
            tag = "✅ Confident match" if confident else "🔎 Possible match"

            img_col, info_col = st.columns([1, 2])
            with img_col:
                if isinstance(row["image_path"], str) and os.path.exists(row["image_path"]):
                    st.image(row["image_path"], width=180)
                else:
                    st.caption("(photo not found)")
            with info_col:
                st.markdown(f"**{tag}**")
                st.write(f"📍 Location: **{row['location']}**")
                st.write(f"🕒 Seen: {row['day']} at {row['time']}")
                st.write(f"Similarity score: `{row['match_score']:.4f}`")
            st.divider()

st.caption(
    "Matching is done using CLIP (ViT-B/32) embeddings — scores are not absolute proof, "
    "just a visual similarity estimate. The 'Confident match' tag is given to matches above the threshold."
)
