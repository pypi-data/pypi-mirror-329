import{d as y,r as l,cd as x,u as h,o as v,t as o,v as b,z as t,Z as s,A as c,B as V,N as d}from"./Bl2PtCmi.js";import{_ as k}from"./BrqYU--B.js";import{u as S,b as w,a as C,V as B,D as N}from"./BMk0wala.js";import{V as g}from"./TgNZA6Y3.js";import"./D1jDBoMW.js";import"./DlAUqK2U.js";import"./BCYVl_Vs.js";const R=y({__name:"new",setup(K){const p=S(),u=l(!1),a=x(),i=h(),r=l({endpoint:"",apiKey:"",name:""});v(()=>{const e=a.query.endpoint,n=a.query.key,_=a.query.name||"Local scanner";e!=null&&n!==void 0&&n!==null?(r.value={endpoint:e.toString(),apiKey:n.toString(),name:_},u.value=!0):(p.reportError("Invalid scanner configuration."),i.push({path:"/scanners"}))});const m=[{text:"Scanners",disabled:!1,to:"/scanners",exact:!0},{text:"New",disabled:!0,to:"/scanners",exact:!0}];function f(){r.value={endpoint:"",apiKey:"",name:""},i.push({path:"/scanners"})}return(e,n)=>(o(),b("div",null,[t(s(N),{breadcrumbs:m,class:"mb-5"}),t(B,{variant:"outlined",class:"my-4"},{default:c(()=>[t(w,null,{default:c(()=>[V(" Add a new scanner ")]),_:1}),t(C,null,{default:c(()=>[s(u)===!0?(o(),d(k,{key:0,scanner:s(r),onCloseForm:f},null,8,["scanner"])):(o(),d(g,{key:1,type:"heading@3, button@2",width:"400px"}))]),_:1})]),_:1})]))}});export{R as default};
