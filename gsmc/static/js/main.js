const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


setTimeout(function(){
    $('#message').fadeOut('slow');
}, 3000);


function showForm(){
    document.getElementById("changeProfileForm").removeAttribute("hidden");
    document.getElementById("changeImage").setAttribute("hidden","true");
    document.getElementById("deactivate").setAttribute("hidden","true");
}


function hideForm(){
    document.getElementById("changeProfileForm").setAttribute("hidden","true");
    document.getElementById("changeImage").removeAttribute("hidden");
    document.getElementById("deactivate").removeAttribute("hidden");
}

