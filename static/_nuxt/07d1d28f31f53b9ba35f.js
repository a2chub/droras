(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{218:function(t,e,r){var content=r(224);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(59).default)("5fd994ba",content,!0,{sourceMap:!1})},223:function(t,e,r){"use strict";var n=r(218);r.n(n).a},224:function(t,e,r){(t.exports=r(58)(!1)).push([t.i,"table[data-v-43e9fef4]{font-size:larger}td[data-v-43e9fef4],th[data-v-43e9fef4]{text-align:center}tr.active[data-v-43e9fef4]{font-size:larger;font-weight:700}.buttons[data-v-43e9fef4]{text-align:center}.buttons a[data-v-43e9fef4],.buttons button[data-v-43e9fef4]{margin:0 10px}#progress[data-v-43e9fef4]{margin-top:15px}#progress .progress-bar[data-v-43e9fef4]{font-size:larger}",""])},227:function(t,e,r){"use strict";r.r(e);r(48);var n,o=r(13),c=(r(14),r(83),r(77)),h=r.n(c),l={data:function(){return{timer:-1,progress:0,current:""}},validate:function(t){var e=t.params;return/^\d+$/.test(e.id)},computed:{heats:function(){var t=this.$store.state.heats.length;if(0!==t&&this.$store.state.current){for(var e=0|this.$store.state.current.heat,r=[],i=e-2;i<=e;i++){var n=(i+t)%t,o=this.$store.state.heats[n],c=o.find(function(p){return p.name}).class;r.push({index:n+1,class:c,pilots:o,active:i+1===e})}return r}},next:function(){var t=this.$store.state.heats.length;if(0===t||!this.$store.state.current)return"";var e=0|this.$store.state.current.heat;return"/".concat(e===t?1:e+1)},prev:function(){var t=this.$store.state.heats.length;if(0===t||!this.$store.state.current)return"";var e=0|this.$store.state.current.heat;return"/".concat(1===e?t:e-1)}},fetch:(n=Object(o.a)(regeneratorRuntime.mark(function t(e){var r,n;return regeneratorRuntime.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return r=e.store,n=e.params,e.$axios,t.next=3,r.dispatch("initRaces");case 3:return t.next=5,r.dispatch("initCurrent");case 5:return t.next=7,h.a.get("/api/"+n.id);case 7:case"end":return t.stop()}},t)})),function(t){return n.apply(this,arguments)}),beforeDestroy:function(){this.stop()},methods:{start:function(){var t=this;this.$axios.get("/api/start");var e=Date.now();this.timer=setInterval(function(){var r=(Date.now()-e)/1e3,p=Math.min(r/120*100,100);100===p&&t.stop(),t.progress=p,t.current="".concat(Math.round(r)," / ").concat(120-Math.round(r))},100)},stop:function(){clearInterval(this.timer)}}},f=(r(223),r(45)),component=Object(f.a)(l,function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"container"},[r("table",{staticClass:"table"},[t._m(0),r("tbody",{staticClass:"list"},t._l(t.heats,function(e){return r("tr",{key:e.index,class:{"table-success":e.active,active:e.active}},[r("td",[t._v(t._s(e.index))]),r("td",[t._v(t._s(e.class))]),t._l(e.pilots,function(e,n){return r("td",{key:n},[t._v(t._s(e.JDL_ID.match(/^J/)?e.name:"-"))])})],2)}),0)]),r("hr"),r("div",{staticClass:"buttons"},[r("button",{staticClass:"btn btn-lg btn-success",attrs:{id:"btn-start",type:"button"},on:{click:t.start}},[t._v("スタート音 "),r("kbd",[t._v("1")])]),r("nuxt-link",{staticClass:"btn btn-lg btn-secondary",attrs:{id:"btn-prev",role:"button",to:t.prev}},[t._v("前のヒート"),r("kbd",[t._v("2")])]),r("nuxt-link",{staticClass:"btn btn-lg btn-primary",attrs:{id:"btn-next",role:"button",to:t.next}},[t._v("次のヒート"),r("kbd",[t._v("3")])])],1),r("div",{staticClass:"progress",staticStyle:{height:"30px"},attrs:{id:"progress"}},[r("div",{staticClass:"progress-bar",style:{width:t.progress+"%"}},[t._v(t._s(t.current))])])])},[function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",[this._v("Heat")]),e("th",[this._v("Class")]),e("th",[this._v("E1: 5705")]),e("th",[this._v("F1: 5740")]),e("th",[this._v("F4: 5800")])])])}],!1,null,"43e9fef4",null);e.default=component.exports}}]);