$('.submit').click(function(){
    var code = editor.getSession().getValue();
    var language = $("#languages").val();
    $.ajax({
        type: "GET",
        url: "/text_extract",
        contentType: 'application/json;charset=UTF-8',
        data: {'code':code, 'language':language},
        success: function(data,status){
            document.getElementById('show-term').style.display = 'block';
            document.getElementById('show-term-label').style.display = 'block';
            document.getElementById('hide-term').style.display = 'block';
            var output = JSON.parse(data);
            console.log(output)
            $('#show-term').text(output);
        }
    });
});