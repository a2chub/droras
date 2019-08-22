$(function () {
  $.getJSON("/api/get_race_data", function (data) {
    var trs = $(data).map(function (index, pilots) {
      var heat = index + 1
      var klass = pilots[0]["class"]
      return "<tr>" +
        "<td>" + heat + "</td>" +
        "<td>" + klass + "</td>" +
        "<td>" + pilots[0]["name"] + "</td>" +
        "<td>" + pilots[1]["name"] + "</td>" +
        "<td>" + pilots[1]["name"] + "</td>" +
        "</tr>"
    })
    $("#list").append($.makeArray(trs))
  })
})
