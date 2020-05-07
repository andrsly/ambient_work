document.addEventListener("DOMContentLoaded", function(){
    // Real time clock
    setInterval(function() {
      var currentTime = new Date();
    
      var hours = currentTime.getHours();
      var minutes = currentTime.getMinutes();
      var seconds = currentTime.getSeconds();

      if (seconds < 10) {
        seconds = "0" + seconds;
      }
      if (minutes < 10) {
        minutes = "0" + minutes;
      } 
      var clockTime = hours + ":" + minutes + ":" + seconds;
    
      var clock = document.getElementById('myclock');
      clock.innerText = clockTime;
    },500);

    // Exceeded preferred duration of total work session
    var warned = false;
    var pause = true;
    var workpause = document.getElementById('myworkpause');
    setInterval(function() {
      var compareDate = current_user_logintime;
      var currentTime = new Date()
      var prediff = (currentTime.getUTCHours() + currentTime.getUTCMinutes()/60 + currentTime.getUTCSeconds()/3600)
               - (new Date(compareDate.replace(/-/g,'/')).getHours() + new Date(compareDate.replace(/-/g,'/')).getMinutes()/60 + new Date(compareDate.replace(/-/g,'/')).getSeconds()/3600);
      var diff = Math.abs(prediff);
      var h = Math.floor(diff);
      var m = Math.floor((diff-h)*60);
      var s = Math.floor((((diff-h)*60)-m)*60);

      if ((h + m/60 + s/3600)>=current_user_hours) {
        var ex = document.getElementById('myexceeded');
        ex.innerText = "You have exceeded your preferred session duration!";
        workpause.innerText = "No more notifications for breaks will be given, due to exceeded limit!";
        pause = false;
      }
      if((h + m/60 + s/3600)>=current_user_hours && !warned){
        playAirhorn();
        warned=true;
      }
      var mod = (((h*60)+m+(s/60))%(parseInt(current_user_work) + parseInt(current_user_pause)));
      if((mod>=0.0) && (mod<parseInt(current_user_work)) && pause && prediff>0){
        if (mod<0.02) { playBell(); }
        workpause.innerText = "Work till the next break!";
      }
      if ((mod>=parseInt(current_user_work)) && pause) {
        workpause.innerText = "It is time for a break!";
        if (mod<(parseInt(current_user_work)+0.02)) { playBell(); }
        
      }
      if (s < 10) {
          s = "0" + s;
        }
      if (m < 10) {
          m = "0" + m;
        } 
      if (h < 10) {
          h = "0" + h;
        }
      var diffTime = h +":"+ m +":"+ s;
      var timer = document.getElementById('mytimer');
      timer.innerText = diffTime;

      var dur = document.getElementById("mydur");
      if (prediff<0){
        workpause.innerText = "Session will begin soon";
        dur.innerText = "Time until session begins"
      } else {
        dur.innerText = "Durration of current session"
      }
    },500);
    });
