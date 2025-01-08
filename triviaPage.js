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
        const questionsCopy = [...questions]; // Create a copy to preserve the original array
        //console.log(questionsCopy)
        this.tenQuestions = [];

        for (let i = 0; i < 10; i++) {
            const randomIndex = Math.floor(Math.random() * questionsCopy.length);
            const value = questionsCopy.splice(randomIndex, 1)[0]; // Remove the element at randomIndex and return it
            this.tenQuestions.push(value);
        }
        console.log(this.tenQuestions);
        let html = '';
        this.tenQuestions.forEach(question => {
            html += ` <div class="question-container" data-question-number="${question.number}">
            <div class="question">
                ${question.question}
            </div>
            <div class="answers">
                <div class="choice-container">
                    <p class="choice-prefix">A</p>
                    <p class="choice-text" data-number="1">${question.options[0]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">B</p>
                    <p class="choice-text" data-number="2">${question.options[1]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">C</p>
                    <p class="choice-text" data-number="3">${question.options[2]}</p>
                </div>
                <div class="choice-container">
                    <p class="choice-prefix">D</p>
                    <p class="choice-text" data-number="4">${question.options[3]}</p>
                </div>
            </div>
        </div>
        `

        })
        html += `<div class="button-container">
        <button class="finished-button js-finished-button">Done!</button>
        </div>`;

        this.bodyHTML.innerHTML = html;

        this.checkAnswer();


    }
    checkAnswer() {
        const questionElement = document.querySelectorAll('.question-container');
        let questionAnswers = {};

        questionElement.forEach(question => {
            const choices = question.querySelectorAll('.choice-container');
            //console.log(question.dataset);



            choices.forEach(choice => {
                choice.addEventListener('click', () => {

                    const questionNumber = question.dataset.questionNumber;
                    //console.log(`Question Number: ${questionNumber}`);


                    const currentQuestion = this.matchingQuestion(questionNumber);
                    //console.log(currentQuestion);

                    choices.forEach(otherChoice => {
                        otherChoice.classList.remove('clicked');
                    });
                    choice.classList.toggle('clicked');

                    let answerChoice = '';
                    const number = choice.querySelector('.choice-text').dataset['number'];
                    answerChoice = number;
                    console.log(answerChoice)

                    if (Number(answerChoice) === Number(currentQuestion.answerNumber)) {
                        questionAnswers[questionNumber] = 'correct';
                    } else {
                        questionAnswers[questionNumber] = 'wrong';
                    }


                })

            })

        })
        document.body.addEventListener('click', (event) => {
            if (event.target.classList.contains('js-finished-button')) {
                const length = Object.keys(questionAnswers).length;
                if (length < 10) {
                    alert("You have not answered all questions!")
                } else {
                    console.log(questionAnswers);
                    this.generateScoreHTML(questionAnswers);
                }
            }
        });

    }

    matchingQuestion(questionNumber) {

        let matchingQuestion = null;

        this.tenQuestions.forEach(question => {
            if (question.number === Number(questionNumber)) {
                matchingQuestion = question;
            }
        });

        return matchingQuestion;
    }
    generateScoreHTML(questionAnswers) {
        let score = 0;
        Object.keys(questionAnswers).forEach(key => {
            if (questionAnswers[key] === 'correct') {
                score++;
            }
        })
        console.log(score);
        let html = '';

    }





}

const triviaPage = new Trivia(triviaPageItems);
triviaPage.constructHTML();


const difficultyElement = document.querySelectorAll('.easy');
difficultyElement.forEach(item => {
    item.addEventListener('click', () => {
        const itemId = item.getAttribute('data-id');
        //console.log(itemId);
        if (itemId === '1') {
            triviaPage.generateQuestions(easy);
        }
    })
})

document.body.addEventListener('click', (event) => {
    if (event.target.classList.contains('js-finished-button')) {
        console.log('clicked');
    }
});

//triviaPage.checkAnswer();
