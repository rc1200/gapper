
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

  var $orders = $('#orders');
  var myText = $('#myOpt');
//  var myText = $('#myText');
  alert(myText);

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