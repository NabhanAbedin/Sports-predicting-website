class SoccerPrediction {
    constructor() {
        this.htmlContainer = document.querySelector('.leagues-container')
    }

    leagueSelect() {
        const leagueSelect = document.querySelectorAll('.league-button');
        leagueSelect.forEach(league => {
            league.addEventListener('click', () => {
                const leagueName = league.getAttribute('data-country');
                if (leagueName === 'England') {
                    this.predictionHTML('PremierLeague.csv', 'Premier League')
                } else if (leagueName == 'Spain') {
                    this.predictionHTML('laLiga.csv', 'La Liga')
                } else if (leagueName == 'Italy')
                    this.predictionHTML('SerieA.csv', 'Serie A')

            })
        })
    }
    predictionHTML(leaguecsv, league) {
        this.htmlContainer.innerHTML = `
        <div class="table-container">
        <h1 class="text-center">${league} Predictions!</h1>
        <h2 class="text-center">  From the 2023-24 season to the middle of 2024-25 season</h2>
        <div class="df-table">

        </div>
        <a href="soccerPrediction.html"><button class="return-button">Return</button></a>
    </div>
        
        `
        const data = { league: leaguecsv }
        fetch('https://sports-predicting-website.onrender.com/preprocess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        })
            .then(response => response.json())
            .then(data => {
                const tableElement = document.querySelector('.df-table')
                tableElement.innerHTML = data['wins'];
                console.log(data['precision'])
            })
            .catch(error => console.error('Error:', error));








    }
}



SoccerPage = new SoccerPrediction();

SoccerPage.leagueSelect()