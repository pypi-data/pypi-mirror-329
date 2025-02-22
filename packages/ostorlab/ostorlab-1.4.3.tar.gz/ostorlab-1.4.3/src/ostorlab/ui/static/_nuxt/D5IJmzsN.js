import{bB as xt,d as Pt,N as wt,A as O,t as kt,z as u,x as ee,W as te,B as E,y as N,Y as $e,U as A,C as It,D as Dt,r as W,bC as Vt,$ as T,b9 as X,bD as _t,aX as Ae,aA as Le,bb as Tt,be as Ct,bE as Bt,aB as Re,aZ as Oe,bf as Ft,a3 as M,a4 as z,aN as ae,bF as $t,a_ as Ne,bG as oe,bt as At,aG as ge,bH as Lt,j as I,bI as le,aE as _,a7 as q,ab as B,bJ as ke,aS as Ie,F as Ee,aV as Y,bK as Me,H as He,av as J,bz as ce,bL as Rt,aI as L,bM as Ot,bN as Nt,bO as Ge,aL as fe,bP as ne,bQ as be,bR as Et,bS as Mt,aD as Ht,bT as Gt,R as Q,aa as he,T as jt,bU as je,bV as ve,ad as De,aC as Wt,bW as re,bX as zt,bY as qt}from"./Bl2PtCmi.js";import{_ as Ut}from"./DlAUqK2U.js";import{a as Kt,V as We}from"./CvQdbTl1.js";import{a as Xt,V as Qt}from"./BMk0wala.js";function Ve(e,l,a){return Object.keys(e).filter(t=>xt(t)&&t.endsWith(l)).reduce((t,n)=>(t[n.slice(0,-l.length)]=r=>e[n](r,a(r)),t),{})}const Yt=Pt({name:"DfConfirmationModal",props:{modelValue:{type:Boolean},title:{type:String,default:null},cardIcon:{type:String,default:"mdi-information"},description:{type:String,default:null},cancelButtonText:{type:String,default:"Add"},cancelIcon:{type:String,default:"mdi-lock"},confirmButtonText:{type:String,default:"Proceed"},confirmButtonColor:{type:String,default:"success"},confirmIcon:{type:String,default:"mdi-arrow-right"}},emits:["cancel","confirm","update:modelValue"],data(){return{toggleDialog:!1,dontShowWarning:!1}},watch:{modelValue(e){this.toggleDialog=e},toggleDialog(e){this.$emit("update:modelValue",e)}},mounted(){this.toggleDialog=this.modelValue},methods:{confirm(){this.toggleDialog=!1,this.$emit("confirm")},cancel(){this.toggleDialog=!1,this.$emit("cancel")}}}),Jt=e=>(It("data-v-d8b4c0e7"),e=e(),Dt(),e),Zt={class:"d-flex flex-column align-center px-4 py-6"},ea={class:"icon-container mb-4"},ta=Jt(()=>ee("div",{class:"icon-background"},null,-1)),aa={class:"text-center mb-0 font-weight-bold"},la={class:"d-flex justify-space-around py-3"};function na(e,l,a,t,n,r){return kt(),wt(Kt,{modelValue:e.toggleDialog,"onUpdate:modelValue":l[0]||(l[0]=o=>e.toggleDialog=o),"max-width":"400"},{default:O(()=>[u(Qt,null,{default:O(()=>[ee("div",Zt,[ee("div",ea,[ta,u(te,{class:"icon-position",size:30},{default:O(()=>[E(N(e.cardIcon),1)]),_:1})]),ee("p",aa,N(e.title),1),u(Xt,{class:"text-center pb-0 pt-2"},{default:O(()=>[E(N(e.description),1)]),_:1})]),u($e),ee("div",la,[u(A,{style:{width:"47%"},onClick:e.cancel},{default:O(()=>[u(te,{dark:"",start:""},{default:O(()=>[E(N(e.cancelIcon),1)]),_:1}),E(" "+N(e.cancelButtonText),1)]),_:1},8,["onClick"]),u(A,{color:e.confirmButtonColor,style:{width:"47%"},onClick:e.confirm},{default:O(()=>[u(te,{start:""},{default:O(()=>[E(N(e.confirmIcon),1)]),_:1}),E(" "+N(e.confirmButtonText),1)]),_:1},8,["color","onClick"])])]),_:1})]),_:1},8,["modelValue"])}const Xa=Ut(Yt,[["render",na],["__scopeId","data-v-d8b4c0e7"]]);function ra(){const e=W([]);Vt(()=>e.value=[]);function l(a,t){e.value[t]=a}return{refs:e,updateRef:l}}const sa=T({activeColor:String,start:{type:[Number,String],default:1},modelValue:{type:Number,default:e=>e.start},disabled:Boolean,length:{type:[Number,String],default:1,validator:e=>e%1===0},totalVisible:[Number,String],firstIcon:{type:X,default:"$first"},prevIcon:{type:X,default:"$prev"},nextIcon:{type:X,default:"$next"},lastIcon:{type:X,default:"$last"},ariaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.root"},pageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.page"},currentPageAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.currentPage"},firstAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.first"},previousAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.previous"},nextAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.next"},lastAriaLabel:{type:String,default:"$vuetify.pagination.ariaLabel.last"},ellipsis:{type:String,default:"..."},showFirstLastPage:Boolean,..._t(),...Ae(),...Le(),...Tt(),...Ct(),...Bt(),...Re({tag:"nav"}),...Oe(),...Ft({variant:"text"})},"VPagination"),_e=M()({name:"VPagination",props:sa(),emits:{"update:modelValue":e=>!0,first:e=>!0,prev:e=>!0,next:e=>!0,last:e=>!0},setup(e,l){let{slots:a,emit:t}=l;const n=z(e,"modelValue"),{t:r,n:o}=ae(),{isRtl:s}=$t(),{themeClasses:c}=Ne(e),{width:i}=oe(),m=At(-1);ge(void 0,{scoped:!0});const{resizeRef:p}=Lt(b=>{if(!b.length)return;const{target:d,contentRect:w}=b[0],P=d.querySelector(".v-pagination__list > *");if(!P)return;const D=w.width,C=P.offsetWidth+parseFloat(getComputedStyle(P).marginRight)*2;m.value=x(D,C)}),v=I(()=>parseInt(e.length,10)),S=I(()=>parseInt(e.start,10)),h=I(()=>e.totalVisible!=null?parseInt(e.totalVisible,10):m.value>=0?m.value:x(i.value,58));function x(b,d){const w=e.showFirstLastPage?5:3;return Math.max(0,Math.floor(+((b-d*w)/d).toFixed(2)))}const g=I(()=>{if(v.value<=0||isNaN(v.value)||v.value>Number.MAX_SAFE_INTEGER)return[];if(h.value<=0)return[];if(h.value===1)return[n.value];if(v.value<=h.value)return le(v.value,S.value);const b=h.value%2===0,d=b?h.value/2:Math.floor(h.value/2),w=b?d:d+1,P=v.value-d;if(w-n.value>=0)return[...le(Math.max(1,h.value-1),S.value),e.ellipsis,v.value];if(n.value-P>=(b?1:0)){const D=h.value-1,C=v.value-D+S.value;return[S.value,e.ellipsis,...le(D,C)]}else{const D=Math.max(1,h.value-3),C=D===1?n.value:n.value-Math.ceil(D/2)+S.value;return[S.value,e.ellipsis,...le(D,C),e.ellipsis,v.value]}});function y(b,d,w){b.preventDefault(),n.value=d,w&&t(w,d)}const{refs:f,updateRef:V}=ra();ge({VPaginationBtn:{color:_(e,"color"),border:_(e,"border"),density:_(e,"density"),size:_(e,"size"),variant:_(e,"variant"),rounded:_(e,"rounded"),elevation:_(e,"elevation")}});const F=I(()=>g.value.map((b,d)=>{const w=P=>V(P,d);if(typeof b=="string")return{isActive:!1,key:`ellipsis-${d}`,page:b,props:{ref:w,ellipsis:!0,icon:!0,disabled:!0}};{const P=b===n.value;return{isActive:P,key:b,page:o(b),props:{ref:w,ellipsis:!1,icon:!0,disabled:!!e.disabled||+e.length<2,color:P?e.activeColor:e.color,"aria-current":P,"aria-label":r(P?e.currentPageAriaLabel:e.pageAriaLabel,b),onClick:D=>y(D,b)}}}})),k=I(()=>{const b=!!e.disabled||n.value<=S.value,d=!!e.disabled||n.value>=S.value+v.value-1;return{first:e.showFirstLastPage?{icon:s.value?e.lastIcon:e.firstIcon,onClick:w=>y(w,S.value,"first"),disabled:b,"aria-label":r(e.firstAriaLabel),"aria-disabled":b}:void 0,prev:{icon:s.value?e.nextIcon:e.prevIcon,onClick:w=>y(w,n.value-1,"prev"),disabled:b,"aria-label":r(e.previousAriaLabel),"aria-disabled":b},next:{icon:s.value?e.prevIcon:e.nextIcon,onClick:w=>y(w,n.value+1,"next"),disabled:d,"aria-label":r(e.nextAriaLabel),"aria-disabled":d},last:e.showFirstLastPage?{icon:s.value?e.firstIcon:e.lastIcon,onClick:w=>y(w,S.value+v.value-1,"last"),disabled:d,"aria-label":r(e.lastAriaLabel),"aria-disabled":d}:void 0}});function R(){var d;const b=n.value-S.value;(d=f.value[b])==null||d.$el.focus()}function H(b){b.key===ke.left&&!e.disabled&&n.value>+e.start?(n.value=n.value-1,Ie(R)):b.key===ke.right&&!e.disabled&&n.value<S.value+v.value-1&&(n.value=n.value+1,Ie(R))}return q(()=>u(e.tag,{ref:p,class:["v-pagination",c.value,e.class],style:e.style,role:"navigation","aria-label":r(e.ariaLabel),onKeydown:H,"data-test":"v-pagination-root"},{default:()=>[u("ul",{class:"v-pagination__list"},[e.showFirstLastPage&&u("li",{key:"first",class:"v-pagination__first","data-test":"v-pagination-first"},[a.first?a.first(k.value.first):u(A,B({_as:"VPaginationBtn"},k.value.first),null)]),u("li",{key:"prev",class:"v-pagination__prev","data-test":"v-pagination-prev"},[a.prev?a.prev(k.value.prev):u(A,B({_as:"VPaginationBtn"},k.value.prev),null)]),F.value.map((b,d)=>u("li",{key:b.key,class:["v-pagination__item",{"v-pagination__item--is-active":b.isActive}],"data-test":"v-pagination-item"},[a.item?a.item(b):u(A,B({_as:"VPaginationBtn"},b.props),{default:()=>[b.page]})])),u("li",{key:"next",class:"v-pagination__next","data-test":"v-pagination-next"},[a.next?a.next(k.value.next):u(A,B({_as:"VPaginationBtn"},k.value.next),null)]),e.showFirstLastPage&&u("li",{key:"last",class:"v-pagination__last","data-test":"v-pagination-last"},[a.last?a.last(k.value.last):u(A,B({_as:"VPaginationBtn"},k.value.last),null)])])]})),{}}}),oa=T({page:{type:[Number,String],default:1},itemsPerPage:{type:[Number,String],default:10}},"DataTable-paginate"),ze=Symbol.for("vuetify:data-table-pagination");function ua(e){const l=z(e,"page",void 0,t=>+(t??1)),a=z(e,"itemsPerPage",void 0,t=>+(t??10));return{page:l,itemsPerPage:a}}function ia(e){const{page:l,itemsPerPage:a,itemsLength:t}=e,n=I(()=>a.value===-1?0:a.value*(l.value-1)),r=I(()=>a.value===-1?t.value:Math.min(t.value,n.value+a.value)),o=I(()=>a.value===-1||t.value===0?1:Math.ceil(t.value/a.value));Ee(()=>{l.value>o.value&&(l.value=o.value)});function s(v){a.value=v,l.value=1}function c(){l.value=ce(l.value+1,1,o.value)}function i(){l.value=ce(l.value-1,1,o.value)}function m(v){l.value=ce(v,1,o.value)}const p={page:l,itemsPerPage:a,startIndex:n,stopIndex:r,pageCount:o,itemsLength:t,nextPage:c,prevPage:i,setPage:m,setItemsPerPage:s};return Y(ze,p),p}function da(){const e=J(ze);if(!e)throw new Error("Missing pagination!");return e}function ca(e){const l=Me("usePaginatedItems"),{items:a,startIndex:t,stopIndex:n,itemsPerPage:r}=e,o=I(()=>r.value<=0?a.value:a.value.slice(t.value,n.value));return He(o,s=>{l.emit("update:currentItems",s)}),{paginatedItems:o}}const qe=T({prevIcon:{type:String,default:"$prev"},nextIcon:{type:String,default:"$next"},firstIcon:{type:String,default:"$first"},lastIcon:{type:String,default:"$last"},itemsPerPageText:{type:String,default:"$vuetify.dataFooter.itemsPerPageText"},pageText:{type:String,default:"$vuetify.dataFooter.pageText"},firstPageLabel:{type:String,default:"$vuetify.dataFooter.firstPage"},prevPageLabel:{type:String,default:"$vuetify.dataFooter.prevPage"},nextPageLabel:{type:String,default:"$vuetify.dataFooter.nextPage"},lastPageLabel:{type:String,default:"$vuetify.dataFooter.lastPage"},itemsPerPageOptions:{type:Array,default:()=>[{value:10,title:"10"},{value:25,title:"25"},{value:50,title:"50"},{value:100,title:"100"},{value:-1,title:"$vuetify.dataFooter.itemsPerPageAll"}]},showCurrentPage:Boolean},"VDataTableFooter"),Te=M()({name:"VDataTableFooter",props:qe(),setup(e,l){let{slots:a}=l;const{t}=ae(),{page:n,pageCount:r,startIndex:o,stopIndex:s,itemsLength:c,itemsPerPage:i,setItemsPerPage:m}=da(),p=I(()=>e.itemsPerPageOptions.map(v=>typeof v=="number"?{value:v,title:v===-1?t("$vuetify.dataFooter.itemsPerPageAll"):String(v)}:{...v,title:isNaN(Number(v.title))?t(v.title):v.title}));return q(()=>{var S;const v=_e.filterProps(e);return u("div",{class:"v-data-table-footer"},[(S=a.prepend)==null?void 0:S.call(a),u("div",{class:"v-data-table-footer__items-per-page"},[u("span",null,[t(e.itemsPerPageText)]),u(We,{items:p.value,modelValue:i.value,"onUpdate:modelValue":h=>m(Number(h)),density:"compact",variant:"outlined","hide-details":!0},null)]),u("div",{class:"v-data-table-footer__info"},[u("div",null,[t(e.pageText,c.value?o.value+1:0,s.value,c.value)])]),u("div",{class:"v-data-table-footer__pagination"},[u(_e,B({modelValue:n.value,"onUpdate:modelValue":h=>n.value=h,density:"comfortable","first-aria-label":e.firstPageLabel,"last-aria-label":e.lastPageLabel,length:r.value,"next-aria-label":e.nextPageLabel,"previous-aria-label":e.prevPageLabel,rounded:!0,"show-first-last-page":!0,"total-visible":e.showCurrentPage?1:0,variant:"plain"},v),null)])])}),{}}}),se=Rt({align:{type:String,default:"start"},fixed:Boolean,fixedOffset:[Number,String],height:[Number,String],lastFixed:Boolean,noPadding:Boolean,tag:String,width:[Number,String],maxWidth:[Number,String],nowrap:Boolean},(e,l)=>{let{slots:a}=l;const t=e.tag??"td";return u(t,{class:["v-data-table__td",{"v-data-table-column--fixed":e.fixed,"v-data-table-column--last-fixed":e.lastFixed,"v-data-table-column--no-padding":e.noPadding,"v-data-table-column--nowrap":e.nowrap},`v-data-table-column--align-${e.align}`],style:{height:L(e.height),width:L(e.width),maxWidth:L(e.maxWidth),left:L(e.fixedOffset||null)}},{default:()=>{var n;return[(n=a.default)==null?void 0:n.call(a)]}})}),fa=T({headers:Array},"DataTable-header"),Ue=Symbol.for("vuetify:data-table-headers"),Ke={title:"",sortable:!1},va={...Ke,width:48};function ga(){const l=(arguments.length>0&&arguments[0]!==void 0?arguments[0]:[]).map(a=>({element:a,priority:0}));return{enqueue:(a,t)=>{let n=!1;for(let r=0;r<l.length;r++)if(l[r].priority>t){l.splice(r,0,{element:a,priority:t}),n=!0;break}n||l.push({element:a,priority:t})},size:()=>l.length,count:()=>{let a=0;if(!l.length)return 0;const t=Math.floor(l[0].priority);for(let n=0;n<l.length;n++)Math.floor(l[n].priority)===t&&(a+=1);return a},dequeue:()=>l.shift()}}function me(e){let l=arguments.length>1&&arguments[1]!==void 0?arguments[1]:[];if(!e.children)l.push(e);else for(const a of e.children)me(a,l);return l}function Xe(e){let l=arguments.length>1&&arguments[1]!==void 0?arguments[1]:new Set;for(const a of e)a.key&&l.add(a.key),a.children&&Xe(a.children,l);return l}function ma(e){if(e.key){if(e.key==="data-table-group")return Ke;if(["data-table-expand","data-table-select"].includes(e.key))return va}}function ye(e){let l=arguments.length>1&&arguments[1]!==void 0?arguments[1]:0;return e.children?Math.max(l,...e.children.map(a=>ye(a,l+1))):l}function ba(e){let l=!1;function a(r){let o=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1;if(r)if(o&&(r.fixed=!0),r.fixed)if(r.children)for(let s=r.children.length-1;s>=0;s--)a(r.children[s],!0);else l?isNaN(+r.width)&&Nt(`Multiple fixed columns should have a static width (key: ${r.key})`):r.lastFixed=!0,l=!0;else if(r.children)for(let s=r.children.length-1;s>=0;s--)a(r.children[s]);else l=!1}for(let r=e.length-1;r>=0;r--)a(e[r]);function t(r){let o=arguments.length>1&&arguments[1]!==void 0?arguments[1]:0;if(!r)return o;if(r.children){r.fixedOffset=o;for(const s of r.children)o=t(s,o)}else r.fixed&&(r.fixedOffset=o,o+=parseFloat(r.width||"0")||0);return o}let n=0;for(const r of e)n=t(r,n)}function ha(e,l){const a=[];let t=0;const n=ga(e);for(;n.size()>0;){let o=n.count();const s=[];let c=1;for(;o>0;){const{element:i,priority:m}=n.dequeue(),p=l-t-ye(i);if(s.push({...i,rowspan:p??1,colspan:i.children?me(i).length:1}),i.children)for(const v of i.children){const S=m%1+c/Math.pow(10,t+2);n.enqueue(v,t+p+S)}c+=1,o-=1}t+=1,a.push(s)}return{columns:e.map(o=>me(o)).flat(),headers:a}}function Qe(e){const l=[];for(const a of e){const t={...ma(a),...a},n=t.key??(typeof t.value=="string"?t.value:null),r=t.value??n??null,o={...t,key:n,value:r,sortable:t.sortable??(t.key!=null||!!t.sort),children:t.children?Qe(t.children):void 0};l.push(o)}return l}function ya(e,l){const a=W([]),t=W([]),n=W({}),r=W({}),o=W({});Ee(()=>{var x,g,y;const i=(e.headers||Object.keys(e.items[0]??{}).map(f=>({key:f,title:Ot(f)}))).slice(),m=Xe(i);(x=l==null?void 0:l.groupBy)!=null&&x.value.length&&!m.has("data-table-group")&&i.unshift({key:"data-table-group",title:"Group"}),(g=l==null?void 0:l.showSelect)!=null&&g.value&&!m.has("data-table-select")&&i.unshift({key:"data-table-select"}),(y=l==null?void 0:l.showExpand)!=null&&y.value&&!m.has("data-table-expand")&&i.push({key:"data-table-expand"});const p=Qe(i);ba(p);const v=Math.max(...p.map(f=>ye(f)))+1,S=ha(p,v);a.value=S.headers,t.value=S.columns;const h=S.headers.flat(1);for(const f of h)f.key&&(f.sortable&&(f.sort&&(n.value[f.key]=f.sort),f.sortRaw&&(r.value[f.key]=f.sortRaw)),f.filter&&(o.value[f.key]=f.filter))});const s={headers:a,columns:t,sortFunctions:n,sortRawFunctions:r,filterFunctions:o};return Y(Ue,s),s}function ue(){const e=J(Ue);if(!e)throw new Error("Missing headers!");return e}const pa={showSelectAll:!1,allSelected:()=>[],select:e=>{var t;let{items:l,value:a}=e;return new Set(a?[(t=l[0])==null?void 0:t.value]:[])},selectAll:e=>{let{selected:l}=e;return l}},Ye={showSelectAll:!0,allSelected:e=>{let{currentPage:l}=e;return l},select:e=>{let{items:l,value:a,selected:t}=e;for(const n of l)a?t.add(n.value):t.delete(n.value);return t},selectAll:e=>{let{value:l,currentPage:a,selected:t}=e;return Ye.select({items:a,value:l,selected:t})}},Je={showSelectAll:!0,allSelected:e=>{let{allItems:l}=e;return l},select:e=>{let{items:l,value:a,selected:t}=e;for(const n of l)a?t.add(n.value):t.delete(n.value);return t},selectAll:e=>{let{value:l,allItems:a,selected:t}=e;return Je.select({items:a,value:l,selected:t})}},Sa=T({showSelect:Boolean,selectStrategy:{type:[String,Object],default:"page"},modelValue:{type:Array,default:()=>[]},valueComparator:{type:Function,default:Ge}},"DataTable-select"),Ze=Symbol.for("vuetify:data-table-selection");function xa(e,l){let{allItems:a,currentPage:t}=l;const n=z(e,"modelValue",e.modelValue,y=>new Set(fe(y).map(f=>{var V;return((V=a.value.find(F=>e.valueComparator(f,F.value)))==null?void 0:V.value)??f})),y=>[...y.values()]),r=I(()=>a.value.filter(y=>y.selectable)),o=I(()=>t.value.filter(y=>y.selectable)),s=I(()=>{if(typeof e.selectStrategy=="object")return e.selectStrategy;switch(e.selectStrategy){case"single":return pa;case"all":return Je;case"page":default:return Ye}});function c(y){return fe(y).every(f=>n.value.has(f.value))}function i(y){return fe(y).some(f=>n.value.has(f.value))}function m(y,f){const V=s.value.select({items:y,value:f,selected:new Set(n.value)});n.value=V}function p(y){m([y],!c([y]))}function v(y){const f=s.value.selectAll({value:y,allItems:r.value,currentPage:o.value,selected:new Set(n.value)});n.value=f}const S=I(()=>n.value.size>0),h=I(()=>{const y=s.value.allSelected({allItems:r.value,currentPage:o.value});return!!y.length&&c(y)}),x=I(()=>s.value.showSelectAll),g={toggleSelect:p,select:m,selectAll:v,isSelected:c,isSomeSelected:i,someSelected:S,allSelected:h,showSelectAll:x};return Y(Ze,g),g}function ie(){const e=J(Ze);if(!e)throw new Error("Missing selection!");return e}const Pa=T({sortBy:{type:Array,default:()=>[]},customKeySort:Object,multiSort:Boolean,mustSort:Boolean},"DataTable-sort"),et=Symbol.for("vuetify:data-table-sort");function wa(e){const l=z(e,"sortBy"),a=_(e,"mustSort"),t=_(e,"multiSort");return{sortBy:l,mustSort:a,multiSort:t}}function ka(e){const{sortBy:l,mustSort:a,multiSort:t,page:n}=e,r=c=>{if(c.key==null)return;let i=l.value.map(p=>({...p}))??[];const m=i.find(p=>p.key===c.key);m?m.order==="desc"?a.value?m.order="asc":i=i.filter(p=>p.key!==c.key):m.order="desc":t.value?i=[...i,{key:c.key,order:"asc"}]:i=[{key:c.key,order:"asc"}],l.value=i,n&&(n.value=1)};function o(c){return!!l.value.find(i=>i.key===c.key)}const s={sortBy:l,toggleSort:r,isSorted:o};return Y(et,s),s}function tt(){const e=J(et);if(!e)throw new Error("Missing sort!");return e}function Ia(e,l,a,t){const n=ae();return{sortedItems:I(()=>{var o,s;return!a.value.length||e.disableSort?l.value:Da(l.value,a.value,n.current.value,{transform:t==null?void 0:t.transform,sortFunctions:{...e.customKeySort,...(o=t==null?void 0:t.sortFunctions)==null?void 0:o.value},sortRawFunctions:(s=t==null?void 0:t.sortRawFunctions)==null?void 0:s.value})})}}function Da(e,l,a,t){const n=new Intl.Collator(a,{sensitivity:"accent",usage:"sort"});return e.map(o=>[o,t!=null&&t.transform?t.transform(o):o]).sort((o,s)=>{var c,i;for(let m=0;m<l.length;m++){let p=!1;const v=l[m].key,S=l[m].order??"asc";if(S===!1)continue;let h=o[1][v],x=s[1][v],g=o[0].raw,y=s[0].raw;if(S==="desc"&&([h,x]=[x,h],[g,y]=[y,g]),(c=t==null?void 0:t.sortRawFunctions)!=null&&c[v]){const f=t.sortRawFunctions[v](g,y);if(f==null)continue;if(p=!0,f)return f}if((i=t==null?void 0:t.sortFunctions)!=null&&i[v]){const f=t.sortFunctions[v](h,x);if(f==null)continue;if(p=!0,f)return f}if(!p){if(h instanceof Date&&x instanceof Date)return h.getTime()-x.getTime();if([h,x]=[h,x].map(f=>f!=null?f.toString().toLocaleLowerCase():f),h!==x)return ne(h)&&ne(x)?0:ne(h)?-1:ne(x)?1:!isNaN(h)&&!isNaN(x)?Number(h)-Number(x):n.compare(h,x)}}return 0}).map(o=>{let[s]=o;return s})}const at=T({color:String,sticky:Boolean,disableSort:Boolean,multiSort:Boolean,sortAscIcon:{type:X,default:"$sortAsc"},sortDescIcon:{type:X,default:"$sortDesc"},headerProps:{type:Object},...be(),...Et()},"VDataTableHeaders"),Ce=M()({name:"VDataTableHeaders",props:at(),setup(e,l){let{slots:a}=l;const{t}=ae(),{toggleSort:n,sortBy:r,isSorted:o}=tt(),{someSelected:s,allSelected:c,selectAll:i,showSelectAll:m}=ie(),{columns:p,headers:v}=ue(),{loaderClasses:S}=Mt(e);function h(b,d){if(!(!e.sticky&&!b.fixed))return{position:"sticky",left:b.fixed?L(b.fixedOffset):void 0,top:e.sticky?`calc(var(--v-table-header-height) * ${d})`:void 0}}function x(b){const d=r.value.find(w=>w.key===b.key);return d?d.order==="asc"?e.sortAscIcon:e.sortDescIcon:e.sortAscIcon}const{backgroundColorClasses:g,backgroundColorStyles:y}=Ht(e,"color"),{displayClasses:f,mobile:V}=oe(e),F=I(()=>({headers:v.value,columns:p.value,toggleSort:n,isSorted:o,sortBy:r.value,someSelected:s.value,allSelected:c.value,selectAll:i,getSortIcon:x})),k=I(()=>["v-data-table__th",{"v-data-table__th--sticky":e.sticky},f.value,S.value]),R=b=>{let{column:d,x:w,y:P}=b;const D=d.key==="data-table-select"||d.key==="data-table-expand",C=B(e.headerProps??{},d.headerProps??{});return u(se,B({tag:"th",align:d.align,class:[{"v-data-table__th--sortable":d.sortable&&!e.disableSort,"v-data-table__th--sorted":o(d),"v-data-table__th--fixed":d.fixed},...k.value],style:{width:L(d.width),minWidth:L(d.minWidth),maxWidth:L(d.maxWidth),...h(d,P)},colspan:d.colspan,rowspan:d.rowspan,onClick:d.sortable?()=>n(d):void 0,fixed:d.fixed,nowrap:d.nowrap,lastFixed:d.lastFixed,noPadding:D},C),{default:()=>{var K;const G=`header.${d.key}`,U={column:d,selectAll:i,isSorted:o,toggleSort:n,sortBy:r.value,someSelected:s.value,allSelected:c.value,getSortIcon:x};return a[G]?a[G](U):d.key==="data-table-select"?((K=a["header.data-table-select"])==null?void 0:K.call(a,U))??(m.value&&u(he,{modelValue:c.value,indeterminate:s.value&&!c.value,"onUpdate:modelValue":i},null)):u("div",{class:"v-data-table-header__content"},[u("span",null,[d.title]),d.sortable&&!e.disableSort&&u(te,{key:"icon",class:"v-data-table-header__sort-icon",icon:x(d)},null),e.multiSort&&o(d)&&u("div",{key:"badge",class:["v-data-table-header__sort-badge",...g.value],style:y.value},[r.value.findIndex(de=>de.key===d.key)+1])])}})},H=()=>{const b=B(e.headerProps??{}??{}),d=I(()=>p.value.filter(P=>(P==null?void 0:P.sortable)&&!e.disableSort)),w=I(()=>{if(p.value.find(D=>D.key==="data-table-select")!=null)return c.value?"$checkboxOn":s.value?"$checkboxIndeterminate":"$checkboxOff"});return u(se,B({tag:"th",class:[...k.value],colspan:v.value.length+1},b),{default:()=>[u("div",{class:"v-data-table-header__content"},[u(We,{chips:!0,class:"v-data-table__td-sort-select",clearable:!0,density:"default",items:d.value,label:t("$vuetify.dataTable.sortBy"),multiple:e.multiSort,variant:"underlined","onClick:clear":()=>r.value=[],appendIcon:w.value,"onClick:append":()=>i(!c.value)},{...a,chip:P=>{var D;return u(jt,{onClick:(D=P.item.raw)!=null&&D.sortable?()=>n(P.item.raw):void 0,onMousedown:C=>{C.preventDefault(),C.stopPropagation()}},{default:()=>[P.item.title,u(te,{class:["v-data-table__td-sort-icon",o(P.item.raw)&&"v-data-table__td-sort-icon-active"],icon:x(P.item.raw),size:"small"},null)]})}})])]})};q(()=>V.value?u("tr",null,[u(H,null,null)]):u(Q,null,[a.headers?a.headers(F.value):v.value.map((b,d)=>u("tr",null,[b.map((w,P)=>u(R,{column:w,x:P,y:d},null))])),e.loading&&u("tr",{class:"v-data-table-progress"},[u("th",{colspan:p.value.length},[u(Gt,{name:"v-data-table-progress",absolute:!0,active:!0,color:typeof e.loading=="boolean"?void 0:e.loading,indeterminate:!0},{default:a.loader})])])]))}}),Va=T({groupBy:{type:Array,default:()=>[]}},"DataTable-group"),lt=Symbol.for("vuetify:data-table-group");function _a(e){return{groupBy:z(e,"groupBy")}}function Ta(e){const{groupBy:l,sortBy:a}=e,t=W(new Set),n=I(()=>l.value.map(i=>({...i,order:i.order??!1})).concat(a.value));function r(i){return t.value.has(i.id)}function o(i){const m=new Set(t.value);r(i)?m.delete(i.id):m.add(i.id),t.value=m}function s(i){function m(p){const v=[];for(const S of p.items)"type"in S&&S.type==="group"?v.push(...m(S)):v.push(S);return v}return m({type:"group",items:i,id:"dummy",key:"dummy",value:"dummy",depth:0})}const c={sortByWithGroups:n,toggleGroup:o,opened:t,groupBy:l,extractRows:s,isGroupOpen:r};return Y(lt,c),c}function nt(){const e=J(lt);if(!e)throw new Error("Missing group!");return e}function Ca(e,l){if(!e.length)return[];const a=new Map;for(const t of e){const n=je(t.raw,l);a.has(n)||a.set(n,[]),a.get(n).push(t)}return a}function rt(e,l){let a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:0,t=arguments.length>3&&arguments[3]!==void 0?arguments[3]:"root";if(!l.length)return[];const n=Ca(e,l[0]),r=[],o=l.slice(1);return n.forEach((s,c)=>{const i=l[0],m=`${t}_${i}_${c}`;r.push({depth:a,id:m,key:i,value:c,items:o.length?rt(s,o,a+1,m):s,type:"group"})}),r}function st(e,l){const a=[];for(const t of e)"type"in t&&t.type==="group"?(t.value!=null&&a.push(t),(l.has(t.id)||t.value==null)&&a.push(...st(t.items,l))):a.push(t);return a}function Ba(e,l,a){return{flatItems:I(()=>{if(!l.value.length)return e.value;const n=rt(e.value,l.value.map(r=>r.key));return st(n,a.value)})}}const Fa=T({item:{type:Object,required:!0}},"VDataTableGroupHeaderRow"),$a=M()({name:"VDataTableGroupHeaderRow",props:Fa(),setup(e,l){let{slots:a}=l;const{isGroupOpen:t,toggleGroup:n,extractRows:r}=nt(),{isSelected:o,isSomeSelected:s,select:c}=ie(),{columns:i}=ue(),m=I(()=>r([e.item]));return()=>u("tr",{class:"v-data-table-group-header-row",style:{"--v-data-table-group-header-row-depth":e.item.depth}},[i.value.map(p=>{var v,S;if(p.key==="data-table-group"){const h=t(e.item)?"$expand":"$next",x=()=>n(e.item);return((v=a["data-table-group"])==null?void 0:v.call(a,{item:e.item,count:m.value.length,props:{icon:h,onClick:x}}))??u(se,{class:"v-data-table-group-header-row__column"},{default:()=>[u(A,{size:"small",variant:"text",icon:h,onClick:x},null),u("span",null,[e.item.value]),u("span",null,[E("("),m.value.length,E(")")])]})}if(p.key==="data-table-select"){const h=o(m.value),x=s(m.value)&&!h,g=y=>c(m.value,y);return((S=a["data-table-select"])==null?void 0:S.call(a,{props:{modelValue:h,indeterminate:x,"onUpdate:modelValue":g}}))??u("td",null,[u(he,{modelValue:h,indeterminate:x,"onUpdate:modelValue":g},null)])}return u("td",null,null)})])}}),Aa=T({expandOnClick:Boolean,showExpand:Boolean,expanded:{type:Array,default:()=>[]}},"DataTable-expand"),ot=Symbol.for("vuetify:datatable:expanded");function La(e){const l=_(e,"expandOnClick"),a=z(e,"expanded",e.expanded,s=>new Set(s),s=>[...s.values()]);function t(s,c){const i=new Set(a.value);c?i.add(s.value):i.delete(s.value),a.value=i}function n(s){return a.value.has(s.value)}function r(s){t(s,!n(s))}const o={expand:t,expanded:a,expandOnClick:l,isExpanded:n,toggleExpand:r};return Y(ot,o),o}function ut(){const e=J(ot);if(!e)throw new Error("foo");return e}const Ra=T({index:Number,item:Object,cellProps:[Object,Function],onClick:ve(),onContextmenu:ve(),onDblclick:ve(),...be()},"VDataTableRow"),Oa=M()({name:"VDataTableRow",props:Ra(),setup(e,l){let{slots:a}=l;const{displayClasses:t,mobile:n}=oe(e,"v-data-table__tr"),{isSelected:r,toggleSelect:o,someSelected:s,allSelected:c,selectAll:i}=ie(),{isExpanded:m,toggleExpand:p}=ut(),{toggleSort:v,sortBy:S,isSorted:h}=tt(),{columns:x}=ue();q(()=>u("tr",{class:["v-data-table__tr",{"v-data-table__tr--clickable":!!(e.onClick||e.onContextmenu||e.onDblclick)},t.value],onClick:e.onClick,onContextmenu:e.onContextmenu,onDblclick:e.onDblclick},[e.item&&x.value.map((g,y)=>{const f=e.item,V=`item.${g.key}`,F=`header.${g.key}`,k={index:e.index,item:f.raw,internalItem:f,value:je(f.columns,g.key),column:g,isSelected:r,toggleSelect:o,isExpanded:m,toggleExpand:p},R={column:g,selectAll:i,isSorted:h,toggleSort:v,sortBy:S.value,someSelected:s.value,allSelected:c.value,getSortIcon:()=>""},H=typeof e.cellProps=="function"?e.cellProps({index:k.index,item:k.item,internalItem:k.internalItem,value:k.value,column:g}):e.cellProps,b=typeof g.cellProps=="function"?g.cellProps({index:k.index,item:k.item,internalItem:k.internalItem,value:k.value}):g.cellProps;return u(se,B({align:g.align,class:{"v-data-table__td--expanded-row":g.key==="data-table-expand","v-data-table__td--select-row":g.key==="data-table-select"},fixed:g.fixed,fixedOffset:g.fixedOffset,lastFixed:g.lastFixed,maxWidth:n.value?void 0:g.maxWidth,noPadding:g.key==="data-table-select"||g.key==="data-table-expand",nowrap:g.nowrap,width:n.value?void 0:g.width},H,b),{default:()=>{var w,P,D,C,G;if(a[V]&&!n.value)return(w=a[V])==null?void 0:w.call(a,k);if(g.key==="data-table-select")return((P=a["item.data-table-select"])==null?void 0:P.call(a,k))??u(he,{disabled:!f.selectable,modelValue:r([f]),onClick:De(()=>o(f),["stop"])},null);if(g.key==="data-table-expand")return((D=a["item.data-table-expand"])==null?void 0:D.call(a,k))??u(A,{icon:m(f)?"$collapse":"$expand",size:"small",variant:"text",onClick:De(()=>p(f),["stop"])},null);const d=N(k.value);return n.value?u(Q,null,[u("div",{class:"v-data-table__td-title"},[((C=a[F])==null?void 0:C.call(a,R))??g.title]),u("div",{class:"v-data-table__td-value"},[((G=a[V])==null?void 0:G.call(a,k))??d])]):d}})})]))}}),it=T({loading:[Boolean,String],loadingText:{type:String,default:"$vuetify.dataIterator.loadingText"},hideNoData:Boolean,items:{type:Array,default:()=>[]},noDataText:{type:String,default:"$vuetify.noDataText"},rowProps:[Object,Function],cellProps:[Object,Function],...be()},"VDataTableRows"),Be=M()({name:"VDataTableRows",inheritAttrs:!1,props:it(),setup(e,l){let{attrs:a,slots:t}=l;const{columns:n}=ue(),{expandOnClick:r,toggleExpand:o,isExpanded:s}=ut(),{isSelected:c,toggleSelect:i}=ie(),{toggleGroup:m,isGroupOpen:p}=nt(),{t:v}=ae(),{mobile:S}=oe(e);return q(()=>{var h,x;return e.loading&&(!e.items.length||t.loading)?u("tr",{class:"v-data-table-rows-loading",key:"loading"},[u("td",{colspan:n.value.length},[((h=t.loading)==null?void 0:h.call(t))??v(e.loadingText)])]):!e.loading&&!e.items.length&&!e.hideNoData?u("tr",{class:"v-data-table-rows-no-data",key:"no-data"},[u("td",{colspan:n.value.length},[((x=t["no-data"])==null?void 0:x.call(t))??v(e.noDataText)])]):u(Q,null,[e.items.map((g,y)=>{var F;if(g.type==="group"){const k={index:y,item:g,columns:n.value,isExpanded:s,toggleExpand:o,isSelected:c,toggleSelect:i,toggleGroup:m,isGroupOpen:p};return t["group-header"]?t["group-header"](k):u($a,B({key:`group-header_${g.id}`,item:g},Ve(a,":group-header",()=>k)),t)}const f={index:y,item:g.raw,internalItem:g,columns:n.value,isExpanded:s,toggleExpand:o,isSelected:c,toggleSelect:i},V={...f,props:B({key:`item_${g.key??g.index}`,onClick:r.value?()=>{o(g)}:void 0,index:y,item:g,cellProps:e.cellProps,mobile:S.value},Ve(a,":row",()=>f),typeof e.rowProps=="function"?e.rowProps({item:f.item,index:f.index,internalItem:f.internalItem}):e.rowProps)};return u(Q,{key:V.props.key},[t.item?t.item(V):u(Oa,V.props,t),s(g)&&((F=t["expanded-row"])==null?void 0:F.call(t,f))])})])}),{}}}),dt=T({fixedHeader:Boolean,fixedFooter:Boolean,height:[Number,String],hover:Boolean,...Ae(),...Le(),...Re(),...Oe()},"VTable"),Fe=M()({name:"VTable",props:dt(),setup(e,l){let{slots:a,emit:t}=l;const{themeClasses:n}=Ne(e),{densityClasses:r}=Wt(e);return q(()=>u(e.tag,{class:["v-table",{"v-table--fixed-height":!!e.height,"v-table--fixed-header":e.fixedHeader,"v-table--fixed-footer":e.fixedFooter,"v-table--has-top":!!a.top,"v-table--has-bottom":!!a.bottom,"v-table--hover":e.hover},n.value,r.value,e.class],style:e.style},{default:()=>{var o,s,c;return[(o=a.top)==null?void 0:o.call(a),a.default?u("div",{class:"v-table__wrapper",style:{height:L(e.height)}},[u("table",null,[a.default()])]):(s=a.wrapper)==null?void 0:s.call(a),(c=a.bottom)==null?void 0:c.call(a)]}})),{}}}),Na=T({items:{type:Array,default:()=>[]},itemValue:{type:[String,Array,Function],default:"id"},itemSelectable:{type:[String,Array,Function],default:null},rowProps:[Object,Function],cellProps:[Object,Function],returnObject:Boolean},"DataTable-items");function Ea(e,l,a,t){const n=e.returnObject?l:re(l,e.itemValue),r=re(l,e.itemSelectable,!0),o=t.reduce((s,c)=>(c.key!=null&&(s[c.key]=re(l,c.value)),s),{});return{type:"item",key:e.returnObject?re(l,e.itemValue):n,index:a,value:n,selectable:r,columns:o,raw:l}}function Ma(e,l,a){return l.map((t,n)=>Ea(e,t,n,a))}function Ha(e,l){return{items:I(()=>Ma(e,e.items,l.value))}}function Ga(e){let{page:l,itemsPerPage:a,sortBy:t,groupBy:n,search:r}=e;const o=Me("VDataTable"),s=I(()=>({page:l.value,itemsPerPage:a.value,sortBy:t.value,groupBy:n.value,search:r.value}));let c=null;He(s,()=>{Ge(c,s.value)||(c&&c.search!==s.value.search&&(l.value=1),o.emit("update:options",s.value),c=s.value)},{deep:!0,immediate:!0})}const ja=T({...it(),hideDefaultBody:Boolean,hideDefaultFooter:Boolean,hideDefaultHeader:Boolean,width:[String,Number],search:String,...Aa(),...Va(),...fa(),...Na(),...Sa(),...Pa(),...at(),...dt()},"DataTable"),Wa=T({...oa(),...ja(),...zt(),...qe()},"VDataTable"),Qa=M()({name:"VDataTable",props:Wa(),emits:{"update:modelValue":e=>!0,"update:page":e=>!0,"update:itemsPerPage":e=>!0,"update:sortBy":e=>!0,"update:options":e=>!0,"update:groupBy":e=>!0,"update:expanded":e=>!0,"update:currentItems":e=>!0},setup(e,l){let{attrs:a,slots:t}=l;const{groupBy:n}=_a(e),{sortBy:r,multiSort:o,mustSort:s}=wa(e),{page:c,itemsPerPage:i}=ua(e),{columns:m,headers:p,sortFunctions:v,sortRawFunctions:S,filterFunctions:h}=ya(e,{groupBy:n,showSelect:_(e,"showSelect"),showExpand:_(e,"showExpand")}),{items:x}=Ha(e,m),g=_(e,"search"),{filteredItems:y}=qt(e,x,g,{transform:j=>j.columns,customKeyFilter:h}),{toggleSort:f}=ka({sortBy:r,multiSort:o,mustSort:s,page:c}),{sortByWithGroups:V,opened:F,extractRows:k,isGroupOpen:R,toggleGroup:H}=Ta({groupBy:n,sortBy:r}),{sortedItems:b}=Ia(e,y,V,{transform:j=>j.columns,sortFunctions:v,sortRawFunctions:S}),{flatItems:d}=Ba(b,n,F),w=I(()=>d.value.length),{startIndex:P,stopIndex:D,pageCount:C,setItemsPerPage:G}=ia({page:c,itemsPerPage:i,itemsLength:w}),{paginatedItems:U}=ca({items:d,startIndex:P,stopIndex:D,itemsPerPage:i}),K=I(()=>k(U.value)),{isSelected:de,select:ct,selectAll:ft,toggleSelect:vt,someSelected:gt,allSelected:mt}=xa(e,{allItems:x,currentPage:K}),{isExpanded:bt,toggleExpand:ht}=La(e);Ga({page:c,itemsPerPage:i,sortBy:r,groupBy:n,search:g}),ge({VDataTableRows:{hideNoData:_(e,"hideNoData"),noDataText:_(e,"noDataText"),loading:_(e,"loading"),loadingText:_(e,"loadingText")}});const $=I(()=>({page:c.value,itemsPerPage:i.value,sortBy:r.value,pageCount:C.value,toggleSort:f,setItemsPerPage:G,someSelected:gt.value,allSelected:mt.value,isSelected:de,select:ct,selectAll:ft,toggleSelect:vt,isExpanded:bt,toggleExpand:ht,isGroupOpen:R,toggleGroup:H,items:K.value.map(j=>j.raw),internalItems:K.value,groupedItems:U.value,columns:m.value,headers:p.value}));return q(()=>{const j=Te.filterProps(e),yt=Ce.filterProps(e),pt=Be.filterProps(e),St=Fe.filterProps(e);return u(Fe,B({class:["v-data-table",{"v-data-table--show-select":e.showSelect,"v-data-table--loading":e.loading},e.class],style:e.style},St),{top:()=>{var Z;return(Z=t.top)==null?void 0:Z.call(t,$.value)},default:()=>{var Z,pe,Se,xe,Pe,we;return t.default?t.default($.value):u(Q,null,[(Z=t.colgroup)==null?void 0:Z.call(t,$.value),!e.hideDefaultHeader&&u("thead",{key:"thead"},[u(Ce,yt,t)]),(pe=t.thead)==null?void 0:pe.call(t,$.value),!e.hideDefaultBody&&u("tbody",null,[(Se=t["body.prepend"])==null?void 0:Se.call(t,$.value),t.body?t.body($.value):u(Be,B(a,pt,{items:U.value}),t),(xe=t["body.append"])==null?void 0:xe.call(t,$.value)]),(Pe=t.tbody)==null?void 0:Pe.call(t,$.value),(we=t.tfoot)==null?void 0:we.call(t,$.value)])},bottom:()=>t.bottom?t.bottom($.value):!e.hideDefaultFooter&&u(Q,null,[u($e,null,null),u(Te,j,{prepend:t["footer.prepend"]})])})}),{}}});export{Xa as D,Qa as V,ja as a,qe as b,_a as c,wa as d,ua as e,ya as f,Ta as g,ia as h,Ba as i,xa as j,La as k,Ga as l,oa as m,Te as n,Ce as o,ka as p,Be as q,Fe as r,Ha as u};
