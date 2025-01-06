import { homepageItems } from "./data/homepageData.js"

class homePage {
    constructor(homePage) {
        this.homePage = homePage;
    }

    createPanels() {
        let html = '';
        this.homePage.forEach(item => {
            html += `
            <div class="cards-container">
            <a href="${item.link}" class="card-link">
                <div class="selection" data-aos="fade-in" data-aos-duration="1000">
                    <img src="${item.image}" alt="">
                    <div class="selection-text">
                        <h1>${item.header}</h1>
                        ${item.text}
                    </div>
                </div>
                </a>
            </div>
    `;

        });

        document.querySelector('.js-item-choice').innerHTML = html;
        return html;



    }


}

const home = new homePage(homepageItems);
home.createPanels();