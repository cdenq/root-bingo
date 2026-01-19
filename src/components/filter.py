# ----------------------------------
# IMPORTS
# ----------------------------------
import streamlit as st
from src.utils.data_loader import load_achievements

# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------
def get_category2_keys(achievements, selected_cat1):
    cat2_keys = set()
    for cat1 in selected_cat1:
        if cat1 in achievements:
            cat2_keys.update(achievements[cat1].keys())
    return sorted(list(cat2_keys))


# ----------------------------------
# FILTER COMPONENTS
# ----------------------------------
def render_category_filters(key_prefix, default_cat1=None, default_cat2=None, locked_selections=None):
    achievements = load_achievements()

    if not achievements:
        return [], []

    category1_keys = list(achievements.keys())

    if default_cat1 is None:
        default_cat1 = category1_keys

    if locked_selections is None:
        locked_selections = {}

    col1, col2 = st.columns(2)

    with col1:
        selected_cat1 = st.multiselect(
            "Category 1",
            options=category1_keys,
            default=default_cat1,
            key=f"{key_prefix}_cat1"
        )

        locked_cat1 = locked_selections.get("cat1", [])
        if locked_cat1:
            for locked in locked_cat1:
                if locked not in selected_cat1:
                    selected_cat1.append(locked)

    available_cat2 = get_category2_keys(achievements, selected_cat1)

    if default_cat2 is None:
        default_cat2 = available_cat2

    valid_default_cat2 = [c for c in default_cat2 if c in available_cat2]

    with col2:
        selected_cat2 = st.multiselect(
            "Category 2",
            options=available_cat2,
            default=valid_default_cat2,
            key=f"{key_prefix}_cat2"
        )

        locked_cat2 = locked_selections.get("cat2", [])
        if locked_cat2:
            for locked in locked_cat2:
                if locked in available_cat2 and locked not in selected_cat2:
                    selected_cat2.append(locked)

    return selected_cat1, selected_cat2
