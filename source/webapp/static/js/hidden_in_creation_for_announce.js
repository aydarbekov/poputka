type = document.getElementById("id_type");   //Находим поле тип пользователя

description_child = document.getElementById("id_description"); //Находим поле описания
description = description_child.parentNode;   //Находим блок описания по его полю

place_from_child = document.getElementById("id_place_from");
place_from = place_from_child.parentNode;

place_to_child = document.getElementById("id_place_to");
place_to = place_to_child.parentNode;

departure_time_child = document.getElementById("id_departure_time");
departure_time = departure_time_child.parentNode;

seats_child = document.getElementById("id_seats");
seats = seats_child.parentNode;

luggage_child = document.getElementById("id_luggage");
luggage = luggage_child.parentNode;

price_child = document.getElementById("id_price");
price = price_child.parentNode;

photo_child = document.getElementById("id_photo");
photo = photo_child.parentNode;

car_child = document.getElementById("id_car");    //Находим поле марки авто
car_mark = car_child.parentNode;

car_model_child = document.getElementById("id_car_model");
car_model = car_model_child.parentNode;


description.hidden = true;
place_from.hidden = true;
place_to.hidden = true;
departure_time.hidden = true;
seats.hidden = true;
luggage.hidden = true;
price.hidden = true;
photo.hidden = true;
car_mark.hidden = true;
car_model.hidden = true;

function hide(type) {       //Создаем функцию прятания полей, принимает тип обьявления
  if (type === "client" ) {
    description.hidden = false;
    place_from.hidden = false;
    place_to.hidden = false;
    departure_time.hidden = false;
    seats.hidden = false;
    luggage.hidden = false;
    price.hidden = false;
    car_mark.hidden = true;
    car_model.hidden = true;
    photo.hidden = true;
  } else if (type === "driver"){
    description.hidden = false;
    place_from.hidden = false;
    place_to.hidden = false;
    departure_time.hidden = false;
    seats.hidden = false;
    luggage.hidden = false;
    price.hidden = false;
    photo.hidden = false;
    car_mark.hidden = false;
    car_model.hidden = false;

  } else if (type === ''){
    description.hidden = true;
    place_from.hidden = true;
    place_to.hidden = true;
    departure_time.hidden = true;
    seats.hidden = true;
    luggage.hidden = true;
    price.hidden = true;
    photo.hidden = true;
    car_mark.hidden = true;
    car_model.hidden = true;

  }
}
type.addEventListener('change', function(){hide(type.value)});      //Создаем листенер для типа, если
// меняется значение то передаем ее в функцию скрывания полей
