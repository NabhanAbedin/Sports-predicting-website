import { triviaPageItems, easy } from "./data/triviaPageData.js";

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
    generateQuestions(questions) {
        document.body.classList.remove('selection-body');
        document.body.classList.add('questions-body');
        let tenQuestions = [];
        for (let i = 0; i < 10; i++) {
            const randomIndex = Math.floor(Math.random() * questions.length);
            tenQuestions.push(questions[randomIndex]);

        }
        console.log(tenQuestions);
        let html = '';
        tenQuestions.forEach(question => {
            html += ` <div class="question-container">
            <div class="question">
                ${question.question}
            </div>
            <div class="answers">
                <div class="choice-container">
                    <p class="choice-prefix">A</p>
                    <p class="choice-text">${question.options[0]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">B</p>
                    <p class="choice-text">${question.options[1]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">C</p>
                    <p class="choice-text">${question.options[2]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">D</p>
                    <p class="choice-text">${question.options[3]}</p>
                </div>
            </div>
        </div>`

        })

        this.bodyHTML.innerHTML = html;

    }

}

const triviaPage = new Trivia(triviaPageItems);
triviaPage.constructHTML();


const difficultyElement = document.querySelectorAll('.easy');
difficultyElement.forEach(item => {
    item.addEventListener('click', () => {
        const itemId = item.getAttribute('data-id');
        console.log(itemId);
        if (itemId === '1') {
            triviaPage.generateQuestions(easy);
        }
    })
})

//triviaPage.generateQuestions(easy);
