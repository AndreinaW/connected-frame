const ctx = document.getElementById('man_woman_parity_chart').getContext('2d');

const parityChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["Men", "Women"],
        datasets: [{
            data: [0, 0],
            backgroundColor: ['rgb(41, 128, 185)', 'rgb(142, 68, 173)'],
            borderColor: 'rgb(85, 85, 85)'
        }],
    },
    options: {}
});

const url_parity = url_path + 'parity/';

fetch(url_parity)
    .then((resp) => resp.json())
    .then(function(data) {
        const jsonResp = data.parity;

        parityChart.data.datasets.forEach((dataset) => {
            dataset.data = [jsonResp.man, jsonResp.woman];
        });

        parityChart.update()
    })
    .catch(function(error) {
        console.log(error)
    });