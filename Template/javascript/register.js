/**
 * Created by admin on 2017/9/25.
 */
function register(e)
{
    $.ajax({
        url:"/register",
        type:"post",
        //dataType:'json',
        data:{'username':$('#username').val(),'password':$('#password').val(),'hobby':$('#hobby').val()},
        beforeSend: function(xhr){xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');},
        success:function(data){
            jsonData = JSON.parse(data);
            if(jsonData.verification == "true"){
                window.location.href="/login.html";
            }else{
                window.location.href="/register.html";
            }
        },
        error:function(){
            console.log("error");
        }
    });
    e.preventDefault()
}
