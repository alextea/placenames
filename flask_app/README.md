# 📍 A Place in England

This is a web app that generates random, plausible-sounding English place names using a corpus of 38,600+ real place names from the [ONS Index of Place Names](https://geoportal.statistics.gov.uk/datasets/208d9884575647c29f0dd5a1184e711a/about). The app uses a combination of linguistic rules and randomisation to create new names, and can optionally generate "rude" place names for fun.

## Features
- Generates random English place names based on real data
- Optionally generates "rude" place names

## Generating the placenames

There are 3 scripts used to extract and generate the placenames:

- `filter_placename_data.py`: Filters the raw ONS data to get placenames that match locations in England
- `extract_parts.py`: Splits the placenames into tokens (prefixes, roots, suffixes, etc.) used to reconstruct new names
- `generate_placename.py`: Contains methods to generate placenames based on different rules

## Running the web app

1. **Install dependencies**
   ```sh
   cd flask_app
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   - Create a `.env` file in the project root or set the `UNSPLASH_ACCESS_KEY` in your shell:
     ```sh
     echo "UNSPLASH_ACCESS_KEY=your_unsplash_api_key" > .env
     ```

3. **Run the Flask app from the project root**
   ```sh
   cd ..  # if you're in flask_app
   python -m flask_app.app
   # or
   export FLASK_APP=flask_app/app.py
   flask run
   ```

4. **Open your browser** and go to [http://localhost:5000](http://localhost:5000)

## Project structure
- `placenames/` — logic for extracting and generating placename parts
- `flask_app/` — Flask web app and templates
- `data/` — data files and extracted parts

---

Site by [Alex Torrance](https://bsky.app/profile/alextorrance.co.uk)