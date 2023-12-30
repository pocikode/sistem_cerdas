/*!

=========================================================
* Soft UI Dashboard Tailwind - v1.0.5
=========================================================

* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-tailwind
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (site.license)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
var page = window.location.pathname.split("/").pop().split(".")[0];
var aux = window.location.pathname.split("/");
// var to_build = (aux.includes('pages')?'../':'./');
var to_build = '/';
var root = window.location.pathname.split("/")
if (!aux.includes("pages")) {
  page = "dashboard";
}

loadStylesheet(to_build + "static/css/perfect-scrollbar.css");
loadJS(to_build + "static/js/perfect-scrollbar.js", true);

if (document.querySelector("nav [navbar-trigger]")) {
  loadJS(to_build + "static/js/navbar-collapse.js", true);
}

if (document.querySelector("[data-target='tooltip']")) {
  loadJS(to_build + "static/js/tooltips.js", true);
  loadStylesheet(to_build + "static/css/tooltips.css");
}

if (document.querySelector("[nav-pills]")) {
  loadJS(to_build + "static/js/nav-pills.js", true);
}

if (document.querySelector("[dropdown-trigger]")) {
  loadJS(to_build + "static/js/dropdown.js", true);

}

if (document.querySelector("[fixed-plugin]")) {
  loadJS(to_build + "static/js/fixed-plugin.js", true);
}

if (document.querySelector("[navbar-main]")) {
  loadJS(to_build + "static/js/sidenav-burger.js", true);
  loadJS(to_build + "static/js/navbar-sticky.js", true);
}

if (document.querySelector("canvas")) {
  loadJS(to_build + "static/js/chart-1.js", true);
  loadJS(to_build + "static/js/chart-2.js", true);
}

function loadJS(FILE_URL, async) {
  let dynamicScript = document.createElement("script");

  dynamicScript.setAttribute("src", FILE_URL);
  dynamicScript.setAttribute("type", "text/javascript");
  dynamicScript.setAttribute("async", async);

  document.head.appendChild(dynamicScript);
}

function loadStylesheet(FILE_URL) {
  let dynamicStylesheet = document.createElement("link");

  dynamicStylesheet.setAttribute("href", FILE_URL);
  dynamicStylesheet.setAttribute("type", "text/css");
  dynamicStylesheet.setAttribute("rel", "stylesheet");

  document.head.appendChild(dynamicStylesheet);
}

// SENTIMENT
var options = {
  // colors: ['#F44336', '#E91E63', '#9C27B0'],
  series: [{
  name: 'Anies-Imin',
  data: [6346, 24836, 15868]
}, {
  name: 'Prabowo-Gibran',
  data: [9674, 29113, 9847]
}, {
  name: 'Ganjar-Mahfud',
  data: [8142, 18750, 8736]
}],
  chart: {
  type: 'bar',
  height: 350
},
plotOptions: {
  bar: {
    horizontal: false,
    columnWidth: '55%',
    endingShape: 'rounded'
  },
},
dataLabels: {
  enabled: false
},
stroke: {
  show: true,
  width: 2,
  colors: ['transparent']
},
xaxis: {
  categories: ['Negative', 'Neutral', 'Positive'],
},
yaxis: {
  title: {
    text: 'Tweets'
  }
},
fill: {
  opacity: 1
},
tooltip: {
  y: {
    formatter: function (val) {
      return "Tweets"
    }
  }
}
};

var chart = new ApexCharts(document.querySelector("#sentiment-chart"), options);
chart.render();
