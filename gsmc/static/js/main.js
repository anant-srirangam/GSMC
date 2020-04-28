const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


setTimeout(function(){
    $('#message').fadeOut('slow');
}, 3000);


$('#pages').twbsPagination({
    visiblePages: 2,
    onPageClick: function (event, page) {
        $('#page-content').text(page);
    }
});