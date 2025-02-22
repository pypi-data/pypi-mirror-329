import{Y as W,c as H,_ as J}from"./CwXbrQOx.js";import{d as Y,i as f,v as p,z as a,A as s,t as r,ad as P,x as d,y as k,U as B,af as T,L as Z,M as x,ab as z,W as w,B as u,Y as M,V as ee,P as V,Q as S,N as h,ag as te,ah as ae,ai as se,T as $,O as ne,C as ie,D as oe}from"./Bl2PtCmi.js";import{d as q,V as C,O as le,D as re,e as O,u as de,b as G,a as ue}from"./BMk0wala.js";import{s as ce,V as pe,a as me}from"./B1xz6Z1U.js";import{S as ge}from"./DkCZQGJD.js";import{V as he,D as fe}from"./D5IJmzsN.js";import{_ as F}from"./DlAUqK2U.js";import{a as be}from"./CvQdbTl1.js";import{u as ye}from"./D1jDBoMW.js";import{D as ke}from"./H9Z6M5RT.js";import{V as j}from"./BDrxhtKl.js";import{V as K}from"./BCYVl_Vs.js";import{V as U}from"./C2GUiMkT.js";import"./TgNZA6Y3.js";import"./Bo6yBl8U.js";import"./BvH6OxSR.js";const ve={info:1,important:2,secure:3,hardening:4,potentially:5,low:6,medium:7,high:8,critical:9},De=Y({name:"VulnzTable",components:{DfRisk:q},props:{vulnz:{type:Array,required:!0,default:()=>[]},vulnerabilityPreviewLoading:{type:Boolean,default:!1},selectedVulnerabilityKey:{type:String,required:!0}},emits:["goToDetail","goToDetailNewTab","showVulnDetails"],data(){return{headers:[{title:"Show",value:"show",align:"left",width:"4%"},{title:"Risk | CVSS",value:"risk",align:"left",width:"7%"},{title:"Title",value:"title",align:"left",minWidth:"350"},{title:"Short description",value:"description",align:"left"}]}},computed:{kbVulnerabilities(){var n,i,b,v,y,g,o,c,I,_,N,R,L;const e=[];for(const t of this.vulnz)if(((n=t==null?void 0:t.kb)==null?void 0:n.title)==="Use of Outdated Vulnerable Component"){let D=!1;for(const l of t.vulnerabilities.vulnerabilities)if((l==null?void 0:l.metadata)===null||(l==null?void 0:l.metadata)===void 0)D||(e.push({key:l==null?void 0:l.id,goToVulnId:!1,risk:l==null?void 0:l.customRiskRating,title:t.kb.title,securityIssue:t.kb.securityIssue,privacyIssue:t.kb.privacyIssue,targetedByMalware:t.kb.targetedByMalware,targetedByRansomware:t.kb.targetedByRansomware,targetedByNationState:t.kb.targetedByNationState,hasPublicExploit:t.kb.hasPublicExploit,cvssV3:t.highestCvssV3BaseScore,description:t.kb.shortDescription,descriptionFormat:t.kb.shortDescriptionFormat,kb:t.kb}),D=!0);else{const X=(i=l==null?void 0:l.metadata)==null?void 0:i.find(E=>E.name==="dependency_name").value,Q=(b=l==null?void 0:l.metadata)==null?void 0:b.find(E=>E.name==="dependency_version").value;e.push({key:l.id,goToVulnId:!0,risk:l.customRiskRating,cvssV3:l.customCvssV3BaseScore,title:`${t.kb.title} for ${X} version ${Q}`,securityIssue:t.kb.securityIssue,privacyIssue:t.kb.privacyIssue,targetedByMalware:t.kb.targetedByMalware,targetedByRansomware:t.kb.targetedByRansomware,targetedByNationState:t.kb.targetedByNationState,hasPublicExploit:t.kb.hasPublicExploit,description:t.kb.shortDescription,descriptionFormat:t.kb.shortDescriptionFormat,kb:t.kb})}}else e.push({key:(v=t==null?void 0:t.kb)==null?void 0:v.title,goToVulnId:!1,risk:t.highestRiskRating,title:(y=t==null?void 0:t.kb)==null?void 0:y.title,securityIssue:(g=t==null?void 0:t.kb)==null?void 0:g.securityIssue,privacyIssue:(o=t==null?void 0:t.kb)==null?void 0:o.privacyIssue,targetedByMalware:(c=t==null?void 0:t.kb)==null?void 0:c.targetedByMalware,targetedByRansomware:(I=t==null?void 0:t.kb)==null?void 0:I.targetedByRansomware,targetedByNationState:(_=t==null?void 0:t.kb)==null?void 0:_.targetedByNationState,hasPublicExploit:(N=t==null?void 0:t.kb)==null?void 0:N.hasPublicExploit,cvssV3:t.highestCvssV3BaseScore,description:(R=t==null?void 0:t.kb)==null?void 0:R.shortDescription,descriptionFormat:(L=t==null?void 0:t.kb)==null?void 0:L.shortDescriptionFormat,kb:t.kb});return ce(e).by([{desc:t=>{var D;return ve[((D=t==null?void 0:t.risk)==null?void 0:D.toLocaleLowerCase())||""]}},{desc:t=>t.cvssV3}])}},methods:{goToDetail(e){this.$emit("goToDetail",e)},goToDetailNewTab(e){this.$emit("goToDetailNewTab",e)},showVulnDetails(e){this.$emit("showVulnDetails",e)}}}),we=["onClick","onMouseup"],Ve=["onClick","onMouseup"];function Se(e,n,i,b,v,y){const g=f("DfRisk");return r(),p("div",null,[a(he,{hover:"",headers:e.headers,items:e.kbVulnerabilities,"items-per-page":-1},{"item.risk":s(({item:o})=>[a(g,{"cvss-score":o.cvssV3,risk:o.risk,class:"cursor-pointer",onClick:c=>e.goToDetail(o),onMouseup:P(c=>e.goToDetailNewTab(o),["middle"])},null,8,["cvss-score","risk","onClick","onMouseup"])]),"item.title":s(({item:o})=>[d("div",{class:"cursor-pointer",onClick:c=>e.goToDetail(o),onMouseup:P(c=>e.goToDetailNewTab(o),["middle"])},k(o.title),41,we)]),"item.description":s(({item:o})=>[d("div",{class:"cursor-pointer",onClick:c=>e.goToDetail(o),onMouseup:P(c=>e.goToDetailNewTab(o),["middle"])},k(o.description),41,Ve)]),"item.show":s(({item:o})=>[a(B,{size:"small",variant:"text",disabled:e.vulnerabilityPreviewLoading===!0&&o.key!==e.selectedVulnerabilityKey,loading:e.vulnerabilityPreviewLoading===!0&&o.key===e.selectedVulnerabilityKey,icon:"mdi-magnify",onClick:c=>e.showVulnDetails(o)},null,8,["disabled","loading","onClick"])]),_:2},1032,["headers","items"])])}const $e=F(De,[["render",Se]]),Te=Y({name:"VulnerabilityDetailDialog",components:{VulnerabilityDetail:pe},props:{modelValue:{type:Boolean,default:!1},vuln:{type:Object,default:null},scanId:{type:Number,required:!0},scanner:{type:Object,required:!0}},emits:["update:modelValue","update:loading","afterLeave"],data(){return{loading:!1,dialog:!1}},computed:{vulnKey(){var e;return(e=this.vuln)==null?void 0:e.key}},watch:{modelValue:{immediate:!0,handler(e){this.dialog=e}},dialog(e){this.$emit("update:modelValue",e)},loading(e){this.$emit("update:loading",e),this.vuln!==null&&this.vuln!==void 0&&(e===!0?this.dialog=!1:this.dialog=!0)}}}),Be={id:"vulnerability-detail-container"};function Ce(e,n,i,b,v,y){const g=f("VulnerabilityDetail");return r(),p("div",Be,[a(be,{ref:"dialogRef",modelValue:e.dialog,"onUpdate:modelValue":n[1]||(n[1]=o=>e.dialog=o),scrollable:"",attach:"",eager:"","max-width":"50%",transition:"slide-x-transition",class:"ml-auto",onAfterLeave:n[2]||(n[2]=o=>e.$emit("afterLeave"))},{default:s(()=>[a(C,{class:"dialog-card pa-2",loading:e.loading,style:{"min-height":"100vh"}},{default:s(()=>[a(g,{loading:e.loading,"onUpdate:loading":n[0]||(n[0]=o=>e.loading=o),"vuln-title":e.vulnKey,"scan-id":e.scanId,scanner:e.scanner,"show-breadcrumbs":!1},null,8,["loading","vuln-title","scan-id","scanner"])]),_:1},8,["loading"])]),_:1},8,["modelValue"])])}const Ie=F(Te,[["render",Ce]]),A=1,_e=Y({name:"Index",components:{DfRisk:q,OXOAssets:le,DfScanProgress:ke,DfConfirmationModal:fe,VulnzTable:$e,VunerabilityDetailDialog:Ie,DfBreadcrumbs:re},data(){return{scanner:{endpoint:"",name:"",apiKey:""},vulenrabilityLoading:!1,vulnDetailsDialog:!1,selectedVulnerability:null,options:{page:1,itemsPerPage:15},vulnerabilityService:new me(this.$axios),scanService:new ge(this.$axios),kb:null,title:"",progress:"UNKNOWN",riskRating:"UNKNOWN",vulns:[],loadingDialog:!0,stopBtnLoading:!1,deleteScanDialog:!1,archiveBtnLoading:!1,stopScanDialog:!1,assets:[],agentGroup:null,show:!1,editorLanguage:"yaml",editorOptions:{theme:"vs",wordWrap:"on",wordWrapColumn:"on",fontFamily:"Fira Code",automaticLayout:!0,minimap:{enabled:!1},readOnly:!0},breadcrumbs:[{text:"scans",disabled:!1,to:"/scan/list",exact:!0},{text:"Scan",disabled:!1,to:`/scan/${(this._.provides[T]||this.$route).params.scan}`,exact:!0,scans:[]}]}},computed:{...Z(ye,["scanners"]),scanId(){return(this._.provides[T]||this.$route).params.scan===void 0||(this._.provides[T]||this.$route).params.scan===null?(this.reportError("Scan ID not provided"),0):parseInt((this._.provides[T]||this.$route).params.scan)},AgentGroupYaml(){var n,i;const e=(n=this.agentGroup)==null?void 0:n.yamlSource;return e==null?"No agent group found":`# Agent Group ID: ${(i=this.agentGroup)==null?void 0:i.id}
${W.stringify(W.parse(e))}`},totalVulnerabilities(){var e;return((e=this.vulns)==null?void 0:e.length)||0}},async mounted(){const e=this.scanners.find(n=>O(n.endpoint)===(this._.provides[T]||this.$route).params.scanner);e===void 0?(this.reportError("Scanner not found"),this.$router.push({name:"scan-list"})):(this.scanner=e,await Promise.allSettled([this.fetchKBVulnerabilities(),this.fetchScans()]),this.updateBreadcrumbs())},methods:{...x(de,["reportError","reportInfo","reportSuccess"]),async fetchKBVulnerabilities(){var e,n;try{this.loadingDialog=!0;const i=await this.vulnerabilityService.getKBVulnerabilities(this.scanner,this.scanId);this.kb=i,this.vulns=(i==null?void 0:i.kbVulnerabilities)||[],this.title=i==null?void 0:i.title,this.assets=i==null?void 0:i.assets,this.progress=(e=i==null?void 0:i.progress)==null?void 0:e.toLowerCase(),this.riskRating=(n=i==null?void 0:i.riskRating)==null?void 0:n.toLowerCase(),this.agentGroup=i==null?void 0:i.agentGroup}catch(i){this.reportError(`An error was encountered while fetching the scan: ${i}`)}finally{this.loadingDialog=!1}},showVulnDetails(e){this.selectedVulnerability=e,this.vulnDetailsDialog=!0},goToDetail(e){this.$router.push({name:"scan-scanner-scan-vuln-vuln",params:{scan:this.scanId,scanner:O(this.scanner.endpoint),vuln:e.key??e.kb.id}})},goToDetailNewTab(e){const n=this.$router.resolve(`/scan/${O(this.scanner.endpoint)}/${this.scanId}/vuln/${e.key??e.kb.id}`);window.open(n.href,"_blank")},async fetchScans(){this.breadcrumbs[A].scans=await this.scanService.getScans(this.scanner,{page:1,numberElements:20})},updateBreadcrumbs(){var n,i,b;((i=((n=this.breadcrumbs[A])==null?void 0:n.scans)||[])==null?void 0:i.find(v=>{var y;return v.id===((y=this.kb)==null?void 0:y.id)}))===void 0&&(this.breadcrumbs[A].scans=[...((b=this.breadcrumbs[A])==null?void 0:b.scans)||[],this.kb])},async stopScan(){try{this.stopBtnLoading=!0,await this.scanService.stopScans(this.scanner,[this.scanId]),await this.fetchKBVulnerabilities()}catch(e){this.reportError((e==null?void 0:e.message)||"Error Stopping scan.")}finally{this.stopBtnLoading=!1}},async deleteScan(){try{this.loadingDialog=!0,await this.scanService.deleteScans(this.scanner,[this.scanId]),this.reportSuccess("Scan deleted successfully"),this.$router.push("/scan/list")}catch(e){this.reportError(`An error occurred while deleting the scan: ${e.message}`)}finally{this.loadingDialog=!1}},async exportScan(){try{this.loadingDialog=!0,this.reportInfo("Scan export in progress, this process may take some time."),await this.scanService.exportScan(this.scanner,this.scanId),this.reportSuccess("Scan exported successfully")}catch(e){this.reportError((e==null?void 0:e.message)||"An error occurred while exporting the scan")}finally{this.loadingDialog=!1}}}}),Ne=H(J),m=e=>(ie("data-v-e8c5b85a"),e=e(),oe(),e),Re=m(()=>d("span",null,"Stops scan. Stopped scans can't be restarted.",-1)),Le=m(()=>d("span",null,"Archives scan and removes all findings and artifacts.",-1)),Me=m(()=>d("span",null,"Exports scan to a zip file.",-1)),Ae=m(()=>d("p",{class:"mb-0 mr-2"}," Title: ",-1)),Ee={key:0,class:"mb-0"},Pe={key:1},ze={key:1},Oe=m(()=>d("p",{class:"mb-0 mr-2"}," Targets: ",-1)),Ge=m(()=>d("p",{class:"mb-0 mr-2"}," Progress: ",-1)),Ke=m(()=>d("p",{class:"mb-0 mr-2"}," Risk Rating: ",-1)),Ue=m(()=>d("p",{class:"mb-0 mr-2"}," Date: ",-1)),Ye={key:0,class:"mb-0"},Fe={key:1},We={key:1},je=m(()=>d("p",{class:"mb-0 mr-2"}," Scanner: ",-1)),qe={key:0},Xe={key:1},Qe=m(()=>d("span",null,"Agent Group",-1));function He(e,n,i,b,v,y){const g=f("DfConfirmationModal"),o=f("VunerabilityDetailDialog"),c=f("DfBreadcrumbs"),I=f("OXOAssets"),_=f("DfScanProgress"),N=f("DfRisk"),R=Ne,L=f("VulnzTable");return r(),p("div",null,[a(g,{modelValue:e.deleteScanDialog,"onUpdate:modelValue":n[0]||(n[0]=t=>e.deleteScanDialog=t),title:"Are you sure you would like to archive this scan?","cancel-button-text":"Cancel","confirm-button-text":"Delete","cancel-icon":"mdi-close","confirm-icon":"mdi-check","confirm-button-color":"secondary","card-icon":"mdi-archive-arrow-down-outline",onConfirm:e.deleteScan},null,8,["modelValue","onConfirm"]),a(g,{modelValue:e.stopScanDialog,"onUpdate:modelValue":n[1]||(n[1]=t=>e.stopScanDialog=t),title:"Are you sure you would like to stop the scan?",description:"A stopped scan cannot be resumed.","cancel-button-text":"Cancel","confirm-button-text":"Stop","cancel-icon":"mdi-close","confirm-icon":"mdi-check","confirm-button-color":"secondary","card-icon":"mdi-stop-circle-outline",onConfirm:e.stopScan},null,8,["modelValue","onConfirm"]),a(o,{loading:e.vulenrabilityLoading,"onUpdate:loading":n[2]||(n[2]=t=>e.vulenrabilityLoading=t),"model-value":e.vulnDetailsDialog,"onUpdate:modelValue":n[3]||(n[3]=t=>e.vulnDetailsDialog=t),vuln:e.selectedVulnerability,"scan-id":e.scanId,scanner:e.scanner,onAfterLeave:n[4]||(n[4]=t=>e.selectedVulnerability=null)},null,8,["loading","model-value","vuln","scan-id","scanner"]),a(c,{"scan-id":e.scanId,breadcrumbs:e.breadcrumbs,scanner:e.scanner,class:"mb-5"},null,8,["scan-id","breadcrumbs","scanner"]),a(C,{class:"d-flex pl-3 py-3 mt-3",variant:"outlined"},{default:s(()=>[a(K,{bottom:""},{activator:s(({props:t})=>[a(B,z({disabled:e.progress==="stopped"||e.progress==="done"||e.loadingDialog===!0,loading:e.stopBtnLoading,class:"mr-2"},t,{onClick:n[5]||(n[5]=D=>e.stopScanDialog=!0)}),{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-stop-circle-outline ")]),_:1}),u(" Stop ")]),_:2},1040,["disabled","loading"])]),default:s(()=>[Re]),_:1}),a(K,{bottom:""},{activator:s(({props:t})=>[a(B,z({loading:e.archiveBtnLoading,class:"mr-2"},t,{onClick:n[6]||(n[6]=D=>e.deleteScanDialog=!0)}),{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-delete-outline ")]),_:1}),u(" Delete ")]),_:2},1040,["loading"])]),default:s(()=>[Le]),_:1}),a(K,{bottom:""},{activator:s(({props:t})=>[a(B,z({class:"mr-2"},t,{onClick:e.exportScan}),{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-file-export-outline ")]),_:1}),u(" Export ")]),_:2},1040,["onClick"])]),default:s(()=>[Me]),_:1})]),_:1}),a(j,{class:"mt-4 align-stretch"},{default:s(()=>[a(U,{cols:"12",lg:"12"},{default:s(()=>[a(C,{loading:e.loadingDialog,height:"100%",variant:"outlined"},{default:s(()=>[a(G,null,{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-shield-check-outline ")]),_:1}),u(" Scan Details ")]),_:1}),a(M),a(ee,null,{default:s(()=>[a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[Ae,e.title!==null&&e.title!==""?(r(),p("p",Ee,k(e.title),1)):(r(),p("div",Pe,[e.loadingDialog===!0?(r(),h($,{key:0,variant:"tonal",size:"small",label:"",style:{width:"80px"}})):(r(),p("span",ze,"-"))]))]),_:1})]),_:1}),a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[Oe,e.loadingDialog===!0?(r(),h($,{key:0,variant:"tonal",label:"",style:{width:"90px"}})):(r(),h(I,{key:1,assets:e.assets},null,8,["assets"]))]),_:1})]),_:1}),a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[Ge,e.loadingDialog===!0?(r(),h($,{key:0,variant:"tonal",size:"small",label:"",style:{width:"60px"}})):(r(),h(_,{key:1,progress:e.progress},null,8,["progress"]))]),_:1})]),_:1}),a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[Ke,e.loadingDialog===!0?(r(),h($,{key:0,variant:"tonal",size:"small",label:"",style:{width:"60px"}})):(r(),h(N,{key:1,risk:e.riskRating},null,8,["risk"]))]),_:1})]),_:1}),a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[Ue,e.loadingDialog===!1&&e.kb!==null?(r(),p("p",Ye,k(e.$moment(e.kb.createdTime).format("MMMM Do YYYY, k:mm:ss")),1)):(r(),p("div",Fe,[e.loadingDialog===!0?(r(),h($,{key:0,variant:"tonal",size:"x-small",label:"",style:{width:"180px"}})):(r(),p("span",We,"-"))]))]),_:1})]),_:1}),a(V,null,{default:s(()=>[a(S,{class:"d-flex align-center"},{default:s(()=>[je,d("div",null,[(e.scanner.name||"").trim()!==""?(r(),p("p",qe,[u(k(e.scanner.name)+" (",1),d("code",null,k(e.scanner.endpoint),1),u(") ")])):(r(),p("code",Xe,k(e.scanner.endpoint),1))])]),_:1})]),_:1})]),_:1})]),_:1},8,["loading"])]),_:1})]),_:1}),a(C,{class:"mt-12",variant:"outlined"},{default:s(()=>[a(G,{class:"cursor-pointer",onClick:n[7]||(n[7]=t=>e.show=!e.show)},{default:s(()=>[a(j,{align:"center",justify:"space-between",class:"w-100"},{default:s(()=>[a(U,{class:"d-flex align-center"},{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-format-list-group ")]),_:1}),Qe]),_:1}),a(U,{class:"d-flex justify-end"},{default:s(()=>[a(B,{icon:e.show?"mdi-chevron-up":"mdi-chevron-down",elevation:"0"},null,8,["icon"])]),_:1})]),_:1})]),_:1}),a(M),a(te,null,{default:s(()=>[ae(d("div",null,[a(M),a(ue,null,{default:s(()=>[a(R,{modelValue:e.AgentGroupYaml,"onUpdate:modelValue":n[8]||(n[8]=t=>e.AgentGroupYaml=t),lang:e.editorLanguage,options:e.editorOptions,style:{"min-height":"300px"}},null,8,["modelValue","lang","options"])]),_:1})],512),[[se,e.show]])]),_:1})]),_:1}),a(C,{loading:e.loadingDialog,class:"mt-12",justify:"space-around",variant:"outlined"},{default:s(()=>[a(G,null,{default:s(()=>[a(w,{start:""},{default:s(()=>[u(" mdi-bug-outline ")]),_:1}),u(" Vulnerabilities "),e.totalVulnerabilities!==null?(r(),h($,{key:0,size:"small",class:"ml-2"},{default:s(()=>[u(k(e.totalVulnerabilities),1)]),_:1})):ne("",!0)]),_:1}),a(M),a(L,{"vulnerability-preview-loading":e.vulenrabilityLoading,vulnz:e.vulns,"selected-vulnerability-key":e.selectedVulnerability!==null?e.selectedVulnerability.key:null,onGoToDetail:e.goToDetail,onGoToDetailNewTab:e.goToDetailNewTab,onShowVulnDetails:e.showVulnDetails},null,8,["vulnerability-preview-loading","vulnz","selected-vulnerability-key","onGoToDetail","onGoToDetailNewTab","onShowVulnDetails"])]),_:1},8,["loading"])])}const mt=F(_e,[["render",He],["__scopeId","data-v-e8c5b85a"]]);export{mt as default};
