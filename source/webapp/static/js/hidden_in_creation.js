type = document.getElementById("id_type");   //Находим поле тип пользователя

status_child = document.getElementById("id_status"); //Находим поле статуса
statuss = status_child.parentNode;   //Находим блок статуса по его полю

car_child = document.getElementById("id_car");    //Находим поле марки авто
car = car_child.parentNode;       //Находим блок марки авто по его полю

car_model_child = document.getElementById("id_car_model");    //Находим поле года окончания
car_model = car_model_child.parentNode;       //Находим блок года окончания по его полю

car_number_child = document.getElementById("id_car_number");    //Находим поле года окончания
car_number = car_number_child.parentNode;       //Находим блок года окончания по его полю

car_seats_child = document.getElementById("id_car_seats");    //Находим поле года окончания
car_seats = car_seats_child.parentNode;       //Находим блок года окончания по его полю

statuss.hidden = true;
car.hidden = true;
car_model.hidden = true;
car_number.hidden = true;
car_seats.hidden = true;

function hide(type) {       //Создаем функцию прятания полей, принимает тип эксперта
  console.log(type);

  if (type === "client" || type === '' ) {     //Если тип междунар эксперт или работодатель, то скрываем поля сертифицированности, аффилированности и года окончания
    statuss.hidden = true;
    car.hidden = true;
    car_model.hidden = true;
    car_number.hidden = true;
    car_seats.hidden = true;
  } else if (type === "driver"){
    statuss.hidden = false;
    car.hidden = false;
    car_model.hidden = false;
    car_number.hidden = false;
    car_seats.hidden = false;
  }
}
type.addEventListener('change', function(){hide(type.value)});      //Создаем листенер для типа эксперта, если меняется значение то передаем ее в функцию скрывания полей
