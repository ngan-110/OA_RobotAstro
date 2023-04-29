// TO DISPLAY CURRENT DATE & TIME //
function displayDate() {
  setInterval(function() {
    var now = new Date();
    var options = { month: 'long', day: 'numeric', year: 'numeric', 
      hour: 'numeric', minute: 'numeric', second: 'numeric',
      timeZone: 'America/New_York' };
    var estDate = now.toLocaleString("en-US", options);
    document.getElementById('current-date-&-time').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + estDate;
  }, 1000);
} displayDate();
