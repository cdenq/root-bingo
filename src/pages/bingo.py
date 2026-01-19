# ----------------------------------
# IMPORTS
# ----------------------------------
import io
import random
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from src.utils.data_loader import load_achievements
from config.settings import DEFAULT_SEED, ICONS_DIR

# ----------------------------------
# CONSTANTS
# ----------------------------------
GENERAL_CATEGORIES = ["Gameplay", "Map", "Landmarks", "Bingo"]

# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------
def get_faction_category2_keys(achievements):
    faction_data = achievements.get("Faction", {})
    return sorted(list(faction_data.keys()))


def get_bingo_achievement_id(achievements, difficulty):
    bingo_data = achievements.get("General", {}).get("Bingo", {})
    mode_to_find = "Normal" if difficulty == "n" else "Elite"

    for achievement_id, achievement in bingo_data.items():
        if achievement.get("mode") == mode_to_find:
            return achievement_id

    return None


def get_achievements_pool(achievements, selected_cat1, selected_faction_cat2, difficulty):
    pool = []
    valid_modes = ["Both", "Normal"] if difficulty == "n" else ["Both", "Elite"]

    for cat1 in selected_cat1:
        if cat1 not in achievements:
            continue

        cat1_data = achievements[cat1]

        if cat1 == "General":
            categories_to_use = [c for c in GENERAL_CATEGORIES if c != "Bingo"]
        else:
            categories_to_use = selected_faction_cat2

        for cat2 in categories_to_use:
            if cat2 not in cat1_data:
                continue

            cat2_data = cat1_data[cat2]

            for achievement_id, achievement in cat2_data.items():
                if not isinstance(achievement, dict):
                    continue

                if achievement.get("mode") in valid_modes:
                    pool.append({
                        "id": achievement_id,
                        "cat1": cat1,
                        "cat2": cat2,
                        "data": achievement
                    })

    return pool


def get_bucket_key(cat1, cat2):
    if cat1 == "General":
        return "General"
    else:
        return f"Faction-{cat2}"


def group_pool_by_bucket(pool):
    buckets = {}

    for item in pool:
        key = get_bucket_key(item["cat1"], item["cat2"])
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(item)

    return buckets


def sample_from_buckets(buckets, total_needed, rng):
    if not buckets:
        return []

    num_buckets = len(buckets)
    base_per_bucket = total_needed // num_buckets
    remainder = total_needed % num_buckets

    sampled = []
    sampled_ids = set()

    bucket_names = list(buckets.keys())
    rng.shuffle(bucket_names)

    remaining_buckets = {}

    for i, bucket_name in enumerate(bucket_names):
        bucket = buckets[bucket_name].copy()
        rng.shuffle(bucket)

        count = base_per_bucket + (1 if i < remainder else 0)
        count = min(count, len(bucket))

        for item in bucket[:count]:
            sampled.append(item)
            sampled_ids.add(item["id"])

        leftover = [item for item in bucket[count:] if item["id"] not in sampled_ids]
        if leftover:
            remaining_buckets[bucket_name] = leftover

    while len(sampled) < total_needed and remaining_buckets:
        available_bucket_names = list(remaining_buckets.keys())
        chosen_bucket_name = rng.choice(available_bucket_names)
        chosen_bucket = remaining_buckets[chosen_bucket_name]

        if chosen_bucket:
            item = chosen_bucket.pop(0)
            sampled.append(item)
            sampled_ids.add(item["id"])

        if not chosen_bucket:
            del remaining_buckets[chosen_bucket_name]

    return sampled


def sampler(achievements, seed, difficulty, selected_cat1, selected_faction_cat2):
    if seed == "" or seed is None:
        seed = DEFAULT_SEED

    try:
        seed_int = int(seed)
    except ValueError:
        seed_int = hash(seed) % (2**32)

    rng = random.Random(seed_int)

    difficulty_code = "n" if difficulty == "Normal" else "e"

    bingo_id = get_bingo_achievement_id(achievements, difficulty_code)
    if bingo_id is None:
        return None

    pool = get_achievements_pool(achievements, selected_cat1, selected_faction_cat2, difficulty_code)

    buckets = group_pool_by_bucket(pool)

    sampled_items = sample_from_buckets(buckets, 24, rng)

    rng.shuffle(sampled_items)

    result = [difficulty_code, bingo_id]
    for item in sampled_items:
        result.append(item["id"])

    return result


def get_achievement_by_id(achievements, achievement_id):
    for _cat1, cat1_data in achievements.items():
        for _cat2, cat2_data in cat1_data.items():
            if achievement_id in cat2_data:
                return cat2_data[achievement_id]
    return None


def get_icon_path(icon_name):
    if not icon_name:
        return None

    icon_file = ICONS_DIR / f"{icon_name}.png"
    if icon_file.exists():
        return str(icon_file)

    return None


def format_cell_content(achievement, difficulty_code):
    name = achievement.get("name") or "Unnamed"
    window = achievement.get("window") or ""
    base = achievement.get("base") or ""
    normal = achievement.get("normal")
    elite = achievement.get("elite")
    icon = achievement.get("icon")

    if difficulty_code == "n" and normal:
        base_text = base.replace("{x}", str(normal))
    elif difficulty_code == "e" and elite:
        base_text = base.replace("{x}", str(elite))
    elif normal and elite:
        value = normal if difficulty_code == "n" else elite
        base_text = base.replace("{x}", str(value))
    else:
        base_text = base.replace("{x}", "")

    icon_path = get_icon_path(icon)
    content = f"[{window}] {base_text}"

    return icon_path, name, content


def grid_placer(achievements, sampled_list):
    if sampled_list is None or len(sampled_list) < 26:
        return None

    difficulty_code = sampled_list[0]
    bingo_id = sampled_list[1]
    other_ids = sampled_list[2:]

    grid = [[None for _ in range(5)] for _ in range(5)]

    bingo_achievement = get_achievement_by_id(achievements, bingo_id)
    if bingo_achievement:
        icon_text, name, content = format_cell_content(bingo_achievement, difficulty_code)
        grid[2][2] = {
            "icon": icon_text,
            "name": name,
            "content": content
        }

    idx = 0
    for row in range(5):
        for col in range(5):
            if row == 2 and col == 2:
                continue

            if idx < len(other_ids):
                achievement_id = other_ids[idx]
                achievement = get_achievement_by_id(achievements, achievement_id)

                if achievement:
                    icon_text, name, content = format_cell_content(achievement, difficulty_code)
                    grid[row][col] = {
                        "icon": icon_text,
                        "name": name,
                        "content": content
                    }

                idx += 1

    return grid


def render_bingo_grid(grid):
    if grid is None:
        st.warning("Could not generate bingo grid")
        return

    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            cell = grid[row][col]
            with cols[col]:
                if cell:
                    icon_path = cell["icon"]
                    if icon_path:
                        st.image(icon_path, width=50)
                    else:
                        st.markdown("*(no icon)*")
                    st.markdown(f"**{cell['name']}**")
                    st.markdown(f"{cell['content']}")
                else:
                    st.markdown("---")
                st.markdown("---")


def generate_pdf(grid, seed_value, difficulty_text):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=0.25*inch,
        rightMargin=0.25*inch,
        topMargin=0.25*inch,
        bottomMargin=0.25*inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        alignment=1,
        spaceAfter=5
    )

    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Normal"],
        fontSize=8,
        alignment=1,
        fontName="Helvetica-Bold",
        leading=10
    )

    content_style = ParagraphStyle(
        "ContentStyle",
        parent=styles["Normal"],
        fontSize=6,
        alignment=1,
        leading=8
    )

    elements = []

    title = Paragraph(f"Seed: {seed_value} | {difficulty_text}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))

    table_data = []
    cell_width = 2.0 * inch
    cell_height = 1.4 * inch

    for row in range(5):
        row_data = []
        for col in range(5):
            cell = grid[row][col]
            if cell:
                cell_elements = []

                icon_path = cell["icon"]
                if icon_path:
                    try:
                        img = Image(icon_path, width=0.4*inch, height=0.4*inch)
                        cell_elements.append(img)
                    except Exception:
                        pass

                name_para = Paragraph(cell["name"], name_style)
                cell_elements.append(name_para)

                content_para = Paragraph(cell["content"], content_style)
                cell_elements.append(content_para)

                row_data.append(cell_elements)
            else:
                row_data.append("")
        table_data.append(row_data)

    table = Table(
        table_data,
        colWidths=[cell_width] * 5,
        rowHeights=[cell_height] * 5
    )

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (2, 2), (2, 2), colors.lightyellow),
    ]))

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)
    return buffer


# ----------------------------------
# RENDER MAIN
# ----------------------------------
def render():
    st.title("Bingo Sheet")
    st.markdown("---")

    achievements = load_achievements()

    if not achievements:
        st.warning("No achievements loaded")
        return

    category1_keys = list(achievements.keys())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        seed_value = st.text_input(
            "Seed Value",
            value=str(DEFAULT_SEED),
            placeholder="Enter a seed"
        )

    with col2:
        difficulty = st.toggle("Elite Mode", value=False)
        difficulty_text = "Elite" if difficulty else "Normal"
        st.caption(f"Difficulty: {difficulty_text}")

    default_cat1 = ["General"]
    if "Faction" in category1_keys:
        default_cat1.append("Faction")

    with col3:
        selected_cat1 = st.multiselect(
            "Category 1",
            options=category1_keys,
            default=default_cat1,
            key="bingo_cat1"
        )

        if "General" not in selected_cat1:
            selected_cat1.append("General")
            st.warning("General is required")

    faction_cat2_options = get_faction_category2_keys(achievements) if "Faction" in selected_cat1 else []

    with col4:
        selected_faction_cat2 = st.multiselect(
            "Factions",
            options=faction_cat2_options,
            default=faction_cat2_options,
            key="bingo_cat2"
        )

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("Generate Bingo Sheet", use_container_width=True):
            sampled = sampler(achievements, seed_value, difficulty_text, selected_cat1, selected_faction_cat2)

            if sampled and len(sampled) >= 26:
                grid = grid_placer(achievements, sampled)
                st.session_state["bingo_grid"] = grid
                st.session_state["bingo_seed_for_pdf"] = seed_value
                st.session_state["bingo_difficulty_for_pdf"] = difficulty_text
            else:
                count = len(sampled) - 1 if sampled else 0
                st.error(f"Not enough achievements to generate a bingo sheet. Got {count} achievements, need 25.")

    with btn_col2:
        if "bingo_grid" in st.session_state and st.session_state["bingo_grid"] is not None:
            grid = st.session_state["bingo_grid"]
            seed_for_pdf = st.session_state.get("bingo_seed_for_pdf", seed_value)
            difficulty_for_pdf = st.session_state.get("bingo_difficulty_for_pdf", difficulty_text)

            pdf_buffer = generate_pdf(grid, seed_for_pdf, difficulty_for_pdf)

            st.markdown(
                """
                <style>
                div[data-testid="stDownloadButton"] > button {
                    background-color: #ff4b4b;
                    color: white;
                    width: 100%;
                }
                div[data-testid="stDownloadButton"] > button:hover {
                    background-color: #ff6b6b;
                    color: white;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="Save as PDF",
                data=pdf_buffer,
                file_name=f"bingo_sheet_{seed_for_pdf}_{difficulty_for_pdf}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.markdown("---")

    if "bingo_grid" in st.session_state and st.session_state["bingo_grid"] is not None:
        render_bingo_grid(st.session_state["bingo_grid"])
