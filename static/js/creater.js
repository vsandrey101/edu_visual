function add_list(){
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://45.155.204.231:8000/list_plots");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const urlParams = new URLSearchParams(window.location.search);
    const body = JSON.stringify({
    type: "all",
    });
    xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log(JSON.parse(xhr.responseText));
    } else {
        console.log(`Error: ${xhr.status}`);
    }
    };
    xhr.send(body);
}