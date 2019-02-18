const url_faces = url_path + 'total_faces/';

fetch(url_faces)
    .then((resp) => resp.json())
    .then(function(data) {
        document.getElementById('total_faces').innerHTML = data.totalFaces;
    })
    .catch(function(error) {
        console.log(error)
    });


const url_age = url_path + 'avg_age/';

fetch(url_age)
    .then((resp) => resp.json())
    .then(function(data) {
        document.getElementById('avg_age').innerHTML = data.currentAverageAge;
    })
    .catch(function(error) {
        console.log(error)
    });