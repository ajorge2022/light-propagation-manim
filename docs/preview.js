"use strict";
(()=>{const vs=[...document.querySelectorAll(".preview-video[data-src]")];
const reduce=window.matchMedia("(prefers-reduced-motion: reduce)");
function load(v){if(v.dataset.loaded)return;v.src=v.dataset.src;v.dataset.loaded="true";v.load();}
function play(v){if(reduce.matches||document.hidden)return;const p=v.play();if(p&&p.catch)p.catch(()=>{});}
if("IntersectionObserver" in window){const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){load(e.target);play(e.target);}else e.target.pause();}),{rootMargin:"100px 0px",threshold:.01});vs.forEach(v=>obs.observe(v));}
else vs.forEach(v=>{load(v);play(v);});
document.addEventListener("visibilitychange",()=>{if(document.hidden)vs.forEach(v=>v.pause());else vs.filter(v=>v.dataset.loaded).forEach(play);});})();