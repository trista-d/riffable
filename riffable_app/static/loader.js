// show css loading sign before redirecting to play.html
function showLoading() {
    let body = document.getElementById("main");
    body.style.display = 'none';
    
    let container = document.createElement("div");
    container.setAttribute('id', 'cont');
    
    let div = document.createElement("div");
    div.setAttribute('class', 'loader');
    container.appendChild(div);
    
    let msg = document.createElement("div");
    msg.innerHTML = 'Loading song...';
    container.appendChild(msg);

    document.body.appendChild(container);
}