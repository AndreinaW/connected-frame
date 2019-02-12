const toReplace = document.getElementById('face_expression_chart').getContext('2d');

const exprDoughnut = new Chart(toReplace, {
    type: 'doughnut',
    data: {
        labels: ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"],
        datasets: [{
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                'rgb(157, 41, 51)',   // Anger
                'rgb(135, 95, 154)',  // Contempt
                'rgb(141, 178, 85)',  // Disgust
                'rgb(19, 15, 64)',    // Fear
                'rgb(224, 86, 253)',  // Happiness
                'rgb(191, 191, 191)', // Neutral
                'rgb(83, 92, 104)',   // Sadness
                'rgb(126, 214, 223)'  // Surprise
            ],
            borderColor: 'rgb(85, 85, 85)',
        }]
    },
    options: {}
});

const url_expr = 'http://localhost:8080/api/data/expressions';

fetch(url_expr)
    .then((resp) => resp.json())
    .then(function(data) {
        const jsonResp = data.expressions;

        exprDoughnut.data.datasets.forEach((dataset) => {
            dataset.data = [jsonResp.anger, jsonResp.comtempt, jsonResp.disgust, jsonResp.fear, jsonResp.happiness, jsonResp.neutral, jsonResp.sadness, jsonResp.surprise];
        });

        exprDoughnut.update()
    })
    .catch(function(error) {
        console.log(error)
    });