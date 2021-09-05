function change(el){
    let fieldset = this.document.getElementById('info_for_' + el.name)
    if (fieldset.hidden==true){
        fieldset.hidden=false
        fieldset.disabled=false
    } else {
        fieldset.hidden=true
        fieldset.disabled=true
    }
}

function checkdate(el){
    let today = new Date()
    if (Date.parse(el.value) <= Date.parse(today)){
        alert ( "You can't submit in the past. Please change the date" );
        valid = false;
        el.value = NaN
    }
    return valid;
}
