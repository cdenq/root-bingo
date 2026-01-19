# ----------------------------------
# IMPORTS
# ----------------------------------
import streamlit as st
from src.utils.data_loader import load_achievements
from src.components.filter import render_category_filters

# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------
def format_achievement_text(achievement):
    name = achievement.get("name") or "Unnamed"
    window = achievement.get("window") or ""
    base = achievement.get("base") or ""
    normal = achievement.get("normal")
    elite = achievement.get("elite")

    if normal and elite:
        base_text = base.replace("{x}", f"[{normal} | {elite}]")
    elif normal:
        base_text = base.replace("{x}", str(normal))
    elif elite:
        base_text = base.replace("{x}", str(elite))
    else:
        base_text = base.replace("{x}", "")

    display_text = f"**{name}** - {window}: {base_text}"
    notes = achievement.get("notes")

    return display_text, notes


def display_achievements_list(achievements_dict):
    for _achievement_id, achievement in achievements_dict.items():
        if not isinstance(achievement, dict):
            continue
        display_text, notes = format_achievement_text(achievement)

        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"- {display_text}")
        with col2:
            if notes:
                st.markdown("ℹ️", help=notes)


# ----------------------------------
# RENDER MAIN
# ----------------------------------
def render():
    st.title("Achievements List")
    st.markdown("---")

    achievements = load_achievements()

    if not achievements:
        st.warning("No achievements loaded")
        return

    selected_cat1, selected_cat2 = render_category_filters("achievements")

    st.markdown("---")

    for cat1 in selected_cat1:
        if cat1 not in achievements:
            continue

        with st.expander(f"{cat1}", expanded=True):
            cat1_data = achievements[cat1]

            for cat2_key, cat2_value in cat1_data.items():
                if cat2_key not in selected_cat2:
                    continue

                if not isinstance(cat2_value, dict):
                    continue

                with st.expander(f"{cat2_key}", expanded=False):
                    achievements_in_cat2 = {k: v for k, v in cat2_value.items() if isinstance(v, dict)}

                    for mode in ["Normal", "Elite", "Both"]:
                        mode_achievements = {k: v for k, v in achievements_in_cat2.items() if v.get("mode") == mode}
                        if mode_achievements:
                            with st.expander(f"{mode}", expanded=False):
                                display_achievements_list(mode_achievements)
