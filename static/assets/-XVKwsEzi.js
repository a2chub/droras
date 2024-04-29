import{r as b,j as c,u as me,c as he}from"./index-BTpZoLbl.js";function O(){return O=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e},O.apply(this,arguments)}function xe(e,t){typeof e=="function"?e(t):e!=null&&(e.current=t)}function ye(...e){return t=>e.forEach(r=>xe(r,t))}const ae=b.forwardRef((e,t)=>{const{children:r,...o}=e,i=b.Children.toArray(r),n=i.find(we);if(n){const s=n.props.children,l=i.map(f=>f===n?b.Children.count(s)>1?b.Children.only(null):b.isValidElement(s)?s.props.children:null:f);return b.createElement(q,O({},o,{ref:t}),b.isValidElement(s)?b.cloneElement(s,void 0,l):null)}return b.createElement(q,O({},o,{ref:t}),r)});ae.displayName="Slot";const q=b.forwardRef((e,t)=>{const{children:r,...o}=e;return b.isValidElement(r)?b.cloneElement(r,{...ke(o,r.props),ref:t?ye(t,r.ref):r.ref}):b.Children.count(r)>1?b.Children.only(null):null});q.displayName="SlotClone";const ve=({children:e})=>b.createElement(b.Fragment,null,e);function we(e){return b.isValidElement(e)&&e.type===ve}function ke(e,t){const r={...t};for(const o in t){const i=e[o],n=t[o];/^on[A-Z]/.test(o)?i&&n?r[o]=(...l)=>{n(...l),i(...l)}:i&&(r[o]=i):o==="style"?r[o]={...i,...n}:o==="className"&&(r[o]=[i,n].filter(Boolean).join(" "))}return{...e,...r}}function ce(e){var t,r,o="";if(typeof e=="string"||typeof e=="number")o+=e;else if(typeof e=="object")if(Array.isArray(e))for(t=0;t<e.length;t++)e[t]&&(r=ce(e[t]))&&(o&&(o+=" "),o+=r);else for(t in e)e[t]&&(o&&(o+=" "),o+=t);return o}function je(){for(var e,t,r=0,o="";r<arguments.length;)(e=arguments[r++])&&(t=ce(e))&&(o&&(o+=" "),o+=t);return o}const ne=e=>typeof e=="boolean"?"".concat(e):e===0?"0":e,se=je,Ce=(e,t)=>r=>{var o;if((t==null?void 0:t.variants)==null)return se(e,r==null?void 0:r.class,r==null?void 0:r.className);const{variants:i,defaultVariants:n}=t,s=Object.keys(i).map(d=>{const u=r==null?void 0:r[d],p=n==null?void 0:n[d];if(u===null)return null;const y=ne(u)||ne(p);return i[d][y]}),l=r&&Object.entries(r).reduce((d,u)=>{let[p,y]=u;return y===void 0||(d[p]=y),d},{}),f=t==null||(o=t.compoundVariants)===null||o===void 0?void 0:o.reduce((d,u)=>{let{class:p,className:y,...v}=u;return Object.entries(v).every(w=>{let[g,x]=w;return Array.isArray(x)?x.includes({...n,...l}[g]):{...n,...l}[g]===x})?[...d,p,y]:d},[]);return se(e,s,f,r==null?void 0:r.class,r==null?void 0:r.className)};function de(e){var t,r,o="";if(typeof e=="string"||typeof e=="number")o+=e;else if(typeof e=="object")if(Array.isArray(e)){var i=e.length;for(t=0;t<i;t++)e[t]&&(r=de(e[t]))&&(o&&(o+=" "),o+=r)}else for(r in e)e[r]&&(o&&(o+=" "),o+=r);return o}function Ne(){for(var e,t,r=0,o="",i=arguments.length;r<i;r++)(e=arguments[r])&&(t=de(e))&&(o&&(o+=" "),o+=t);return o}const Z="-";function Se(e){const t=Ae(e),{conflictingClassGroups:r,conflictingClassGroupModifiers:o}=e;function i(s){const l=s.split(Z);return l[0]===""&&l.length!==1&&l.shift(),ue(l,t)||ze(s)}function n(s,l){const f=r[s]||[];return l&&o[s]?[...f,...o[s]]:f}return{getClassGroupId:i,getConflictingClassGroupIds:n}}function ue(e,t){var s;if(e.length===0)return t.classGroupId;const r=e[0],o=t.nextPart.get(r),i=o?ue(e.slice(1),o):void 0;if(i)return i;if(t.validators.length===0)return;const n=e.join(Z);return(s=t.validators.find(({validator:l})=>l(n)))==null?void 0:s.classGroupId}const ie=/^\[(.+)\]$/;function ze(e){if(ie.test(e)){const t=ie.exec(e)[1],r=t==null?void 0:t.substring(0,t.indexOf(":"));if(r)return"arbitrary.."+r}}function Ae(e){const{theme:t,prefix:r}=e,o={nextPart:new Map,validators:[]};return $e(Object.entries(e.classGroups),r).forEach(([n,s])=>{K(s,o,n,t)}),o}function K(e,t,r,o){e.forEach(i=>{if(typeof i=="string"){const n=i===""?t:le(t,i);n.classGroupId=r;return}if(typeof i=="function"){if(Ee(i)){K(i(o),t,r,o);return}t.validators.push({validator:i,classGroupId:r});return}Object.entries(i).forEach(([n,s])=>{K(s,le(t,n),r,o)})})}function le(e,t){let r=e;return t.split(Z).forEach(o=>{r.nextPart.has(o)||r.nextPart.set(o,{nextPart:new Map,validators:[]}),r=r.nextPart.get(o)}),r}function Ee(e){return e.isThemeGetter}function $e(e,t){return t?e.map(([r,o])=>{const i=o.map(n=>typeof n=="string"?t+n:typeof n=="object"?Object.fromEntries(Object.entries(n).map(([s,l])=>[t+s,l])):n);return[r,i]}):e}function Me(e){if(e<1)return{get:()=>{},set:()=>{}};let t=0,r=new Map,o=new Map;function i(n,s){r.set(n,s),t++,t>e&&(t=0,o=r,r=new Map)}return{get(n){let s=r.get(n);if(s!==void 0)return s;if((s=o.get(n))!==void 0)return i(n,s),s},set(n,s){r.has(n)?r.set(n,s):i(n,s)}}}const fe="!";function Re(e){const t=e.separator,r=t.length===1,o=t[0],i=t.length;return function(s){const l=[];let f=0,d=0,u;for(let g=0;g<s.length;g++){let x=s[g];if(f===0){if(x===o&&(r||s.slice(g,g+i)===t)){l.push(s.slice(d,g)),d=g+i;continue}if(x==="/"){u=g;continue}}x==="["?f++:x==="]"&&f--}const p=l.length===0?s:s.substring(d),y=p.startsWith(fe),v=y?p.substring(1):p,w=u&&u>d?u-d:void 0;return{modifiers:l,hasImportantModifier:y,baseClassName:v,maybePostfixModifierPosition:w}}}function Te(e){if(e.length<=1)return e;const t=[];let r=[];return e.forEach(o=>{o[0]==="["?(t.push(...r.sort(),o),r=[]):r.push(o)}),t.push(...r.sort()),t}function Pe(e){return{cache:Me(e.cacheSize),splitModifiers:Re(e),...Se(e)}}const Ie=/\s+/;function Ge(e,t){const{splitModifiers:r,getClassGroupId:o,getConflictingClassGroupIds:i}=t,n=new Set;return e.trim().split(Ie).map(s=>{const{modifiers:l,hasImportantModifier:f,baseClassName:d,maybePostfixModifierPosition:u}=r(s);let p=o(u?d.substring(0,u):d),y=!!u;if(!p){if(!u)return{isTailwindClass:!1,originalClassName:s};if(p=o(d),!p)return{isTailwindClass:!1,originalClassName:s};y=!1}const v=Te(l).join(":");return{isTailwindClass:!0,modifierId:f?v+fe:v,classGroupId:p,originalClassName:s,hasPostfixModifier:y}}).reverse().filter(s=>{if(!s.isTailwindClass)return!0;const{modifierId:l,classGroupId:f,hasPostfixModifier:d}=s,u=l+f;return n.has(u)?!1:(n.add(u),i(f,d).forEach(p=>n.add(l+p)),!0)}).reverse().map(s=>s.originalClassName).join(" ")}function Ve(){let e=0,t,r,o="";for(;e<arguments.length;)(t=arguments[e++])&&(r=pe(t))&&(o&&(o+=" "),o+=r);return o}function pe(e){if(typeof e=="string")return e;let t,r="";for(let o=0;o<e.length;o++)e[o]&&(t=pe(e[o]))&&(r&&(r+=" "),r+=t);return r}function Le(e,...t){let r,o,i,n=s;function s(f){const d=t.reduce((u,p)=>p(u),e());return r=Pe(d),o=r.cache.get,i=r.cache.set,n=l,l(f)}function l(f){const d=o(f);if(d)return d;const u=Ge(f,r);return i(f,u),u}return function(){return n(Ve.apply(null,arguments))}}function m(e){const t=r=>r[e]||[];return t.isThemeGetter=!0,t}const be=/^\[(?:([a-z-]+):)?(.+)\]$/i,Oe=/^\d+\/\d+$/,We=new Set(["px","full","screen"]),Be=/^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$/,He=/\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$/,_e=/^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$/,Fe=/^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)/,Ue=/^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$/;function C(e){return A(e)||We.has(e)||Oe.test(e)}function N(e){return E(e,"length",De)}function A(e){return!!e&&!Number.isNaN(Number(e))}function L(e){return E(e,"number",A)}function R(e){return!!e&&Number.isInteger(Number(e))}function qe(e){return e.endsWith("%")&&A(e.slice(0,-1))}function a(e){return be.test(e)}function S(e){return Be.test(e)}const Ke=new Set(["length","size","percentage"]);function Ze(e){return E(e,Ke,ge)}function Je(e){return E(e,"position",ge)}const Xe=new Set(["image","url"]);function Qe(e){return E(e,Xe,tt)}function Ye(e){return E(e,"",et)}function T(){return!0}function E(e,t,r){const o=be.exec(e);return o?o[1]?typeof t=="string"?o[1]===t:t.has(o[1]):r(o[2]):!1}function De(e){return He.test(e)&&!_e.test(e)}function ge(){return!1}function et(e){return Fe.test(e)}function tt(e){return Ue.test(e)}function rt(){const e=m("colors"),t=m("spacing"),r=m("blur"),o=m("brightness"),i=m("borderColor"),n=m("borderRadius"),s=m("borderSpacing"),l=m("borderWidth"),f=m("contrast"),d=m("grayscale"),u=m("hueRotate"),p=m("invert"),y=m("gap"),v=m("gradientColorStops"),w=m("gradientColorStopPositions"),g=m("inset"),x=m("margin"),k=m("opacity"),j=m("padding"),J=m("saturate"),W=m("scale"),X=m("sepia"),Q=m("skew"),Y=m("space"),D=m("translate"),B=()=>["auto","contain","none"],H=()=>["auto","hidden","clip","visible","scroll"],_=()=>["auto",a,t],h=()=>[a,t],ee=()=>["",C,N],I=()=>["auto",A,a],te=()=>["bottom","center","left","left-bottom","left-top","right","right-bottom","right-top","top"],G=()=>["solid","dashed","dotted","double","none"],re=()=>["normal","multiply","screen","overlay","darken","lighten","color-dodge","color-burn","hard-light","soft-light","difference","exclusion","hue","saturation","color","luminosity"],F=()=>["start","end","center","between","around","evenly","stretch"],$=()=>["","0",a],oe=()=>["auto","avoid","all","avoid-page","page","left","right","column"],M=()=>[A,L],V=()=>[A,a];return{cacheSize:500,separator:":",theme:{colors:[T],spacing:[C,N],blur:["none","",S,a],brightness:M(),borderColor:[e],borderRadius:["none","","full",S,a],borderSpacing:h(),borderWidth:ee(),contrast:M(),grayscale:$(),hueRotate:V(),invert:$(),gap:h(),gradientColorStops:[e],gradientColorStopPositions:[qe,N],inset:_(),margin:_(),opacity:M(),padding:h(),saturate:M(),scale:M(),sepia:$(),skew:V(),space:h(),translate:h()},classGroups:{aspect:[{aspect:["auto","square","video",a]}],container:["container"],columns:[{columns:[S]}],"break-after":[{"break-after":oe()}],"break-before":[{"break-before":oe()}],"break-inside":[{"break-inside":["auto","avoid","avoid-page","avoid-column"]}],"box-decoration":[{"box-decoration":["slice","clone"]}],box:[{box:["border","content"]}],display:["block","inline-block","inline","flex","inline-flex","table","inline-table","table-caption","table-cell","table-column","table-column-group","table-footer-group","table-header-group","table-row-group","table-row","flow-root","grid","inline-grid","contents","list-item","hidden"],float:[{float:["right","left","none","start","end"]}],clear:[{clear:["left","right","both","none","start","end"]}],isolation:["isolate","isolation-auto"],"object-fit":[{object:["contain","cover","fill","none","scale-down"]}],"object-position":[{object:[...te(),a]}],overflow:[{overflow:H()}],"overflow-x":[{"overflow-x":H()}],"overflow-y":[{"overflow-y":H()}],overscroll:[{overscroll:B()}],"overscroll-x":[{"overscroll-x":B()}],"overscroll-y":[{"overscroll-y":B()}],position:["static","fixed","absolute","relative","sticky"],inset:[{inset:[g]}],"inset-x":[{"inset-x":[g]}],"inset-y":[{"inset-y":[g]}],start:[{start:[g]}],end:[{end:[g]}],top:[{top:[g]}],right:[{right:[g]}],bottom:[{bottom:[g]}],left:[{left:[g]}],visibility:["visible","invisible","collapse"],z:[{z:["auto",R,a]}],basis:[{basis:_()}],"flex-direction":[{flex:["row","row-reverse","col","col-reverse"]}],"flex-wrap":[{flex:["wrap","wrap-reverse","nowrap"]}],flex:[{flex:["1","auto","initial","none",a]}],grow:[{grow:$()}],shrink:[{shrink:$()}],order:[{order:["first","last","none",R,a]}],"grid-cols":[{"grid-cols":[T]}],"col-start-end":[{col:["auto",{span:["full",R,a]},a]}],"col-start":[{"col-start":I()}],"col-end":[{"col-end":I()}],"grid-rows":[{"grid-rows":[T]}],"row-start-end":[{row:["auto",{span:[R,a]},a]}],"row-start":[{"row-start":I()}],"row-end":[{"row-end":I()}],"grid-flow":[{"grid-flow":["row","col","dense","row-dense","col-dense"]}],"auto-cols":[{"auto-cols":["auto","min","max","fr",a]}],"auto-rows":[{"auto-rows":["auto","min","max","fr",a]}],gap:[{gap:[y]}],"gap-x":[{"gap-x":[y]}],"gap-y":[{"gap-y":[y]}],"justify-content":[{justify:["normal",...F()]}],"justify-items":[{"justify-items":["start","end","center","stretch"]}],"justify-self":[{"justify-self":["auto","start","end","center","stretch"]}],"align-content":[{content:["normal",...F(),"baseline"]}],"align-items":[{items:["start","end","center","baseline","stretch"]}],"align-self":[{self:["auto","start","end","center","stretch","baseline"]}],"place-content":[{"place-content":[...F(),"baseline"]}],"place-items":[{"place-items":["start","end","center","baseline","stretch"]}],"place-self":[{"place-self":["auto","start","end","center","stretch"]}],p:[{p:[j]}],px:[{px:[j]}],py:[{py:[j]}],ps:[{ps:[j]}],pe:[{pe:[j]}],pt:[{pt:[j]}],pr:[{pr:[j]}],pb:[{pb:[j]}],pl:[{pl:[j]}],m:[{m:[x]}],mx:[{mx:[x]}],my:[{my:[x]}],ms:[{ms:[x]}],me:[{me:[x]}],mt:[{mt:[x]}],mr:[{mr:[x]}],mb:[{mb:[x]}],ml:[{ml:[x]}],"space-x":[{"space-x":[Y]}],"space-x-reverse":["space-x-reverse"],"space-y":[{"space-y":[Y]}],"space-y-reverse":["space-y-reverse"],w:[{w:["auto","min","max","fit","svw","lvw","dvw",a,t]}],"min-w":[{"min-w":[a,t,"min","max","fit"]}],"max-w":[{"max-w":[a,t,"none","full","min","max","fit","prose",{screen:[S]},S]}],h:[{h:[a,t,"auto","min","max","fit","svh","lvh","dvh"]}],"min-h":[{"min-h":[a,t,"min","max","fit","svh","lvh","dvh"]}],"max-h":[{"max-h":[a,t,"min","max","fit","svh","lvh","dvh"]}],size:[{size:[a,t,"auto","min","max","fit"]}],"font-size":[{text:["base",S,N]}],"font-smoothing":["antialiased","subpixel-antialiased"],"font-style":["italic","not-italic"],"font-weight":[{font:["thin","extralight","light","normal","medium","semibold","bold","extrabold","black",L]}],"font-family":[{font:[T]}],"fvn-normal":["normal-nums"],"fvn-ordinal":["ordinal"],"fvn-slashed-zero":["slashed-zero"],"fvn-figure":["lining-nums","oldstyle-nums"],"fvn-spacing":["proportional-nums","tabular-nums"],"fvn-fraction":["diagonal-fractions","stacked-fractons"],tracking:[{tracking:["tighter","tight","normal","wide","wider","widest",a]}],"line-clamp":[{"line-clamp":["none",A,L]}],leading:[{leading:["none","tight","snug","normal","relaxed","loose",C,a]}],"list-image":[{"list-image":["none",a]}],"list-style-type":[{list:["none","disc","decimal",a]}],"list-style-position":[{list:["inside","outside"]}],"placeholder-color":[{placeholder:[e]}],"placeholder-opacity":[{"placeholder-opacity":[k]}],"text-alignment":[{text:["left","center","right","justify","start","end"]}],"text-color":[{text:[e]}],"text-opacity":[{"text-opacity":[k]}],"text-decoration":["underline","overline","line-through","no-underline"],"text-decoration-style":[{decoration:[...G(),"wavy"]}],"text-decoration-thickness":[{decoration:["auto","from-font",C,N]}],"underline-offset":[{"underline-offset":["auto",C,a]}],"text-decoration-color":[{decoration:[e]}],"text-transform":["uppercase","lowercase","capitalize","normal-case"],"text-overflow":["truncate","text-ellipsis","text-clip"],"text-wrap":[{text:["wrap","nowrap","balance","pretty"]}],indent:[{indent:h()}],"vertical-align":[{align:["baseline","top","middle","bottom","text-top","text-bottom","sub","super",a]}],whitespace:[{whitespace:["normal","nowrap","pre","pre-line","pre-wrap","break-spaces"]}],break:[{break:["normal","words","all","keep"]}],hyphens:[{hyphens:["none","manual","auto"]}],content:[{content:["none",a]}],"bg-attachment":[{bg:["fixed","local","scroll"]}],"bg-clip":[{"bg-clip":["border","padding","content","text"]}],"bg-opacity":[{"bg-opacity":[k]}],"bg-origin":[{"bg-origin":["border","padding","content"]}],"bg-position":[{bg:[...te(),Je]}],"bg-repeat":[{bg:["no-repeat",{repeat:["","x","y","round","space"]}]}],"bg-size":[{bg:["auto","cover","contain",Ze]}],"bg-image":[{bg:["none",{"gradient-to":["t","tr","r","br","b","bl","l","tl"]},Qe]}],"bg-color":[{bg:[e]}],"gradient-from-pos":[{from:[w]}],"gradient-via-pos":[{via:[w]}],"gradient-to-pos":[{to:[w]}],"gradient-from":[{from:[v]}],"gradient-via":[{via:[v]}],"gradient-to":[{to:[v]}],rounded:[{rounded:[n]}],"rounded-s":[{"rounded-s":[n]}],"rounded-e":[{"rounded-e":[n]}],"rounded-t":[{"rounded-t":[n]}],"rounded-r":[{"rounded-r":[n]}],"rounded-b":[{"rounded-b":[n]}],"rounded-l":[{"rounded-l":[n]}],"rounded-ss":[{"rounded-ss":[n]}],"rounded-se":[{"rounded-se":[n]}],"rounded-ee":[{"rounded-ee":[n]}],"rounded-es":[{"rounded-es":[n]}],"rounded-tl":[{"rounded-tl":[n]}],"rounded-tr":[{"rounded-tr":[n]}],"rounded-br":[{"rounded-br":[n]}],"rounded-bl":[{"rounded-bl":[n]}],"border-w":[{border:[l]}],"border-w-x":[{"border-x":[l]}],"border-w-y":[{"border-y":[l]}],"border-w-s":[{"border-s":[l]}],"border-w-e":[{"border-e":[l]}],"border-w-t":[{"border-t":[l]}],"border-w-r":[{"border-r":[l]}],"border-w-b":[{"border-b":[l]}],"border-w-l":[{"border-l":[l]}],"border-opacity":[{"border-opacity":[k]}],"border-style":[{border:[...G(),"hidden"]}],"divide-x":[{"divide-x":[l]}],"divide-x-reverse":["divide-x-reverse"],"divide-y":[{"divide-y":[l]}],"divide-y-reverse":["divide-y-reverse"],"divide-opacity":[{"divide-opacity":[k]}],"divide-style":[{divide:G()}],"border-color":[{border:[i]}],"border-color-x":[{"border-x":[i]}],"border-color-y":[{"border-y":[i]}],"border-color-t":[{"border-t":[i]}],"border-color-r":[{"border-r":[i]}],"border-color-b":[{"border-b":[i]}],"border-color-l":[{"border-l":[i]}],"divide-color":[{divide:[i]}],"outline-style":[{outline:["",...G()]}],"outline-offset":[{"outline-offset":[C,a]}],"outline-w":[{outline:[C,N]}],"outline-color":[{outline:[e]}],"ring-w":[{ring:ee()}],"ring-w-inset":["ring-inset"],"ring-color":[{ring:[e]}],"ring-opacity":[{"ring-opacity":[k]}],"ring-offset-w":[{"ring-offset":[C,N]}],"ring-offset-color":[{"ring-offset":[e]}],shadow:[{shadow:["","inner","none",S,Ye]}],"shadow-color":[{shadow:[T]}],opacity:[{opacity:[k]}],"mix-blend":[{"mix-blend":[...re(),"plus-lighter","plus-darker"]}],"bg-blend":[{"bg-blend":re()}],filter:[{filter:["","none"]}],blur:[{blur:[r]}],brightness:[{brightness:[o]}],contrast:[{contrast:[f]}],"drop-shadow":[{"drop-shadow":["","none",S,a]}],grayscale:[{grayscale:[d]}],"hue-rotate":[{"hue-rotate":[u]}],invert:[{invert:[p]}],saturate:[{saturate:[J]}],sepia:[{sepia:[X]}],"backdrop-filter":[{"backdrop-filter":["","none"]}],"backdrop-blur":[{"backdrop-blur":[r]}],"backdrop-brightness":[{"backdrop-brightness":[o]}],"backdrop-contrast":[{"backdrop-contrast":[f]}],"backdrop-grayscale":[{"backdrop-grayscale":[d]}],"backdrop-hue-rotate":[{"backdrop-hue-rotate":[u]}],"backdrop-invert":[{"backdrop-invert":[p]}],"backdrop-opacity":[{"backdrop-opacity":[k]}],"backdrop-saturate":[{"backdrop-saturate":[J]}],"backdrop-sepia":[{"backdrop-sepia":[X]}],"border-collapse":[{border:["collapse","separate"]}],"border-spacing":[{"border-spacing":[s]}],"border-spacing-x":[{"border-spacing-x":[s]}],"border-spacing-y":[{"border-spacing-y":[s]}],"table-layout":[{table:["auto","fixed"]}],caption:[{caption:["top","bottom"]}],transition:[{transition:["none","all","","colors","opacity","shadow","transform",a]}],duration:[{duration:V()}],ease:[{ease:["linear","in","out","in-out",a]}],delay:[{delay:V()}],animate:[{animate:["none","spin","ping","pulse","bounce",a]}],transform:[{transform:["","gpu","none"]}],scale:[{scale:[W]}],"scale-x":[{"scale-x":[W]}],"scale-y":[{"scale-y":[W]}],rotate:[{rotate:[R,a]}],"translate-x":[{"translate-x":[D]}],"translate-y":[{"translate-y":[D]}],"skew-x":[{"skew-x":[Q]}],"skew-y":[{"skew-y":[Q]}],"transform-origin":[{origin:["center","top","top-right","right","bottom-right","bottom","bottom-left","left","top-left",a]}],accent:[{accent:["auto",e]}],appearance:[{appearance:["none","auto"]}],cursor:[{cursor:["auto","default","pointer","wait","text","move","help","not-allowed","none","context-menu","progress","cell","crosshair","vertical-text","alias","copy","no-drop","grab","grabbing","all-scroll","col-resize","row-resize","n-resize","e-resize","s-resize","w-resize","ne-resize","nw-resize","se-resize","sw-resize","ew-resize","ns-resize","nesw-resize","nwse-resize","zoom-in","zoom-out",a]}],"caret-color":[{caret:[e]}],"pointer-events":[{"pointer-events":["none","auto"]}],resize:[{resize:["none","y","x",""]}],"scroll-behavior":[{scroll:["auto","smooth"]}],"scroll-m":[{"scroll-m":h()}],"scroll-mx":[{"scroll-mx":h()}],"scroll-my":[{"scroll-my":h()}],"scroll-ms":[{"scroll-ms":h()}],"scroll-me":[{"scroll-me":h()}],"scroll-mt":[{"scroll-mt":h()}],"scroll-mr":[{"scroll-mr":h()}],"scroll-mb":[{"scroll-mb":h()}],"scroll-ml":[{"scroll-ml":h()}],"scroll-p":[{"scroll-p":h()}],"scroll-px":[{"scroll-px":h()}],"scroll-py":[{"scroll-py":h()}],"scroll-ps":[{"scroll-ps":h()}],"scroll-pe":[{"scroll-pe":h()}],"scroll-pt":[{"scroll-pt":h()}],"scroll-pr":[{"scroll-pr":h()}],"scroll-pb":[{"scroll-pb":h()}],"scroll-pl":[{"scroll-pl":h()}],"snap-align":[{snap:["start","end","center","align-none"]}],"snap-stop":[{snap:["normal","always"]}],"snap-type":[{snap:["none","x","y","both"]}],"snap-strictness":[{snap:["mandatory","proximity"]}],touch:[{touch:["auto","none","manipulation"]}],"touch-x":[{"touch-pan":["x","left","right"]}],"touch-y":[{"touch-pan":["y","up","down"]}],"touch-pz":["touch-pinch-zoom"],select:[{select:["none","text","all","auto"]}],"will-change":[{"will-change":["auto","scroll","contents","transform",a]}],fill:[{fill:[e,"none"]}],"stroke-w":[{stroke:[C,N,L]}],stroke:[{stroke:[e,"none"]}],sr:["sr-only","not-sr-only"],"forced-color-adjust":[{"forced-color-adjust":["auto","none"]}]},conflictingClassGroups:{overflow:["overflow-x","overflow-y"],overscroll:["overscroll-x","overscroll-y"],inset:["inset-x","inset-y","start","end","top","right","bottom","left"],"inset-x":["right","left"],"inset-y":["top","bottom"],flex:["basis","grow","shrink"],gap:["gap-x","gap-y"],p:["px","py","ps","pe","pt","pr","pb","pl"],px:["pr","pl"],py:["pt","pb"],m:["mx","my","ms","me","mt","mr","mb","ml"],mx:["mr","ml"],my:["mt","mb"],size:["w","h"],"font-size":["leading"],"fvn-normal":["fvn-ordinal","fvn-slashed-zero","fvn-figure","fvn-spacing","fvn-fraction"],"fvn-ordinal":["fvn-normal"],"fvn-slashed-zero":["fvn-normal"],"fvn-figure":["fvn-normal"],"fvn-spacing":["fvn-normal"],"fvn-fraction":["fvn-normal"],"line-clamp":["display","overflow"],rounded:["rounded-s","rounded-e","rounded-t","rounded-r","rounded-b","rounded-l","rounded-ss","rounded-se","rounded-ee","rounded-es","rounded-tl","rounded-tr","rounded-br","rounded-bl"],"rounded-s":["rounded-ss","rounded-es"],"rounded-e":["rounded-se","rounded-ee"],"rounded-t":["rounded-tl","rounded-tr"],"rounded-r":["rounded-tr","rounded-br"],"rounded-b":["rounded-br","rounded-bl"],"rounded-l":["rounded-tl","rounded-bl"],"border-spacing":["border-spacing-x","border-spacing-y"],"border-w":["border-w-s","border-w-e","border-w-t","border-w-r","border-w-b","border-w-l"],"border-w-x":["border-w-r","border-w-l"],"border-w-y":["border-w-t","border-w-b"],"border-color":["border-color-t","border-color-r","border-color-b","border-color-l"],"border-color-x":["border-color-r","border-color-l"],"border-color-y":["border-color-t","border-color-b"],"scroll-m":["scroll-mx","scroll-my","scroll-ms","scroll-me","scroll-mt","scroll-mr","scroll-mb","scroll-ml"],"scroll-mx":["scroll-mr","scroll-ml"],"scroll-my":["scroll-mt","scroll-mb"],"scroll-p":["scroll-px","scroll-py","scroll-ps","scroll-pe","scroll-pt","scroll-pr","scroll-pb","scroll-pl"],"scroll-px":["scroll-pr","scroll-pl"],"scroll-py":["scroll-pt","scroll-pb"],touch:["touch-x","touch-y","touch-pz"],"touch-x":["touch"],"touch-y":["touch"],"touch-pz":["touch"]},conflictingClassGroupModifiers:{"font-size":["leading"]}}}const ot=Le(rt);function nt(...e){return ot(Ne(e))}const st=Ce("inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),z=b.forwardRef(({className:e,variant:t,size:r,asChild:o=!1,...i},n)=>{const s=o?ae:"button";return c.jsx(s,{className:nt(st({variant:t,size:r,className:e})),ref:n,...i})});z.displayName="Button";const P=120;function it(e){const t=b.useRef(0),r=b.useRef(0),[o,i]=b.useState(0),[n,s]=b.useState("0:00"),[l,f]=b.useState(`${Math.floor(P/60)}:${(P%60).toString().padStart(2,"0")}`),d=b.useCallback(u=>{s(`${Math.floor(u/60)}:${(u%60).toString().padStart(2,"0")}`);const p=P-u;f(`${Math.floor(p/60)}:${(p%60).toString().padStart(2,"0")}`)},[]);return b.useEffect(()=>{function u(p){t.current&&(window.clearInterval(t.current),t.current=0,p&&e.onComplete())}return e.enabled?(r.current=Date.now(),t.current=window.setInterval(()=>{const p=Math.floor((Date.now()-r.current)/1e3);if(p>P){u(!0);return}d(p),i(p/P*100)},1e3)):(u(!1),d(0),i(0)),()=>window.clearInterval(t.current)},[e,d]),c.jsxs("div",{className:"relative w-full h-8 overflow-hidden font-bold bg-gray-200 rounded-md",children:[c.jsxs("div",{className:"absolute top-0 flex items-center justify-between w-full h-full px-2 text-black ",children:[c.jsx("div",{children:n}),c.jsx("div",{children:l})]}),c.jsxs("div",{className:"absolute top-0 flex items-center justify-between w-full h-full px-2 text-white bg-blue-500",style:{clipPath:`inset(0 ${100-o}% 0 0)`},children:[c.jsx("div",{children:n}),c.jsx("div",{children:l})]})]})}const U=e=>c.jsxs("tr",{className:e.focus?"border-y-2 border-green-500/50 text-2xl font-bold bg-green-500/20":"border-b",children:[c.jsx("td",{className:"py-3 text-center",children:e.heatNo}),c.jsx("td",{className:"text-center",children:e.className}),c.jsx("td",{className:"text-center",children:e.pilots[0]}),c.jsx("td",{className:"text-center",children:e.pilots[1]}),c.jsx("td",{className:"text-center",children:e.pilots[2]})]});function lt(){const{currentHeat:e,setCurrentHeat:t,heatList:r,startHeat:o,reloadHeatList:i,downloadHeatList:n,uploadLog:s}=me(),l=r.length,[f,d]=b.useState(!1);b.useEffect(()=>{e>0&&window.history.pushState({},"",`/${e}`)},[e]);const u=b.useCallback(()=>{f?d(!1):(d(!0),o())},[f,o]),p=b.useCallback(()=>{d(!1),t((e-1+l-1)%l+1)},[e,l,t]),y=b.useCallback(()=>{d(!1),t((e-1+1)%l+1)},[e,l,t]),v=e-1,w=r[(v+l-1)%l],g=r[v],x=r[(v+1)%l];return b.useEffect(()=>{function k(j){switch(j.key){case"1":u();break;case"2":p();break;case"3":y();break}}return window.addEventListener("keydown",k),()=>window.removeEventListener("keydown",k)},[u,p,y]),c.jsxs("div",{className:"container max-w-screen-md pt-4 mx-auto text-lg",children:[c.jsx("table",{className:"w-full mb-6 table-auto",children:c.jsxs("thead",{children:[c.jsxs("tr",{className:"border-b-2",children:[c.jsx("th",{className:"py-3",children:"Heat"}),c.jsx("th",{children:"Class"}),c.jsx("th",{children:"E1 / 5705"}),c.jsx("th",{children:"F1 / 5740"}),c.jsx("th",{children:"F4 / 5800"})]}),w&&c.jsx(U,{heatNo:(v+l-1)%l+1,className:w.className,pilots:w.pilots,focus:!1}),g&&c.jsx(U,{heatNo:v+1,className:g.className,pilots:g.pilots,focus:!0}),x&&c.jsx(U,{heatNo:(v+1)%l+1,className:x.className,pilots:x.pilots,focus:!1})]})}),c.jsx("div",{className:"w-full my-6",children:c.jsx(it,{enabled:f,onComplete:y})}),c.jsxs("div",{className:"flex justify-center gap-4 mt-6",children:[c.jsxs(z,{className:`py-6 text-xl ${f?"bg-red-500 hover:bg-red-500/90":"bg-green-600 hover:bg-green-600/90"} `,onClick:u,children:[f?"ストップ":"スタート",c.jsx("kbd",{className:"flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md",children:"1"})]}),c.jsxs(z,{className:"py-6 text-xl bg-slate-400 hover:bg-slate-400/90",onClick:p,children:["前のヒート",c.jsx("kbd",{className:"flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md",children:"2"})]}),c.jsxs(z,{className:"py-6 text-xl bg-blue-600 hover:bg-blue-600/90",onClick:y,children:["次のヒート",c.jsx("kbd",{className:"flex items-center justify-center w-6 h-6 ml-2 bg-gray-800 rounded text-md",children:"3"})]})]}),c.jsx("hr",{className:"my-6"}),c.jsxs("div",{className:"flex justify-center gap-4 text-gray-400",children:[c.jsx(z,{variant:"outline",size:"sm",onClick:i,children:"ヒートリスト再読み込み"}),c.jsx(z,{variant:"outline",size:"sm",onClick:n,children:"ヒートリスト再ダウンロード"}),c.jsx(z,{variant:"outline",size:"sm",onClick:s,children:"ログアップロード"})]})]})}he.createRoot(document.getElementById("root")).render(c.jsx(lt,{}));
