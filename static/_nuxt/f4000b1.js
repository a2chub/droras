(window.webpackJsonp=window.webpackJsonp||[]).push([[4],{281:function(t,e,n){var content=n(295);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(88).default)("334cbb4b",content,!0,{sourceMap:!1})},294:function(t,e,n){"use strict";n(281)},295:function(t,e,n){var r=n(87)((function(i){return i[1]}));r.push([t.i,"table[data-v-2de86ecd]{font-size:larger}td[data-v-2de86ecd],th[data-v-2de86ecd]{text-align:center}tr.active[data-v-2de86ecd]{font-size:larger;font-weight:700}.buttons[data-v-2de86ecd]{text-align:center}.buttons a[data-v-2de86ecd],.buttons button[data-v-2de86ecd]{margin:0 10px}#progress[data-v-2de86ecd]{margin-top:15px}#progress .progress-bar[data-v-2de86ecd]{font-size:larger}",""]),r.locals={},t.exports=r},299:function(t,e,n){"use strict";n.r(e);n(11),n(149),n(22),n(113),n(1),n(35),n(14);var r={fetch:function(t){var e=t.store,n=t.params,r=t.$axios;e.dispatch("initRaces"),r.get("/api/"+n.id)},asyncData:function(t){return{currentHeat:t.params.id}},data:function(){return{timer:-1,currentHeat:1,progress:0,currentTime:""}},computed:{heats:function(){var t=this.$store.state.heats.length;if(0!==t){for(var e=0|this.currentHeat,n=[],i=e-2;i<=e;i++){var r=(i+t)%t,o=this.$store.state.heats[r],c=o.find((function(p){return p.name})).class;n.push({index:r+1,class:c,pilots:o,active:i+1===e})}return n}}},beforeMount:function(){window.addEventListener("keydown",this.onKeyDown)},beforeDestroy:function(){this.stop(),window.removeEventListener("keydown",this.onKeyDown)},methods:{start:function(){var t=this;this.stop(),this.$axios.get("/api/start");var e=Date.now();this.timer=setInterval((function(){var n=(Date.now()-e)/1e3,p=Math.min(n/165*100,100);100===p&&(t.stop(),t.goNext()),t.progress=p,t.currentTime="".concat(Math.round(n)," / ").concat(165-Math.round(n))}),100)},stop:function(){clearInterval(this.timer)},next:function(){var t=this.$store.state.heats.length;if(0===t)return"";var e=0|this.currentHeat;return"/".concat(e===t?1:e+1)},goNext:function(){this.$router.push(this.next())},prev:function(){var t=this.$store.state.heats.length;if(0===t)return"";var e=0|this.currentHeat;return"/".concat(1===e?t:e-1)},goPrevious:function(){this.$router.push(this.prev())},onKeyDown:function(t){switch(t.key){case"1":this.start();break;case"2":this.goPrevious();break;case"3":this.goNext()}}}},o=(n(294),n(64)),component=Object(o.a)(r,(function(){var t=this,e=t._self._c;return e("div",{staticClass:"container"},[e("table",{staticClass:"table"},[t._m(0),e("tbody",{staticClass:"list"},t._l(t.heats,(function(n){return e("tr",{key:n.index,class:{"table-success":n.active,active:n.active}},[e("td",[t._v(t._s(n.index))]),e("td",[t._v(t._s(n.class))]),t._l(n.pilots,(function(n,r){return e("td",{key:r},[t._v(t._s(n.JDL_ID.match(/^J/)?n.name:"-"))])}))],2)})),0)]),e("hr"),e("div",{staticClass:"buttons"},[e("button",{staticClass:"btn btn-lg btn-success",attrs:{type:"button"},on:{click:t.start}},[t._v("スタート音 "),e("kbd",[t._v("1")])]),e("nuxt-link",{staticClass:"btn btn-lg btn-secondary",attrs:{role:"button",to:t.prev()}},[t._v("前のヒート"),e("kbd",[t._v("2")])]),e("nuxt-link",{staticClass:"btn btn-lg btn-primary",attrs:{role:"button",to:t.next()}},[t._v("次のヒート"),e("kbd",[t._v("3")])])],1),e("div",{staticClass:"progress",staticStyle:{height:"30px"},attrs:{id:"progress"}},[e("div",{staticClass:"progress-bar",style:{width:t.progress+"%"}},[t._v(t._s(t.currentTime))])])])}),[function(){var t=this,e=t._self._c;return e("thead",[e("tr",[e("th",[t._v("Heat")]),e("th",[t._v("Class")]),e("th",[t._v("E1: 5705")]),e("th",[t._v("F1: 5740")]),e("th",[t._v("F4: 5800")])])])}],!1,null,"2de86ecd",null);e.default=component.exports}}]);