$(document).ready(function(){
    console.log('this running on page load');
    var j_obj = "{}";
    $.ajax({
        async: false,
        url: "http://45.155.204.231:8000/list_service",
        type: "POST",
        data: {
            'change': 1
        },
        dataType:"json",
        success: function (data) {
            j_obj = data
        }
    })
    
    for (var key in j_obj) {
        var opts = j_obj[key];
        for (var id in opts){
            $(('#'+key)).append($('<option>', {
            value: id,
            text: opts[id]
            }));
        }
        
      }
      $('.invent').trigger("change");
});


$('.invent').on('change',function(){
    $("#var_list").empty();
    var j_obj = "{}";
    $.ajax({
        async: false,
        url: "http://45.155.204.231:8000/list_headers",
        type: "POST",
        data: {
            'plot_id': document.getElementById("select1").value,
            'source_id': document.getElementById("select2").value

        },
        dataType:"json",
        success: function (data) {
            j_obj = data
        }
    })
    inputs = j_obj.headers_code;
    opts = j_obj.headers_source;
    for (var selecter in inputs) {
    var selectList = document.createElement("select");
    selectList.id = inputs[selecter];
    selectList.classList.add('criteria');
    var label = document.createElement("label");
    label.innerText = inputs[selecter]
    var myParent = document.getElementById('var_list');
    myParent.appendChild(label);
    myParent.appendChild(selectList);
    //Create and append the options
    for (var id in opts){
        var option = document.createElement("option");
        option.text = opts[id];
        option.value = opts[id];
        var select = document.getElementById(inputs[selecter]);
        select.appendChild(option);
    }
}


});




document.getElementById("form").onsubmit = function(evt) {
    var key = $('select.criteria').map(function(){
        return this.value
    }).get();
    var value = $('select.criteria').map(function(){
        return this.id
    }).get();
    object = {};
    key.forEach(function (k, i) {
        object[k] = value[i];
    })
 
    document.getElementById("vars").value = JSON.stringify(object);
}

