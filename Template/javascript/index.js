/**
 * Created by admin on 2017/9/19.
 */

$(function () {
  $.ajax({
      url: '/index',
      type: 'GET',
      dataType: 'json',
      timeout: 1000,
      crossDomain: true,
      cache: false,
      beforeSend: LoadFunction, //加载执行方法
      error: erryFunction,  //错误执行方法
      success: succFunction //成功执行方法
  })
  function LoadFunction() {
      $("#list").html('加载中...');
  }

  function erryFunction(data) {
      console.log(data)
      alert("错误");
  }

  function succFunction(data) {
        $("#username").append(data['username'])
        $("#password").append(data['password'])
        $("#hobby").append(data['hobby'])
  }
})

function quit(e){
    $.ajax({
        url:"/quit",
        type:"GET",
        error: function (data){
            alert("error");
            console.log(data);
        },
        success: function(){
            $.cookies.del('session_id');
        }
    });
    e.preventDefault();
}
