document.addEventListener('DOMContentLoaded', function () {
    const carList = document.getElementById('car-list');
    const carForm = document.getElementById('car-form');

    // Função para carregar a lista de carros
    function loadCars() {
        fetch('/carros')
            .then(response => response.json())
            .then(data => {
                carList.innerHTML = '';
                data.dados.forEach(car => {
                    const carDiv = document.createElement('div');
                    carDiv.innerHTML = `
                        <strong>ID:</strong> ${car.id} <br>
                        <strong>Marca:</strong> ${car.marca} <br>
                        <strong>Modelo:</strong> ${car.modelo} <br>
                        <strong>Ano:</strong> ${car.ano} <br>
                        <button onclick="deleteCar(${car.id})">Excluir</button>
                        <button onclick="editCar(${car.id}, '${car.marca}', '${car.modelo}', ${car.ano})">Editar</button>
                    `;
                    carList.appendChild(carDiv);
                });
            });
    }

    // Função para adicionar um novo carro
    carForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = newFormData(carForm);
        const carData = {
            marca: formData.get('marca'),
            modelo: formData.get('modelo'),
            ano: formData.get('ano')
        };

        fetch('/carros', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(carData)
        })
        .then(response => response.json())
        .then(data => {
            loadCars();
            carForm.reset();
        });
    });

    // Função para excluir um carro
    window.deleteCar = function(id) {
        fetch(`/carros/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            loadCars();
        });
    };

    // Função para editar um carro
    window.editCar = function(id, marca, modelo, ano) {
        const newMarca = prompt('Nova Marca:', marca);
        const newModelo = prompt('Novo Modelo:', modelo);
        const newAno = prompt('Novo Ano:', ano);

        const carData = {
            marca: newMarca,
            modelo: newModelo,
            ano: parseInt(newAno)
        };

        fetch(`/carros/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(carData)
        })
        .then(response => response.json())
        .then(data => {
            loadCars();
        });
    };

    // Carregar a lista de carros ao iniciarloadCars();
});
