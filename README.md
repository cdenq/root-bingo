<img src="assets/tofu.png" width="100">

# Tofu's Root Bingo Generator

Browser app for generating bingo sheets for Root the board game. 

Create randomized bingo cards and export them as PDFs for printing. Race either solo or as a team to complete all the items in Root games to claim Bingo victory!

## Usage
Visit the website here: https://tofu-root-bingo.streamlit.app/.

In the sidebar
- `Bingo Sheet`: generates the bingo items
    - `Seed`: the given seed determines the generation randomization (make sure all players play on the same seed)
    - `Difficulty`: Normal vs. Elite to accomodate for all skill levels
    - `Filters`: Allows people to pick which subset of bingo items they want to focus on
- `Bingo Wiki`: shows the pool of all possible items

## Local Installation
1. Clone the repository:
```bash
git clone https://github.com/cdenq/root-bingo.git
cd root-bingo
```

1. Make a new envs:
```bash
conda create --name root-bingo
conda activate root-bingo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run website locally
```bash
streamlit run app.py
```

## Project Structure

```
team-root-bingo-sheet-generator/
├── app.py                   # Main application entry point
├── config/
│   └── settings.py          # Configuration constants
├── src/
│   ├── components/
│   │   ├── filter.py        # Filter component
│   │   └── sidebar.py       # Sidebar navigation
│   ├── pages/
│   │   ├── achievements.py  # Bingo items directory
│   │   ├── bingo.py         # Bingo sheet generator page
│   │   └── home.py          # Home page
│   └── utils/
│       ├── data_ingestor.py # Excel to JSON conversion
│       └── data_loader.py   # Data loading utilities
├── data/
│   ├── achievements.xlsx    # Source bingo item DB
│   └── achievements.json    # Processed bingo items data
├── assets/
│   ├── icons/               # Bing item icons
│   └── tofu.png             # Tofu  
└── requirements.txt
```
