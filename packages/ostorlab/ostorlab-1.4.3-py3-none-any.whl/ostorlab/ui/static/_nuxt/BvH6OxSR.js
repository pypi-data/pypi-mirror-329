var a=Object.defineProperty;var s=(o,t,e)=>t in o?a(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e;var r=(o,t,e)=>s(o,typeof t!="symbol"?t+"":t,e);function d(o,...t){let e="",i;for(i=0;i<t.length;i++)e+=o[i]+t[i];return e+=o[i],e}const n="X-Api-Key";class h{constructor(t){r(this,"$axios");this.$axios=t}_createAuthorizationHeader(t){return{[n]:t.apiKey}}async post(t,e){if(t!=null)return await this.$axios.post(t.endpoint,e,{headers:this._createAuthorizationHeader(t)})}}export{h as R,d as g};
