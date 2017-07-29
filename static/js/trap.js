$(function(){

  $("#contentDrop").change(function(){
    var selected = $(this).find(":selected").val();
    if (selected=="custom"){
      $("#contentDrop").after(
        '<div class="ui input" id="customContent">'
        +
        '<input type="text" id="contentURL" placeholder="http://real-site.com/abc/page.aspx">'
        +
        '</div>'
      );
    }
    else{
      $("#customContent").remove();
    }
  });

  $("#submit").click(function(){
    var notes = $("#notes").val();
    var url = $("#url").val();
    var content = $("#contentDrop").find(":selected").val();
    if (content == "custom"){
      content = $("#contentURL").val();
    }
    var time = $("#time").find(":selected").val();
    var email = $("#email").val();

    var postData = {};
    postData["notes"] = notes;
    postData["url"] = url;
    postData["content"] = content;
    postData["time"] = time;
    postData["email"] = email;

    $.ajax({
      type:   "POST",
      url:    "/set",
      data:   postData,
      success: function(response, xml){
        alert("Sent Success");
        if (response == "1"){
          alert("架设成功");
        }
        else{
          if (response == "0"){
            alert("架设失败");
          }
          else{
            alert(response);
          }
        }
      },
      fail: function(status){
        alert(status);
      }
    });

  });

});
