function ajax_car(car_id){              //Функция аякс запроса, принимает айди марки авто
// <<<<<<< HEAD
//  $.ajax({
//     url: 'http://185.146.157.20:1337/api/v1/cars/'+car_id+'/',       //юрл меняем в зависимости айди марки авто
//     method: 'GET',
//     success: function(response, status) {
// 		models = response.car.model;                        // сохраняем модели принятой марки
// 		$('#id_car_model').find('option').remove();         // удаляем все марки
// 		for (let i = 0; i < models.length; i++) {           // цикл добавления моделей
//           let newOption = new Option(models[i]['model'], models[i]['id']);     // задаем новый опшн название модели итая и айдишник итая
//           id_car_model.append(newOption);                   // сохраняем в селект
// =======
     $.ajax({
        url: 'http://localhost:8000/api/v1/cars/'+car_id+'/',       //юрл меняем в зависимости айди марки авто
        method: 'GET',
        success: function(response, status) {
            models = response.car.model;                        // сохраняем модели принятой марки
            $('#id_car_model').find('option').remove();         // удаляем все марки
            for (let i = 0; i < models.length; i++) {           // цикл добавления моделей
              let newOption = new Option(models[i]['model'], models[i]['id']);     // задаем новый опшн название модели итая и айдишник итая
              id_car_model.append(newOption);                   // сохраняем в селект
            }
            id_car_model.value = old_model;                 // это при обновлении нужно, если есть олд модел тогда выбранным ставим его
        },
        error: function(response, status) {
            $('#id_car_model').find('option').remove();   // Удаление всех полей если ввыбрана -----
// >>>>>>> Кар моделс джиэс обновленный а так не помню
        }
    });
}
car = document.getElementById("id_car");    //находим селект марки авто
model = document.getElementById("id_car_model");  //находим селект модели авто
old_model = model.value;   //при обновлении нужно, если есть выбранная модель сохраняем
ajax_car(car.value);        //при обновлении нужно, отправка моделей сохраненной марки у пользователя
car.addEventListener('change', function(){ajax_car(car.value)});
