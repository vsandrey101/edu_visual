var langTools = ace.require("ace/ext/language_tools");

// var editor = 'editor-1';
// var editor = ace.edit(editor);
// editor.setTheme("ace/theme/github_light_default");
// editor.session.setMode("ace/mode/mysql");
// editor.setShowPrintMargin(false);
// editor.setOptions({
// enableBasicAutocompletion: true,
// enableSnippets: true,
// enableLiveAutocompletion: true
// });
    
var editor = 'editor-2';
var editor = ace.edit(editor);
editor.setShowPrintMargin(false);
editor.setTheme("ace/theme/github_light_default");
editor.session.setMode("ace/mode/python");
editor.setOptions({
enableBasicAutocompletion: true,
enableSnippets: true,
enableLiveAutocompletion: true,
fontSize: "large"
});


document.getElementById("form").onsubmit = function(evt) {
    document.getElementById("code").value = editor.getValue();
}

// document.getElementById("form").addEventListener("submit", function (e) {
//     e.preventDefault();
      
//     var formData = new FormData(form);
//     // output as an object
//     var f_name_in = formData.get("fname");
//     var index_in = formData.get("index");
//     // var group_in = formData.get("groups");
//     // var editor = ace.edit('editor-1');
//     // var query_in = editor.getValue();
//     var editor = ace.edit('editor-2');
//     var plt_config_in = editor.getValue();
//     $.ajax({
//         url: 'http://45.155.204.231:8000/add_plot',
//         type: 'POST',
//         data: {
//             name: f_name_in,
//             index: index_in,
//             code: plt_config_in
//         },
//         success: function (response) {
//             alert("Успешно добавлен новый график");
//         },
//         error: function (response) {   
//             alert("Ошибка добавления графика");
//         }
//         });
//     })