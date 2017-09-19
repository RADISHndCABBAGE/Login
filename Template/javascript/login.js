/**
* Created by admin on 2017/9/19.
*/
function openIndex(e){

    $.ajax({
       url: "/login",
       type: "POST",
       crossDomain: true,
       data: {"username":$('#username').val(),"password":$('#password').val()},
       success: function (response) {
         console.log(response);
           if(response.ok == 'yes'){
                window.location.href="/index.html"
           }
       },
       error: function (xhr, status) {
         alert("error");
       }
     });
    e.preventDefault()

}
