(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{280:function(t,e,n){var content=n(288);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(85).default)("6fbea66b",content,!0,{sourceMap:!1})},287:function(t,e,n){"use strict";n(280)},288:function(t,e,n){var o=n(84)(!1);o.push([t.i,"#__layout,#__nuxt,body,html{background-color:#000}#__layout,#__nuxt,.bg,body,html{width:100%;height:100%;overflow:hidden}.bg{display:flex}.name{color:#fff;width:33.3333%;font-family:sans-serif;text-align:center;font-size:20px;font-weight:700;margin-top:20px}",""]),t.exports=o},294:function(t,e,n){"use strict";n.r(e);n(1);var o={computed:{pilots:function(){var t=0|this.$store.state.current.heat;return this.$store.state.heats.filter((function(e,n){return n+1===t}))[0]}},created:function(){this.$store.dispatch("initRaces"),this.$store.dispatch("initCurrent")}},r=(n(287),n(60)),component=Object(r.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"bg"},t._l(t.pilots,(function(e,o){return n("div",{key:o,staticClass:"name"},[t._v("\n    "+t._s(e.name)+"\n  ")])})),0)}),[],!1,null,null,null);e.default=component.exports}}]);