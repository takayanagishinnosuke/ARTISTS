function loading(){
  let result = window.confirm('生成に時間がかかりますが実行してよろしいですか？')
  if(result){
    $("#loading").show(3000);
    $("#content").hide();
    }
  }

