# Team Root Bingo Sheet Generator

Browser app for generating bingo sheets for Root the board game. 

Create randomized bingo cards and export them as PDFs for printing. Race either solo or as a team to complete all the items in Root games to claim Bingo victory!

## Usage
Visit the website here: .

In the sidebar
- `Bingo Sheet`: generates the bingo items
    - `Seed`: the given seed determines the generation randomization (make sure all players play on the same seed)
    - `Difficulty`: Normal vs. Elite to accomodate for all skill levels
    - `Filters`: Allows people to pick which subset of bingo items they want to focus on
- `Bingo Wiki`: shows the pool of all possible items

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/team-root-bingo-sheet-generator.git
cd team-root-bingo-sheet-generator
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
├── app.py                 # Main application entry point
├── config/
│   └── settings.py        # Configuration constants
├── src/
│   ├── components/
│   │   ├── filter.py      # Filter component
│   │   └── sidebar.py     # Sidebar navigation
│   ├── pages/
│   │   ├── achievements.py # Achievement wiki page
│   │   ├── bingo.py       # Bingo sheet generator page
│   │   └── home.py        # Home page
│   └── utils/
│       ├── data_ingestor.py # Excel to JSON conversion
│       └── data_loader.py   # Data loading utilities
├── data/
│   ├── achievements.xlsx  # Source achievement data
│   └── achievements.json  # Processed achievement data
├── assets/
│   └── icons/             # Achievement icons
└── requirements.txt
```