"use strict";(self["webpackChunkfrontend_web"]=self["webpackChunkfrontend_web"]||[]).push([[88],{76088:function(t,e,n){n.d(e,{JO:function(){return ce}});n(70560),n(98858),n(61318),n(33228);var o=n(73396);const r=/^[a-z0-9]+(-[a-z0-9]+)*$/,i=(t,e,n,o="")=>{const r=t.split(":");if("@"===t.slice(0,1)){if(r.length<2||r.length>3)return null;o=r.shift().slice(1)}if(r.length>3||!r.length)return null;if(r.length>1){const t=r.pop(),n=r.pop(),i={provider:r.length>0?r[0]:o,prefix:n,name:t};return e&&!c(i)?null:i}const i=r[0],s=i.split("-");if(s.length>1){const t={provider:o,prefix:s.shift(),name:s.join("-")};return e&&!c(t)?null:t}if(n&&""===o){const t={provider:o,prefix:"",name:i};return e&&!c(t,n)?null:t}return null},c=(t,e)=>!!t&&!(""!==t.provider&&!t.provider.match(r)||!(e&&""===t.prefix||t.prefix.match(r))||!t.name.match(r)),s=Object.freeze({left:0,top:0,width:16,height:16}),a=Object.freeze({rotate:0,vFlip:!1,hFlip:!1}),l=Object.freeze({...s,...a}),f=Object.freeze({...l,body:"",hidden:!1});function u(t,e){const n={};!t.hFlip!==!e.hFlip&&(n.hFlip=!0),!t.vFlip!==!e.vFlip&&(n.vFlip=!0);const o=((t.rotate||0)+(e.rotate||0))%4;return o&&(n.rotate=o),n}function d(t,e){const n=u(t,e);for(const o in f)o in a?o in t&&!(o in n)&&(n[o]=a[o]):o in e?n[o]=e[o]:o in t&&(n[o]=t[o]);return n}function p(t,e){const n=t.icons,o=t.aliases||Object.create(null),r=Object.create(null);function i(t){if(n[t])return r[t]=[];if(!(t in r)){r[t]=null;const e=o[t]&&o[t].parent,n=e&&i(e);n&&(r[t]=[e].concat(n))}return r[t]}return(e||Object.keys(n).concat(Object.keys(o))).forEach(i),r}function h(t,e,n){const o=t.icons,r=t.aliases||Object.create(null);let i={};function c(t){i=d(o[t]||r[t],i)}return c(e),n.forEach(c),d(t,i)}function g(t,e){const n=[];if("object"!==typeof t||"object"!==typeof t.icons)return n;t.not_found instanceof Array&&t.not_found.forEach((t=>{e(t,null),n.push(t)}));const o=p(t);for(const r in o){const i=o[r];i&&(e(r,h(t,r,i)),n.push(r))}return n}const b={provider:"",aliases:{},not_found:{},...s};function m(t,e){for(const n in e)if(n in t&&typeof t[n]!==typeof e[n])return!1;return!0}function y(t){if("object"!==typeof t||null===t)return null;const e=t;if("string"!==typeof e.prefix||!t.icons||"object"!==typeof t.icons)return null;if(!m(t,b))return null;const n=e.icons;for(const i in n){const t=n[i];if(!i.match(r)||"string"!==typeof t.body||!m(t,f))return null}const o=e.aliases||Object.create(null);for(const i in o){const t=o[i],e=t.parent;if(!i.match(r)||"string"!==typeof e||!n[e]&&!o[e]||!m(t,f))return null}return e}const v=Object.create(null);function x(t,e){return{provider:t,prefix:e,icons:Object.create(null),missing:new Set}}function w(t,e){const n=v[t]||(v[t]=Object.create(null));return n[e]||(n[e]=x(t,e))}function j(t,e){return y(e)?g(e,((e,n)=>{n?t.icons[e]=n:t.missing.add(e)})):[]}function k(t,e,n){try{if("string"===typeof n.body)return t.icons[e]={...n},!0}catch(o){}return!1}let S=!1;function O(t){return"boolean"===typeof t&&(S=t),S}function I(t){const e="string"===typeof t?i(t,!0,S):t;if(e){const t=w(e.provider,e.prefix),n=e.name;return t.icons[n]||(t.missing.has(n)?null:void 0)}}function E(t,e){const n=i(t,!0,S);if(!n)return!1;const o=w(n.provider,n.prefix);return k(o,n.name,e)}function M(t,e){if("object"!==typeof t)return!1;if("string"!==typeof e&&(e=t.provider||""),S&&!e&&!t.prefix){let e=!1;return y(t)&&(t.prefix="",g(t,((t,n)=>{n&&E(t,n)&&(e=!0)}))),e}const n=t.prefix;if(!c({provider:e,prefix:n,name:"a"}))return!1;const o=w(e,n);return!!j(o,t)}const F=Object.freeze({width:null,height:null}),C=Object.freeze({...F,...a}),L=/(-?[0-9.]*[0-9]+[0-9.]*)/g,T=/^-?[0-9.]*[0-9]+[0-9.]*$/g;function _(t,e,n){if(1===e)return t;if(n=n||100,"number"===typeof t)return Math.ceil(t*e*n)/n;if("string"!==typeof t)return t;const o=t.split(L);if(null===o||!o.length)return t;const r=[];let i=o.shift(),c=T.test(i);while(1){if(c){const t=parseFloat(i);isNaN(t)?r.push(i):r.push(Math.ceil(t*e*n)/n)}else r.push(i);if(i=o.shift(),void 0===i)return r.join("");c=!c}}const z=t=>"unset"===t||"undefined"===t||"none"===t;function A(t,e){const n={...l,...t},o={...C,...e},r={left:n.left,top:n.top,width:n.width,height:n.height};let i=n.body;[n,o].forEach((t=>{const e=[],n=t.hFlip,o=t.vFlip;let c,s=t.rotate;switch(n?o?s+=2:(e.push("translate("+(r.width+r.left).toString()+" "+(0-r.top).toString()+")"),e.push("scale(-1 1)"),r.top=r.left=0):o&&(e.push("translate("+(0-r.left).toString()+" "+(r.height+r.top).toString()+")"),e.push("scale(1 -1)"),r.top=r.left=0),s<0&&(s-=4*Math.floor(s/4)),s%=4,s){case 1:c=r.height/2+r.top,e.unshift("rotate(90 "+c.toString()+" "+c.toString()+")");break;case 2:e.unshift("rotate(180 "+(r.width/2+r.left).toString()+" "+(r.height/2+r.top).toString()+")");break;case 3:c=r.width/2+r.left,e.unshift("rotate(-90 "+c.toString()+" "+c.toString()+")");break}s%2===1&&(r.left!==r.top&&(c=r.left,r.left=r.top,r.top=c),r.width!==r.height&&(c=r.width,r.width=r.height,r.height=c)),e.length&&(i='<g transform="'+e.join(" ")+'">'+i+"</g>")}));const c=o.width,s=o.height,a=r.width,f=r.height;let u,d;null===c?(d=null===s?"1em":"auto"===s?f:s,u=_(d,a/f)):(u="auto"===c?a:c,d=null===s?_(u,f/a):"auto"===s?f:s);const p={},h=(t,e)=>{z(e)||(p[t]=e.toString())};return h("width",u),h("height",d),p.viewBox=r.left.toString()+" "+r.top.toString()+" "+a.toString()+" "+f.toString(),{attributes:p,body:i}}const N=/\sid="(\S+)"/g,P="IconifyId"+Date.now().toString(16)+(16777216*Math.random()|0).toString(16);let R=0;function $(t,e=P){const n=[];let o;while(o=N.exec(t))n.push(o[1]);if(!n.length)return t;const r="suffix"+(16777216*Math.random()|Date.now()).toString(16);return n.forEach((n=>{const o="function"===typeof e?e(n):e+(R++).toString(),i=n.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");t=t.replace(new RegExp('([#;"])('+i+')([")]|\\.[a-z])',"g"),"$1"+o+r+"$3")})),t=t.replace(new RegExp(r,"g"),""),t}const D=Object.create(null);function U(t,e){D[t]=e}function q(t){return D[t]||D[""]}function J(t){let e;if("string"===typeof t.resources)e=[t.resources];else if(e=t.resources,!(e instanceof Array)||!e.length)return null;const n={resources:e,path:t.path||"/",maxURL:t.maxURL||500,rotate:t.rotate||750,timeout:t.timeout||5e3,random:!0===t.random,index:t.index||0,dataAfterTimeout:!1!==t.dataAfterTimeout};return n}const Q=Object.create(null),H=["https://api.simplesvg.com","https://api.unisvg.com"],B=[];while(H.length>0)1===H.length||Math.random()>.5?B.push(H.shift()):B.push(H.pop());function V(t,e){const n=J(e);return null!==n&&(Q[t]=n,!0)}function Z(t){return Q[t]}Q[""]=J({resources:["https://api.iconify.design"].concat(B)});const G=()=>{let t;try{if(t=fetch,"function"===typeof t)return t}catch(e){}};let K=G();function W(t,e){const n=Z(t);if(!n)return 0;let o;if(n.maxURL){let t=0;n.resources.forEach((e=>{const n=e;t=Math.max(t,n.length)}));const r=e+".json?icons=";o=n.maxURL-t-n.path.length-r.length}else o=0;return o}function X(t){return 404===t}const Y=(t,e,n)=>{const o=[],r=W(t,e),i="icons";let c={type:i,provider:t,prefix:e,icons:[]},s=0;return n.forEach(((n,a)=>{s+=n.length+1,s>=r&&a>0&&(o.push(c),c={type:i,provider:t,prefix:e,icons:[]},s=n.length),c.icons.push(n)})),o.push(c),o};function tt(t){if("string"===typeof t){const e=Z(t);if(e)return e.path}return"/"}const et=(t,e,n)=>{if(!K)return void n("abort",424);let o=tt(e.provider);switch(e.type){case"icons":{const t=e.prefix,n=e.icons,r=n.join(","),i=new URLSearchParams({icons:r});o+=t+".json?"+i.toString();break}case"custom":{const t=e.uri;o+="/"===t.slice(0,1)?t.slice(1):t;break}default:return void n("abort",400)}let r=503;K(t+o).then((t=>{const e=t.status;if(200===e)return r=501,t.json();setTimeout((()=>{n(X(e)?"abort":"next",e)}))})).then((t=>{"object"===typeof t&&null!==t?setTimeout((()=>{n("success",t)})):setTimeout((()=>{404===t?n("abort",t):n("next",r)}))})).catch((()=>{n("next",r)}))},nt={prepare:Y,send:et};function ot(t){const e={loaded:[],missing:[],pending:[]},n=Object.create(null);t.sort(((t,e)=>t.provider!==e.provider?t.provider.localeCompare(e.provider):t.prefix!==e.prefix?t.prefix.localeCompare(e.prefix):t.name.localeCompare(e.name)));let o={provider:"",prefix:"",name:""};return t.forEach((t=>{if(o.name===t.name&&o.prefix===t.prefix&&o.provider===t.provider)return;o=t;const r=t.provider,i=t.prefix,c=t.name,s=n[r]||(n[r]=Object.create(null)),a=s[i]||(s[i]=w(r,i));let l;l=c in a.icons?e.loaded:""===i||a.missing.has(c)?e.missing:e.pending;const f={provider:r,prefix:i,name:c};l.push(f)})),e}function rt(t,e){t.forEach((t=>{const n=t.loaderCallbacks;n&&(t.loaderCallbacks=n.filter((t=>t.id!==e)))}))}function it(t){t.pendingCallbacksFlag||(t.pendingCallbacksFlag=!0,setTimeout((()=>{t.pendingCallbacksFlag=!1;const e=t.loaderCallbacks?t.loaderCallbacks.slice(0):[];if(!e.length)return;let n=!1;const o=t.provider,r=t.prefix;e.forEach((e=>{const i=e.icons,c=i.pending.length;i.pending=i.pending.filter((e=>{if(e.prefix!==r)return!0;const c=e.name;if(t.icons[c])i.loaded.push({provider:o,prefix:r,name:c});else{if(!t.missing.has(c))return n=!0,!0;i.missing.push({provider:o,prefix:r,name:c})}return!1})),i.pending.length!==c&&(n||rt([t],e.id),e.callback(i.loaded.slice(0),i.missing.slice(0),i.pending.slice(0),e.abort))}))})))}let ct=0;function st(t,e,n){const o=ct++,r=rt.bind(null,n,o);if(!e.pending.length)return r;const i={id:o,icons:e,callback:t,abort:r};return n.forEach((t=>{(t.loaderCallbacks||(t.loaderCallbacks=[])).push(i)})),r}function at(t,e=!0,n=!1){const o=[];return t.forEach((t=>{const r="string"===typeof t?i(t,e,n):t;r&&o.push(r)})),o}var lt={resources:[],index:0,timeout:2e3,rotate:750,random:!1,dataAfterTimeout:!1};function ft(t,e,n,o){const r=t.resources.length,i=t.random?Math.floor(Math.random()*r):t.index;let c;if(t.random){let e=t.resources.slice(0);c=[];while(e.length>1){const t=Math.floor(Math.random()*e.length);c.push(e[t]),e=e.slice(0,t).concat(e.slice(t+1))}c=c.concat(e)}else c=t.resources.slice(i).concat(t.resources.slice(0,i));const s=Date.now();let a,l="pending",f=0,u=null,d=[],p=[];function h(){u&&(clearTimeout(u),u=null)}function g(){"pending"===l&&(l="aborted"),h(),d.forEach((t=>{"pending"===t.status&&(t.status="aborted")})),d=[]}function b(t,e){e&&(p=[]),"function"===typeof t&&p.push(t)}function m(){return{startTime:s,payload:e,status:l,queriesSent:f,queriesPending:d.length,subscribe:b,abort:g}}function y(){l="failed",p.forEach((t=>{t(void 0,a)}))}function v(){d.forEach((t=>{"pending"===t.status&&(t.status="aborted")})),d=[]}function x(e,n,o){const r="success"!==n;switch(d=d.filter((t=>t!==e)),l){case"pending":break;case"failed":if(r||!t.dataAfterTimeout)return;break;default:return}if("abort"===n)return a=o,void y();if(r)return a=o,void(d.length||(c.length?w():y()));if(h(),v(),!t.random){const n=t.resources.indexOf(e.resource);-1!==n&&n!==t.index&&(t.index=n)}l="completed",p.forEach((t=>{t(o)}))}function w(){if("pending"!==l)return;h();const o=c.shift();if(void 0===o)return d.length?void(u=setTimeout((()=>{h(),"pending"===l&&(v(),y())}),t.timeout)):void y();const r={status:"pending",resource:o,callback:(t,e)=>{x(r,t,e)}};d.push(r),f++,u=setTimeout(w,t.rotate),n(o,e,r.callback)}return"function"===typeof o&&p.push(o),setTimeout(w),m}function ut(t){const e={...lt,...t};let n=[];function o(){n=n.filter((t=>"pending"===t().status))}function r(t,r,i){const c=ft(e,t,r,((t,e)=>{o(),i&&i(t,e)}));return n.push(c),c}function i(t){return n.find((e=>t(e)))||null}const c={query:r,find:i,setIndex:t=>{e.index=t},getIndex:()=>e.index,cleanup:o};return c}function dt(){}const pt=Object.create(null);function ht(t){if(!pt[t]){const e=Z(t);if(!e)return;const n=ut(e),o={config:e,redundancy:n};pt[t]=o}return pt[t]}function gt(t,e,n){let o,r;if("string"===typeof t){const e=q(t);if(!e)return n(void 0,424),dt;r=e.send;const i=ht(t);i&&(o=i.redundancy)}else{const e=J(t);if(e){o=ut(e);const n=t.resources?t.resources[0]:"",i=q(n);i&&(r=i.send)}}return o&&r?o.query(e,r,n)().abort:(n(void 0,424),dt)}const bt="iconify2",mt="iconify",yt=mt+"-count",vt=mt+"-version",xt=36e5,wt=168;function jt(t,e){try{return t.getItem(e)}catch(n){}}function kt(t,e,n){try{return t.setItem(e,n),!0}catch(o){}}function St(t,e){try{t.removeItem(e)}catch(n){}}function Ot(t,e){return kt(t,yt,e.toString())}function It(t){return parseInt(jt(t,yt))||0}const Et={local:!0,session:!0},Mt={local:new Set,session:new Set};let Ft=!1;function Ct(t){Ft=t}let Lt="undefined"===typeof window?{}:window;function Tt(t){const e=t+"Storage";try{if(Lt&&Lt[e]&&"number"===typeof Lt[e].length)return Lt[e]}catch(n){}Et[t]=!1}function _t(t,e){const n=Tt(t);if(!n)return;const o=jt(n,vt);if(o!==bt){if(o){const t=It(n);for(let e=0;e<t;e++)St(n,mt+e.toString())}return kt(n,vt,bt),void Ot(n,0)}const r=Math.floor(Date.now()/xt)-wt,i=t=>{const o=mt+t.toString(),i=jt(n,o);if("string"===typeof i){try{const n=JSON.parse(i);if("object"===typeof n&&"number"===typeof n.cached&&n.cached>r&&"string"===typeof n.provider&&"object"===typeof n.data&&"string"===typeof n.data.prefix&&e(n,t))return!0}catch(c){}St(n,o)}};let c=It(n);for(let s=c-1;s>=0;s--)i(s)||(s===c-1?(c--,Ot(n,c)):Mt[t].add(s))}function zt(){if(!Ft){Ct(!0);for(const t in Et)_t(t,(t=>{const e=t.data,n=t.provider,o=e.prefix,r=w(n,o);if(!j(r,e).length)return!1;const i=e.lastModified||-1;return r.lastModifiedCached=r.lastModifiedCached?Math.min(r.lastModifiedCached,i):i,!0}))}}function At(t,e){const n=t.lastModifiedCached;if(n&&n>=e)return n===e;if(t.lastModifiedCached=e,n)for(const o in Et)_t(o,(n=>{const o=n.data;return n.provider!==t.provider||o.prefix!==t.prefix||o.lastModified===e}));return!0}function Nt(t,e){function n(n){let o;if(!Et[n]||!(o=Tt(n)))return;const r=Mt[n];let i;if(r.size)r.delete(i=Array.from(r).shift());else if(i=It(o),!Ot(o,i+1))return;const c={cached:Math.floor(Date.now()/xt),provider:t.provider,data:e};return kt(o,mt+i.toString(),JSON.stringify(c))}Ft||zt(),e.lastModified&&!At(t,e.lastModified)||Object.keys(e.icons).length&&(e.not_found&&(e=Object.assign({},e),delete e.not_found),n("local")||n("session"))}function Pt(){}function Rt(t){t.iconsLoaderFlag||(t.iconsLoaderFlag=!0,setTimeout((()=>{t.iconsLoaderFlag=!1,it(t)})))}function $t(t,e){t.iconsToLoad?t.iconsToLoad=t.iconsToLoad.concat(e).sort():t.iconsToLoad=e,t.iconsQueueFlag||(t.iconsQueueFlag=!0,setTimeout((()=>{t.iconsQueueFlag=!1;const{provider:e,prefix:n}=t,o=t.iconsToLoad;let r;if(delete t.iconsToLoad,!o||!(r=q(e)))return;const i=r.prepare(e,n,o);i.forEach((n=>{gt(e,n,(e=>{if("object"!==typeof e)n.icons.forEach((e=>{t.missing.add(e)}));else try{const n=j(t,e);if(!n.length)return;const o=t.pendingIcons;o&&n.forEach((t=>{o.delete(t)})),Nt(t,e)}catch(o){console.error(o)}Rt(t)}))}))})))}const Dt=(t,e)=>{const n=at(t,!0,O()),o=ot(n);if(!o.pending.length){let t=!0;return e&&setTimeout((()=>{t&&e(o.loaded,o.missing,o.pending,Pt)})),()=>{t=!1}}const r=Object.create(null),i=[];let c,s;return o.pending.forEach((t=>{const{provider:e,prefix:n}=t;if(n===s&&e===c)return;c=e,s=n,i.push(w(e,n));const o=r[e]||(r[e]=Object.create(null));o[n]||(o[n]=[])})),o.pending.forEach((t=>{const{provider:e,prefix:n,name:o}=t,i=w(e,n),c=i.pendingIcons||(i.pendingIcons=new Set);c.has(o)||(c.add(o),r[e][n].push(o))})),i.forEach((t=>{const{provider:e,prefix:n}=t;r[e][n].length&&$t(t,r[e][n])})),e?st(e,o,i):Pt};function Ut(t,e){const n={...t};for(const o in e){const t=e[o],r=typeof t;o in F?(null===t||t&&("string"===r||"number"===r))&&(n[o]=t):r===typeof n[o]&&(n[o]="rotate"===o?t%4:t)}return n}const qt=/[\s,]+/;function Jt(t,e){e.split(qt).forEach((e=>{const n=e.trim();switch(n){case"horizontal":t.hFlip=!0;break;case"vertical":t.vFlip=!0;break}}))}function Qt(t,e=0){const n=t.replace(/^-?[0-9.]*/,"");function o(t){while(t<0)t+=4;return t%4}if(""===n){const e=parseInt(t);return isNaN(e)?0:o(e)}if(n!==t){let e=0;switch(n){case"%":e=25;break;case"deg":e=90}if(e){let r=parseFloat(t.slice(0,t.length-n.length));return isNaN(r)?0:(r/=e,r%1===0?o(r):0)}}return e}function Ht(t,e){let n=-1===t.indexOf("xlink:")?"":' xmlns:xlink="http://www.w3.org/1999/xlink"';for(const o in e)n+=" "+o+'="'+e[o]+'"';return'<svg xmlns="http://www.w3.org/2000/svg"'+n+">"+t+"</svg>"}function Bt(t){return t.replace(/"/g,"'").replace(/%/g,"%25").replace(/#/g,"%23").replace(/</g,"%3C").replace(/>/g,"%3E").replace(/\s+/g," ")}function Vt(t){return"data:image/svg+xml,"+Bt(t)}function Zt(t){return'url("'+Vt(t)+'")'}const Gt={...C,inline:!1},Kt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink","aria-hidden":!0,role:"img"},Wt={display:"inline-block"},Xt={backgroundColor:"currentColor"},Yt={backgroundColor:"transparent"},te={Image:"var(--svg)",Repeat:"no-repeat",Size:"100% 100%"},ee={webkitMask:Xt,mask:Xt,background:Yt};for(const ae in ee){const t=ee[ae];for(const e in te)t[ae+e]=te[e]}const ne={};function oe(t){return t+(t.match(/^[-0-9.]+$/)?"px":"")}["horizontal","vertical"].forEach((t=>{const e=t.slice(0,1)+"Flip";ne[t+"-flip"]=e,ne[t.slice(0,1)+"-flip"]=e,ne[t+"Flip"]=e}));const re=(t,e)=>{const n=Ut(Gt,e),r={...Kt},i=e.mode||"svg",c={},s=e.style,a="object"!==typeof s||s instanceof Array?{}:s;for(let o in e){const t=e[o];if(void 0!==t)switch(o){case"icon":case"style":case"onLoad":case"mode":break;case"inline":case"hFlip":case"vFlip":n[o]=!0===t||"true"===t||1===t;break;case"flip":"string"===typeof t&&Jt(n,t);break;case"color":c.color=t;break;case"rotate":"string"===typeof t?n[o]=Qt(t):"number"===typeof t&&(n[o]=t);break;case"ariaHidden":case"aria-hidden":!0!==t&&"true"!==t&&delete r["aria-hidden"];break;default:{const e=ne[o];e?!0!==t&&"true"!==t&&1!==t||(n[e]=!0):void 0===Gt[o]&&(r[o]=t)}}}const l=A(t,n),f=l.attributes;if(n.inline&&(c.verticalAlign="-0.125em"),"svg"===i){r.style={...c,...a},Object.assign(r,f);let t=0,n=e.id;return"string"===typeof n&&(n=n.replace(/-/g,"_")),r["innerHTML"]=$(l.body,n?()=>n+"ID"+t++:"iconifyVue"),(0,o.h)("svg",r)}const{body:u,width:d,height:p}=t,h="mask"===i||"bg"!==i&&-1!==u.indexOf("currentColor"),g=Ht(u,{...f,width:d+"",height:p+""});return r.style={...c,"--svg":Zt(g),width:oe(f.width),height:oe(f.height),...Wt,...h?Xt:Yt,...a},(0,o.h)("span",r)};if(O(!0),U("",nt),"undefined"!==typeof document&&"undefined"!==typeof window){zt();const t=window;if(void 0!==t.IconifyPreload){const e=t.IconifyPreload,n="Invalid IconifyPreload syntax.";"object"===typeof e&&null!==e&&(e instanceof Array?e:[e]).forEach((t=>{try{("object"!==typeof t||null===t||t instanceof Array||"object"!==typeof t.icons||"string"!==typeof t.prefix||!M(t))&&console.error(n)}catch(e){console.error(n)}}))}if(void 0!==t.IconifyProviders){const e=t.IconifyProviders;if("object"===typeof e&&null!==e)for(let t in e){const n="IconifyProviders["+t+"] is invalid.";try{const o=e[t];if("object"!==typeof o||!o||void 0===o.resources)continue;V(t,o)||console.error(n)}catch(se){console.error(n)}}}}const ie={...l,body:""},ce=(0,o.aZ)({inheritAttrs:!1,data(){return{iconMounted:!1,counter:0}},mounted(){this._name="",this._loadingIcon=null,this.iconMounted=!0},unmounted(){this.abortLoading()},methods:{abortLoading(){this._loadingIcon&&(this._loadingIcon.abort(),this._loadingIcon=null)},getIcon(t,e){if("object"===typeof t&&null!==t&&"string"===typeof t.body)return this._name="",this.abortLoading(),{data:t};let n;if("string"!==typeof t||null===(n=i(t,!1,!0)))return this.abortLoading(),null;const o=I(n);if(!o)return this._loadingIcon&&this._loadingIcon.name===t||(this.abortLoading(),this._name="",null!==o&&(this._loadingIcon={name:t,abort:Dt([n],(()=>{this.counter++}))})),null;this.abortLoading(),this._name!==t&&(this._name=t,e&&e(t));const r=["iconify"];return""!==n.prefix&&r.push("iconify--"+n.prefix),""!==n.provider&&r.push("iconify--"+n.provider),{data:o,classes:r}}},render(){this.counter;const t=this.$attrs,e=this.iconMounted?this.getIcon(t.icon,t.onLoad):null;if(!e)return re(ie,t);let n=t;return e.classes&&(n={...t,class:("string"===typeof t["class"]?t["class"]+" ":"")+e.classes.join(" ")}),re({...l,...e.data},n)}})}}]);
//# sourceMappingURL=88.8d7d46eb.js.map