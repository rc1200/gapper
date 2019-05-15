
function myFunction() {
//  alert("Hello! I am an alert box! in myFunction");

  var $orders = $('#orders');
  var myText = $('#myText');
//  alert(myText.val());

      $.ajax({
            type: 'GET',
            url: '/myAjax/' + myText.val(),
//            url: 'http://127.0.0.1:8000/myAjax/',
            data: {'id': 'id', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
            success: function (data_dict) {
                console.log('ajax should work');
                console.log('success', data_dict);
                $orders.append('<li>' + data_dict.name + '</li>');
                $orders.append('data in loop');
                $.each(data_dict, function(i, data_x) {
                    $orders.append('<li>' + data_x + '</li>');
                });
                $orders.append('<hr>');

            }
        });
}


$("a").click(function(){
  alert("The paragraph was clicked.");
});


//$(function() { //when the DOM is ready
//  alert("Hello! I am an alert box! in ron js in ron js");
//
//      $.ajax({
//            type: 'GET',
//            url: 'http://127.0.0.1:8000/my_ajax_request/',
//            data: {'id': 'id', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
//            dataType: 'json',
//            success: function (data) {
//                console.log('success', data);
//            }
//        });
//});


function myFunction2() {
//  alert("Hello! I am an alert box! in myFunction");

  var $orders = $('#appendStockData');
  var symbol = $('#symbol').val();
  var outputType = $('#outputType').val();
//  var myText = $('#myText');
  alert(outputType);

      $.ajax({
            type: 'GET',
            url: '/returnStockData/' + symbol + '~' + outputType,
//            url: 'http://127.0.0.1:8000/myAjax/',
            data: {'id': 'id', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
            success: function (data_dict) {
                console.log('ajax should work');
                console.log('success', data_dict);
                $orders.append('<li>' + data_dict[0].date + '</li>');
                $orders.append('data in loop');
                $.each(data_dict, function(i, iterData) {
                    $orders.append('<li>' + data_dict[i].open + ' ~~ ' + iterData.low + '</li>');
                });
                $orders.append('<hr>');

            }
        });
}


function returnStockDataPriceRange() {
//  alert("Hello! I am an alert box! in myFunction");

  var appendFilteredPrice = $('#appendFilteredPrice');
  var lprice = $('#lprice').val();
  var hprice = $('#hprice').val();
//  var myText = $('#myText');
//  alert(lprice + " sdfsdf " + hprice);

      $.ajax({
            type: 'GET',
            url: '/returnStockDataPriceRange/' + lprice + '~' + hprice,
//            url: 'http://127.0.0.1:8000/myAjax/',
            data: {'id': 'id', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
            success: function (data_dict) {
                console.log('ajax should work');
                console.log('success', data_dict);
                appendFilteredPrice.append('<li>' + data_dict[0].date + '</li>');
                appendFilteredPrice.append('data in loop');
                $.each(data_dict, function(i, iterData) {
                    appendFilteredPrice.append('<li>' + data_dict[i].open + ' ~~ ' + iterData.low + '</li>');
                });
                appendFilteredPrice.append('<hr>');

            }
        });
}