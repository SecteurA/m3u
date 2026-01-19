
import streamlit as st
from io import StringIO
from m3u_parser import parse_m3u, generate_m3u


st.set_page_config(page_title="M3U Category Editor", layout="wide")

# --- Custom Header ---
st.markdown("""
<div style="text-align:center; margin-bottom: 2rem;">
    <h1 style="color:#1a73e8; margin-bottom:0.2em;">Level Up Your IPTV Experience</h1>
    <h3 style="color:#444; font-weight:400; margin-top:0;">with Customized M3U Playlists</h3>
    <p style="font-size:1.2em; color:#666; max-width:600px; margin:auto;">
        Upload, filter, and export your personalized IPTV M3U playlists — no more clutter, just the channels you want!
    </p>
</div>
""", unsafe_allow_html=True)



# --- File/URL Input Section ---
with st.expander("1️⃣  Load Your M3U Playlist", expanded=True):
    col1, col2 = st.columns([2,1])
    with col1:
        m3u_url = st.text_input("Paste M3U URL (optional):", value="", help="Paste a direct link to an M3U file.")
    with col2:
        uploaded_file = st.file_uploader("Or upload M3U file", type=["m3u", "txt"])



import requests


m3u_content = None
if m3u_url:
    try:
        with st.spinner("Fetching M3U from URL..."):
            resp = requests.get(m3u_url, timeout=10)
            resp.raise_for_status()
            m3u_content = resp.text
        st.success("M3U file loaded from URL.")
    except Exception as e:
        st.error(f"Failed to fetch M3U: {e}")
elif uploaded_file:
    m3u_content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.success("M3U file loaded from upload.")

if m3u_content:
    with st.expander("2️⃣  Filter & Customize", expanded=True):
        categories = parse_m3u(m3u_content)
        st.success(f"Found {len(categories)} categories.")
        all_categories = list(categories.keys())
        with st.expander("Show all categories"):
            st.write(all_categories)

        st.markdown("**Select categories to keep:**")
        selected_categories = st.multiselect(
            "Choose categories to include in the download:",
            options=all_categories,
            default=all_categories[:min(10, len(all_categories))],
            help="Only selected categories will be included in the new M3U file."
        )

        st.write(f"Selected {len(selected_categories)} categories.")

        st.markdown("**Mass Rename Categories**")
        prefix = st.text_input("Add prefix to selected categories (optional):", value="")

        # Prepare renamed categories mapping
        renamed_categories = {cat: f"{prefix}{cat}" if prefix else cat for cat in selected_categories}
        st.caption("Preview renamed categories:")
        st.write(list(renamed_categories.values()))

        if selected_categories:
            st.markdown("---")
            st.markdown(
                "<div style='text-align:center; margin:1.5em 0;'>"
                "<span style='font-size:1.1em; color:#1a73e8; font-weight:600;'>Ready to export your custom playlist?</span>"
                "</div>", unsafe_allow_html=True)
            if st.button("⬇️ Download filtered M3U", use_container_width=True):
                # Create a new categories dict with renamed keys
                renamed_dict = {renamed_categories[cat]: categories[cat] for cat in selected_categories}
                # Generate M3U with renamed categories
                from m3u_parser import generate_m3u_with_custom_names
                filtered_m3u = generate_m3u_with_custom_names(renamed_dict)
                st.download_button(
                    label="Download M3U",
                    data=filtered_m3u,
                    file_name="filtered_playlist.m3u",
                    mime="audio/x-mpegurl",
                    use_container_width=True
                )
else:
    st.info("Please upload an M3U file or enter a URL to begin.")
