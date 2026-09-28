const taskSelect = document.getElementById("task");

const levelContainer =
    document.getElementById("level-container");

const hoursContainer =
    document.getElementById("hours-container");

const quizCountContainer =
    document.getElementById("quiz-count-container");

const levelSelect =
    document.getElementById("level");

const hoursInput =
    document.getElementById("hours");

const quizCountInput =
    document.getElementById("quiz-count");

const inputText =
    document.getElementById("input-text");

const submitButton =
    document.getElementById("submit-btn");

const buttonText =
    document.getElementById("button-text");

const spinner =
    document.getElementById("spinner");

const resultCard =
    document.getElementById("result-card");

const resultContent =
    document.getElementById("result-content");

const copyButton =
    document.getElementById("copy-btn");


let latestResultText = "";


/* -----------------------------------------------------------
   UI
----------------------------------------------------------- */

function updateForm() {

    const task = taskSelect.value;

    levelContainer.classList.add("hidden");
    hoursContainer.classList.add("hidden");
    quizCountContainer.classList.add("hidden");


    if (task === "explain") {
        levelContainer.classList.remove("hidden");
    }


    if (task === "quiz") {
        quizCountContainer.classList.remove("hidden");
    }


    if (task === "learn") {
        levelContainer.classList.remove("hidden");
        hoursContainer.classList.remove("hidden");
    }


    const labels = {
        qa: "Ask a Question",
        explain: "Explain Concept",
        quiz: "Generate Quiz",
        summarize: "Summarize Text",
        learn: "Create Learning Path"
    };


    buttonText.textContent =
        labels[task] || "Generate Answer";
}


taskSelect.addEventListener(
    "change",
    updateForm
);


updateForm();


/* -----------------------------------------------------------
   API
----------------------------------------------------------- */

async function callAPI(
    endpoint,
    payload
) {

    const response = await fetch(
        endpoint,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)
        }
    );


    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            "The server returned an invalid response."
        );
    }


    if (!response.ok) {

        const message =
            data.detail ||
            "Something went wrong.";

        throw new Error(message);
    }


    return data;
}


/* -----------------------------------------------------------
   Loading state
----------------------------------------------------------- */

function setLoading(isLoading) {

    submitButton.disabled = isLoading;

    spinner.classList.toggle(
        "hidden",
        !isLoading
    );


    if (isLoading) {
        buttonText.textContent =
            "EduGenie is thinking...";
    } else {
        updateForm();
    }
}


/* -----------------------------------------------------------
   Result
----------------------------------------------------------- */

function showResult(text) {

    latestResultText = text;

    resultCard.classList.remove("hidden");

    resultContent.innerHTML = "";

    const element =
        document.createElement("div");

    element.className = "result-text";

    element.textContent = text;

    resultContent.appendChild(element);

    resultCard.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function showError(message) {

    latestResultText = "";

    resultCard.classList.remove("hidden");

    resultContent.innerHTML = "";

    const error =
        document.createElement("div");

    error.className = "error-message";

    error.textContent = message;

    resultContent.appendChild(error);
}


/* -----------------------------------------------------------
   Quiz rendering
----------------------------------------------------------- */

function renderQuiz(questions) {

    resultCard.classList.remove("hidden");

    resultContent.innerHTML = "";

    latestResultText = "";


    questions.forEach(
        (question, questionIndex) => {

            const questionContainer =
                document.createElement("div");

            questionContainer.className =
                "quiz-question";


            const title =
                document.createElement("h3");

            title.textContent =
                `${questionIndex + 1}. ${question.question}`;


            questionContainer.appendChild(title);


            const explanation =
                document.createElement("div");

            explanation.className =
                "quiz-explanation hidden";

            explanation.textContent =
                question.explanation || "";


            question.options.forEach(
                option => {

                    const optionButton =
                        document.createElement("button");

                    optionButton.className =
                        "quiz-option";

                    optionButton.textContent =
                        option;


                    optionButton.addEventListener(
                        "click",
                        () => {

                            const allOptions =
                                questionContainer.querySelectorAll(
                                    ".quiz-option"
                                );


                            allOptions.forEach(
                                button => {
                                    button.disabled = true;
                                }
                            );


                            if (
                                option ===
                                question.correct_answer
                            ) {

                                optionButton.classList.add(
                                    "correct"
                                );

                            } else {

                                optionButton.classList.add(
                                    "incorrect"
                                );


                                allOptions.forEach(
                                    button => {

                                        if (
                                            button.textContent ===
                                            question.correct_answer
                                        ) {

                                            button.classList.add(
                                                "correct"
                                            );
                                        }
                                    }
                                );
                            }


                            explanation.classList.remove(
                                "hidden"
                            );
                        }
                    );


                    questionContainer.appendChild(
                        optionButton
                    );
                }
            );


            questionContainer.appendChild(
                explanation
            );


            resultContent.appendChild(
                questionContainer
            );
        }
    );


    resultCard.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


/* -----------------------------------------------------------
   Submit
----------------------------------------------------------- */

submitButton.addEventListener(
    "click",
    async () => {

        const text =
            inputText.value.trim();


        if (!text) {

            showError(
                "Please enter a question, topic, or study material."
            );

            return;
        }


        const task =
            taskSelect.value;


        setLoading(true);


        try {

            let data;


            if (task === "qa") {

                data = await callAPI(
                    "/qa",
                    {
                        text: text
                    }
                );


                showResult(
                    data.answer
                );
            }


            else if (task === "explain") {

                data = await callAPI(
                    "/explain",
                    {
                        text: text,
                        level: levelSelect.value
                    }
                );


                showResult(
                    data.explanation
                );
            }


            else if (task === "quiz") {

                data = await callAPI(
                    "/quiz",
                    {
                        text: text,
                        number_of_questions:
                            Number(
                                quizCountInput.value
                            )
                    }
                );


                renderQuiz(
                    data.questions
                );
            }


            else if (task === "summarize") {

                data = await callAPI(
                    "/summarize",
                    {
                        text: text,
                        max_words: 150
                    }
                );


                showResult(
                    data.summary
                );
            }


            else if (task === "learn") {

                data = await callAPI(
                    "/learn/recommendations",
                    {
                        text: text,
                        level: levelSelect.value,
                        hours_per_week:
                            Number(
                                hoursInput.value
                            )
                    }
                );


                showResult(
                    data.recommendations
                );
            }

        } catch (error) {

            showError(
                error.message ||
                "An unexpected error occurred."
            );

        } finally {

            setLoading(false);
        }
    }
);


/* -----------------------------------------------------------
   Copy result
----------------------------------------------------------- */

copyButton.addEventListener(
    "click",
    async () => {

        if (!latestResultText) {

            return;
        }


        try {

            await navigator.clipboard.writeText(
                latestResultText
            );


            copyButton.textContent =
                "Copied!";


            setTimeout(
                () => {
                    copyButton.textContent =
                        "Copy";
                },
                1500
            );

        } catch {

            copyButton.textContent =
                "Copy failed";

            setTimeout(
                () => {
                    copyButton.textContent =
                        "Copy";
                },
                1500
            );
        }
    }
);