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

        for year in self.years:  
            data = requests.get(self.standings_url)  
            soup = BeautifulSoup(data.text)  
            standings_table = soup.select('table.stats_table')[0]  
            
            
            
            links = [l.get('href') for l in standings_table.find_all('a')]
        
            links = [l for l in links if '/squads/' in l]
            
            team_urls = [F'https://fbref.com{l}' for l in links]

            prevnext_div = soup.find('div', class_='prevnext')
            prev_link = prevnext_div.find('a').get('href')
            standings_url = f"https://fbref.com{prev_link}"

            
            

            for team_url in team_urls:  

                team_name = team_url.split('/')[-1].replace('-Stats', '').replace('-', " ")

                data = requests.get(team_url)
               
                try:
                    matches = pd.read_html(io.StringIO(data.text), match="Scores & Fixtures")[0]
                except ValueError:
                    continue
               
                soup = BeautifulSoup(data.text)
                
                links = [l.get('href') for l in soup.find_all('a')]
                
                links = [l for l in links if l and 'all_comps/shooting/' in l]
                print(links)
                
                data = requests.get(f"https://fbref.com{links[0]}")
                
                try:
                    shooting = pd.read_html(io.StringIO(data.text), match="Shooting")[0]
                 
                    shooting.columns = shooting.columns.droplevel()
                except ValueError:
                    continue

                try:
                    
                    team_data = matches.merge(shooting[["Date", 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']], on="Date")
                except KeyError:  
                    continue  

                team_data = team_data[team_data['Comp'] == self.comp]
                
                team_data['Season'] = year
               
                team_data['Team'] = team_name
                
                self.all_matches.append(team_data)
                
               
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


