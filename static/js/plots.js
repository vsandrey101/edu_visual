//таймер
var handle;

const popup = new Popup({
    id: "override",
    title: "Обратная связь",
    content: `Оцените, пожалуйста, текущую диграмму!
      custom-space-out big-margin§{btn-r1-override}[1]{btn-r2-override}[2]{btn-r3-override}[3]{btn-r4-override}[4]{btn-r5-override}[5]`,
    sideMargin: "1.5em",
    fontSizeMultiplier: "1.2",
    backgroundColor: "#b5bff5",
    allowClose: false,
    css: `
    .popup.override .custom-space-out {
        display: flex;
        justify-content: center;
        gap: 1.5em;
    }`,
    loadCallback: () => {
        /* button functionality */
        document.querySelectorAll(".popup.override button").forEach((button) => {
            button.addEventListener("click", () => {
                
                $.ajax({
                    async: false,
                    url: "https://script.google.com/macros/s/AKfycbwo6SSkVM-K4dIGcyfBWfdldz4YjLITP5AeU--mINNt50AwDhvvy29KtdGxMTrO3Nwiog/exec",
                    type: "POST",
                    data: {
                        'plot_id': document.getElementById('type').value,
                        'plot_name': document.getElementById('type').innerHTML,
                        'mark': button.innerHTML
                    },
                    dataType:"json",
                    success: function(){
                        
                    }
                });
                popup.hide();
                
            });
        });
    },
})

function enable_track(plot_id){
    
    plot_id.on('plotly_hover', function(){
        //alert('You this Plotly chart!');
        yaCounter99026826.reachGoal('interaction',
                {type: "plotly_hover",
                selected: document.getElementById('type').value
                });
        console.log("hover trigger");
    });
    plot_id.on('plotly_legendclick', function(){
        yaCounter99026826.reachGoal('interaction',
                {type: "plotly_legendclick",
                selected: document.getElementById('type').value
                });
        console.log("legend trigger");
    });
    plot_id.on('plotly_click', function(){
        yaCounter99026826.reachGoal('interaction',
                {type: "plotly_click",
                selected: document.getElementById('type').value
                });
        console.log("click trigger");
    });

}



// $(document).ready(function(){
//     console.log('this running on page load');
//     const urlParams = new URLSearchParams(window.location.search);
//     indexes = [];
//     names = [];
//     $.ajax({
//         async: false,
//         url: "http://45.155.204.231:8000/list",
//         type: "POST",
//         data: {
//             'role': key_var
//         },
//         dataType:"json",
//         success: function (data) {
//             for (var i = 0; i < data.length; i++) {
//                 indexes.push(data[i][0]);
//                 //console.log(data[i][0]);
//                 names.push(data[i][1]);
//             }
            

//         }
//     });

    
  
//     select = document.getElementById('type');
//     for (var i = 0; i < indexes.length; i++) {
//         var opt = document.createElement('option');
//         opt.value = indexes[i];
//         opt.innerHTML = names[i];
//         select.appendChild(opt);
//     }
//     console.log("Elements appended")
//     enable_track(document.getElementById('bargraph'));
// });



// function redirect(){
//     const urlParams = new URLSearchParams(window.location.search);
//     key = urlParams.get('key')
//     id = urlParams.get('id')
//     window.open(("http://45.155.204.231:8000/editor?id=" + id + "&key=" + key));
// }


$('#in_id').on('change',function(){
    var user_id = document.getElementById('in_id').value;
    $("#type").empty();
    console.log('ID has changed');
    indexes = [];
    names = [];
    $.ajax({
        async: false,
        url: "http://45.155.204.231:8000/list",
        type: "POST",
        data: {
            'user_id': user_id
        },
        dataType:"json",
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                indexes.push(data[i][0]);
                //console.log(data[i][0]);
                names.push(data[i][1]);
            }
            

        }
    });

    
    select = document.getElementById('type');
    for (var i = 0; i < indexes.length; i++) {
        var opt = document.createElement('option');
        opt.value = indexes[i];
        opt.innerHTML = names[i];
        select.appendChild(opt);
    }
    select.selectedIndex = 0;
    select = $("#type");
    select.trigger( "change" );
    console.log("Elements appended")
})

$('#type').on('change',function(){
    //console.log(document.getElementById('type').value)
    $.ajax({
        url: "/bar",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('type').value,
            'id': document.getElementById('in_id').value        
        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('bargraph', data );
            enable_track(document.getElementById('bargraph'));
            clearTimeout(handle);
            handle = setTimeout(function() {
                popup.show();
          }, 5000);
        }
    });
})
