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


function companySelect(){
    var company = document.getElementById('company');
    var companyName = document.getElementById('companyName');
    var companyUrl = document.getElementById('companyUrl');
    var companyLogo = document.getElementById('companyLogo');

    if(company.value == "Other"){
        companyName.setAttribute("required","true");
        companyName.removeAttribute("disabled");
        companyUrl.setAttribute("required","true");
        companyUrl.removeAttribute("disabled");
        companyLogo.setAttribute("required","true");
        companyLogo.removeAttribute("disabled");
    }
    else{
        companyName.setAttribute("disabled","true");
        companyName.removeAttribute("required");
        companyUrl.setAttribute("disabled","true");
        companyUrl.removeAttribute("required");
        companyLogo.setAttribute("disabled","true");
        companyLogo.removeAttribute("required");
    }
}