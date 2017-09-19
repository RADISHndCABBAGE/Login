/**
 * Created by admin on 2017/9/19.
 */

//向http://localhost:8888/index发送请求，获得json数据并解析。
$(function () {
  $.ajax({
      url: '/index',
      type: 'GET',
      dataType: 'json',
      timeout: 1000,
      cache: false,
      beforeSend: LoadFunction, //加载执行方法
      error: erryFunction,  //错误执行方法
      success: succFunction //成功执行方法
  })
  function LoadFunction() {
      $("#list").html('加载中...');
  }

  function erryFunction() {
      alert("error");
  }

  function succFunction(tt) {
      var json = JSON.parse(tt)
      $.each(json, function (index) {
          //循环获取数据
          $("#username").append(json[index].username);
          $("#password").append(json[index].password);
      });
      // var option = eval(tt)
      // for(var j=0;j<option.length;j++){
      //     $("#username").append(option[j].username);
      //     alert("made")
      //     $("#password").append(option[j].password);
      // }
  }
})
