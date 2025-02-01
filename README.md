# Premier Draft League API Access

This repository contains Python scripts to interact with the Fantasy Premier League (FPL) Draft API. It allows users to retrieve player information, league standings, and transaction data within leagues.

## Project Overview

The **Premier Draft League API Access** project simplifies access to FPL Draft data. Developers and fantasy sports enthusiasts can use these scripts to fetch data such as:
- Player details and statistics
- League standings
- Transaction and draft history within leagues

This tool allows you to interact with the Fantasy Premier League Draft API, enabling a streamlined way to analyze and manage your Fantasy Premier League (FPL) teams.

## Features

- Fetch and process real-time Fantasy Premier League Draft data.
- Retrieve detailed player stats, team details, and league standings.
- Access player transaction history and draft history.
- Customizable Python scripts for integration into your own applications.
- Simple-to-use interface for retrieving data and analyzing FPL Draft performance.

## Requirements

To use these scripts, you'll need the following dependencies:

- Python 3.7 or higher
- [Requests](https://pypi.org/project/requests/): For making HTTP requests.
  - Install with: `pip install requests`
- [Pandas](https://pypi.org/project/pandas/): For data manipulation and analysis.
  - Install with: `pip install pandas`

## Architecture

The project is structured to provide easy access to FPL Draft data via API endpoints. Here is an overview of the pipeline used:

![fpl](https://github.com/user-attachments/assets/c9717c3e-3601-4bfe-ad70-f993f75af8d2)

## Setup Instructions

Follow these steps to get started with the project:

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/ldnm99/draft_fpl.git
   cd draft_fpl
   ```
   
2. **Install Dependencies**

   Install the required dependencies (Requests and Pandas) by running the following commands:

   ```bash
   pip install -r requirements.txt
   ```
   
Alternatively, you can manually install them with:
   ```bash
   pip install requests pandas
   ```

3. **Configure League ID**

To access specific data for your league, modify the LEAGUE_ID in league.py. Replace the placeholder value with your actual league ID.

4. **Run the Scripts**

After setting up, you can start interacting with the API. Run the scripts as needed to fetch player, team, or league data. For example:
   ```bash
   python src/script.py
   ```

**Usage**
Once everything is set up, you can use the following functionalities:
- Fetching Player Data: Retrieve stats and details for individual players in the draft.
- Getting League Standings: Access the standings of teams within the league.
- Viewing Transaction History: Track team changes and draft history within a league
