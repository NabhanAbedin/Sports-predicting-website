class SoccerPrediction {
    constructor() {
        this.htmlContainer = document.querySelector('.leagues-container')
    }

    leagueSelect() {
        const leagueSelect = document.querySelectorAll('.league-button');
        leagueSelect.forEach(league => {
            league.addEventListener('click', () => {
                const leagueName = league.getAttribute('data-country');
                //console.log(leagueName)
                if (leagueName === 'England') {
                    this.predictionHTML('backend/PremierLeague.csv')
                }

            })
        })
    }
    predictionHTML(leaguecsv) {
        const data = { league: leaguecsv }
        fetch('http://127.0.0.1:80/preprocess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        })
            .then(response => response.json())
            .then(data => {
                console.log('Response from server:', data);
                this.htmlContainer.innerHTML = data['wins'];
            })
            .catch(error => console.error('Error:', error));





    }
}



SoccerPage = new SoccerPrediction();

SoccerPage.leagueSelect()