function systeme_done(id_work){
    var xhr = new XMLHttpRequest();
    console.log(id_work)
    
    
    $.ajax({
        url : "http://127.0.0.1:5000",
        type : 'POST',
        contentType : 'application/json',
        data: "{\"id_work\":\""+id_work+"\"}",
    });
    
};