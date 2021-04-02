// javascript funktionality for search.html, i.e. search-view

// this allows user to enter search terms directly after loading the page
document.getElementById('searchbox').focus();

// just a sanity check
// function bgColorHover(){
//     this.style = "background-color: blue;"
// }
// document.querySelectorAll('.ergebnis').forEach(el => {
//     el.addEventListener('mouseover', bgColorHover);
// });

function getArtikelText(id){
// returns a promise; call function with getArtikelText(id).then()
    return fetch('http://10.98.228.171/artikel/api/' + id + '?json')
    .then(response => response.json()) 
    .then(json => json.text)
}
function attachOnClick(e){
    if(e.target.tagName == "LI"){
        target = e.target;
    }else if (e.target.tagName == "SPAN"){
        target = e.target.parentNode;
    }else if (e.target.tagName == "DIV"){
        target = e.target.parentNode.parentNode;
    }
    let id = target.id;
    let divWrapper = target.getElementsByClassName("txt-wrapper")[0];
    let divTxt = divWrapper.getElementsByClassName("txt")[0];
    if(divTxt.innerHTML){
        // if user clicks again, remove artikel-text
        divTxt.innerHTML = "";
        divWrapper.style = "display: none;";
    }else{
        // display artikel-text, accordion-style
        getArtikelText(id)
        .then(txt => { 
            divTxt.innerHTML = txt;
            divWrapper.style = "";
        });
    }
}
// document.querySelectorAll('.ergebnis').forEach(el => {
//     el.addEventListener('click', attachOnClick);
// });
// using event object to attach callback function to one <ul> instead of 50 <li>
let ul = document.getElementsByTagName('ul')[0];
ul.addEventListener('click', e => { attachOnClick(e) }, false);
