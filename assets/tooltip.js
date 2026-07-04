(function(){
  var tip=document.createElement('div');tip.id='term-tooltip';document.body.appendChild(tip);
  var cur=null;
  function show(t){
    var p=t.querySelector('.term-popup');if(!p)return;
    tip.textContent=p.textContent;tip.style.display='block';tip.classList.remove('below');
    var r=t.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight;
    var left=r.left+r.width/2-tw/2;
    left=Math.max(8,Math.min(left,window.innerWidth-tw-8));
    var top=r.top-th-10;
    if(top<8){top=r.bottom+10;tip.classList.add('below');}
    tip.style.left=left+'px';tip.style.top=top+'px';cur=t;
  }
  function hide(){tip.style.display='none';cur=null;}
  document.querySelectorAll('.term').forEach(function(t){
    t.setAttribute('tabindex','0');
    t.addEventListener('mouseenter',function(){show(t);});
    t.addEventListener('mouseleave',hide);
    t.addEventListener('focus',function(){show(t);});
    t.addEventListener('blur',hide);
    t.addEventListener('click',function(e){e.stopPropagation();if(cur===t)hide();else show(t);});
  });
  document.addEventListener('click',hide);
  window.addEventListener('scroll',function(){if(cur)show(cur);},{passive:true});
})();
