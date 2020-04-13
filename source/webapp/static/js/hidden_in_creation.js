type = document.getElementById("id_type");   //Находим поле тип пользователя

status_child = document.getElementById("id_status"); //Находим поле статуса
statuss = status_child.parentNode;   //Находим блок статуса по его полю

car_child = document.getElementById("id_car");    //Находим поле марки авто
car_mark = car_child.parentNode;
//Находим блок марки авто по его полю
car_model_child = document.getElementById("id_car_model");
car_model = car_model_child.parentNode;

car_number_child = document.getElementById("id_car_number");
car_number = car_number_child.parentNode;

car_seats_child = document.getElementById("id_car_seats");
car_seats = car_seats_child.parentNode;

statuss.hidden = true;
car_mark.hidden = true;
car_model.hidden = true;
car_number.hidden = true;
car_seats.hidden = true;

function hide(type) {       //Создаем функцию прятания полей, принимает тип

  if (type === "client" || type === '' ) {
    statuss.hidden = true;
    car_mark.hidden = true;
    car_model.hidden = true;
    car_number.hidden = true;
    car_seats.hidden = true;
  } else if (type === "driver"){
    statuss.hidden = false;
    car_mark.hidden = false;
    car_model.hidden = false;
    car_number.hidden = false;
    car_seats.hidden = false;
  }
}
type.addEventListener('change', function(){hide(type.value)});      //Создаем листенер для типа ,
// если меняется значение то передаем ее в функцию скрывания полей
