document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    //hide content in case of not specified group
    if (urlParams.has('group')) {
        document.getElementById('all_elements').hidden = false;
    } else {
        document.getElementById('closed').hidden = false;
    }

    //auto-fill id if specified
    if (urlParams.has('id')) {
        //console.log("id was received")
        document.getElementById('enter_id').hidden = true;
        document.getElementById('in_id').value = urlParams.get('id');
        $('#in_id').trigger('change');


    }
});