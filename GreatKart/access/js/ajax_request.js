// Это все для HTML страницы ProductDetails (подробное описание товара)
$("#product select[name='color']").on('change', function () {
    var $this = $(this); // сохраняем в переменную текущий элемент
    $.ajax({ // инициализируем ajax запрос
        // получаем value текущего элемента
        url: '/shop/variant/' + $this.val() + '/', // указываем url
        type: 'GET', // тип запроса

        success: function (resp) { // вешаем свой обработчик на функцию success (успешный ответ сервера)
            let options = '';
            if ($('#size').find('option').length > 1) { // если в селекте уже есть опции, то удаляем их
                $('#size').find('option').nextAll().remove(); // удаляем все опции кроме первой
            }
            resp.size.forEach(size => {
                $('#size').append($('<option>', {
                    value: size.id,
                    text: size.size
                }));
            });
        },
        error: function (resp) {
            console.log('Something went wrong'); // выводим ошибку в консоль
        }
    });
});
// при выборе цвета, делаем ajax запрос на сервер, получаем размеры и добавляем их в селект
$("#product select[id='size']").on("change", function () {
    var $this = $(this); // сохраняем в переменную текущий элемент
    $.ajax({ // инициализируем ajax запрос
        // получаем value текущего элемента
        url: '/shop/size/' + $this.val() + '/price/quantity/', // указываем url для получения цены и количества
        type: 'GET', // тип запроса
        // изменять значение поля price при каждом запросе
        success: function (resp) { // вешаем свой обработчик на функцию success (успешный ответ сервера)
            // изменить значение тега span с id price
            $('#price').text("Цена: $" + resp.price);  // изменить значение тега id price на цену
            $('#quantity').text("Количество: " + resp.quantity);  // изменить значение тега id quantity на количество

        },
        error: function (resp) {
            console.log('Something went wrong');
        }
    });
});

