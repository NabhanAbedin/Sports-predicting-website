import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time 
import random
import io

class scraping:
    def __init__(self,standings_url,comp,csv,years):
        self.standings_url = standings_url
        self.comp = comp
        self.csv = csv        
        self.all_matches = []
        self.years = years
    def scrape(self):

        for year in self.years:  # Loop through each year in the 'years' list
            data = requests.get(self.standings_url)  # Make an HTTP request to get the standings page for the given URL
            soup = BeautifulSoup(data.text)  # Parse the HTML content of the page using BeautifulSoup
            standings_table = soup.select('table.stats_table')[0]  # Select the first table with the class 'stats_table'
            
            
            # Extract all links from the standings table
            links = [l.get('href') for l in standings_table.find_all('a')]
            # Filter the links to keep only those related to squads
            links = [l for l in links if '/squads/' in l]
            # Construct full URLs for each team by appending the filtered links to the base URL
            team_urls = [F'https://fbref.com{l}' for l in links]

            prevnext_div = soup.find('div', class_='prevnext')
            prev_link = prevnext_div.find('a').get('href')
            standings_url = f"https://fbref.com{prev_link}"

            
            

            for team_url in team_urls:  # Loop through each team's URL
                # Extract the team name from the URL and format it (remove '-Stats' and replace hyphens with spaces)
                team_name = team_url.split('/')[-1].replace('-Stats', '').replace('-', " ")

                # Make an HTTP request to get the specific team's page
                data = requests.get(team_url)
                # Read the 'Scores & Fixtures' table from the team's page
                try:
                    matches = pd.read_html(io.StringIO(data.text), match="Scores & Fixtures")[0]
                except ValueError:
                    continue
                # Parse the HTML content of the team's page
                soup = BeautifulSoup(data.text)
                # Extract all links from the standings table again
                links = [l.get('href') for l in soup.find_all('a')]
                # Filter the links to find those related to the shooting stats
                links = [l for l in links if l and 'all_comps/shooting/' in l]
                print(links)
                # Make an HTTP request to get the shooting stats page
                data = requests.get(f"https://fbref.com{links[0]}")
                # Read the 'Shooting' table from the stats page
                try:
                    shooting = pd.read_html(io.StringIO(data.text), match="Shooting")[0]
                # Drop the top-level header for the table (multi-level column headers) 
                    shooting.columns = shooting.columns.droplevel()
                except ValueError:
                    continue

                try:
                    # Merge the matches and shooting data on the 'Date' column
                    team_data = matches.merge(shooting[["Date", 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']], on="Date")
                except KeyError:  # Handle cases where merging fails due to missing or mismatched data
                    continue  # Skip to the next iteration

                # Filter data to include only matches from the Premier League
                team_data = team_data[team_data['Comp'] == self.comp]
                # Add the current year as a new column to the team's data
                team_data['Season'] = year
                # Add the team name as a new column to the team's data
                team_data['Team'] = team_name
                # Append the processed team data to the 'all_matches' list
                self.all_matches.append(team_data)
                
                # Pause for 1 second to avoid overloading the server with requests
                random_delay = random.uniform(5, 9)
                time.sleep(random_delay)

                return self.all_matches
    def export_to_csv(self,all_matches):
        match_df = pd.concat(all_matches)
        match_df.to_csv(self.csv)


premier_league = scraping('https://fbref.com/en/comps/9/Premier-League-Stats','Premier League','PremierLeague.csv',list(range(2025,2020),-1) )
prem_matches = premier_league.scrape()
premier_league.export_to_csv(prem_matches)

la_liga = scraping('https://fbref.com/en/comps/12/La-Liga-Stats','la Liga','LaLiga.csv',list(range(2025,2021),-1) )
laLiga_matches = la_liga.scrape()
la_liga.export_to_csv(laLiga_matches)

Serie_A = scraping('https://fbref.com/en/comps/11/Serie-A-Stats','Serie A','SerieA.csv',list(range(2025,2021),-1) )
SerieA_matches = Serie_A.scrape()
Serie_A.export_to_csv(SerieA_matches)


