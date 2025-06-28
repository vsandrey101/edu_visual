$(document).ready(function(){
    $('#tables').trigger("change");
});

$('#tables').on('change',function(){
    //console.log(document.getElementById('type').value)
    $.ajax({
        url: "/load_manager",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('tables').value,       
        },
        dataType:"html",
        success: function (data) {
            $("#f_table").html(data)
        }
    });
})

var cells = document.querySelectorAll("#position td");
for (var i = 0; i < cells.length; i++) {
  cells[i].addEventListener("click", function() {
    console.log(this.innerHTML);
  });
}
