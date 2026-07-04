(function(){
  var s=localStorage.getItem('tg_theme');
  if(s==='light')document.body.classList.add('light');
  var b=document.querySelector('.theme-toggle');
  if(b){
    b.addEventListener('click',function(){
      document.body.classList.toggle('light');
      var l=document.body.classList.contains('light');
      b.textContent=l?'☀️':'🌙';
      localStorage.setItem('tg_theme',l?'light':'dark');
    });
    b.textContent=document.body.classList.contains('light')?'☀️':'🌙';
  }
})();
