let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player;
function onYouTubePlayerAPIReady(){
  player = new YT.Player("player", {
    events: {
      onReady: onPlayerReady
    }
  });
}


function loading(){
  $("#loading").show();
  $("#content").hide();
  player.playVideo(); //動かない     
}
