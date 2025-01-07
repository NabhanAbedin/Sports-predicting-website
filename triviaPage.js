import { triviaPageItems } from "./data/triviaPageData.js";

class Trivia {
    constructor(triviaPageItems, qustions) {
        this.triviaPageItems = triviaPageItems;
        this.questions = this.questions;
        this.triviaHTML = document.querySelector('.js-container');
        this.bodyHTML = document.querySelector('.js-questions-container');
    }
    constructHTML() {
        let html = '';
        this.triviaPageItems.forEach(item => {
            html += `<div data-id="${item.id}" class="easy">
            <div class="section-1">
                <img src="${item.image}" alt="">

            </div>
            <div class="section-2">
                <h1>${item.header}</h1>
                <p>${item.text}</p>
            </div>


        </div>
    `;

            this.triviaHTML.innerHTML = html
        });

    }
    generateQuestions() {

        this.bodyHTML.innerHTML = html;

    }

}

const triviaPage = new Trivia(triviaPageItems);
//triviaPage.constructHTML();


const difficultyElement = document.querySelectorAll('.easy');
difficultyElement.forEach(item => {
    item.addEventListener('click', () => {
        const itemId = item.getAttribute('data-id');
        console.log(itemId);
        triviaPage.generateQuestions();
    })
})

