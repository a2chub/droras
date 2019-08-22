var heats

function updateCurrent() {
  $.getJSON("/api/get_cur_heat", function (current) {
    console.log(current)
    heats.removeClass('table-success')
    $(heats.get(current.id - 1)).addClass('table-success')
  })
}

$(function () {
  $.getJSON("/api/get_race_data", function (data) {
    var prevClass = null;
    var trs = $(data).map(function (index, pilots) {
      var heat = index + 1
      var out = "<tr class='heat'>" +
        "<td>" + heat + "</td>" +
        "<td>" + pilots[0]["name"] + "</td>" +
        "<td>" + pilots[1]["name"] + "</td>" +
        "<td>" + pilots[2]["name"] + "</td>" +
        "</tr>"
      var klass = pilots[0]["class"]
      if (klass != prevClass) {
        out = "<tr><td colspan=4>" + klass + "</td></tr>" + out
        prevClass = klass
      }
      return out
    })
    $("#list").append($.makeArray(trs))
    heats = $(".heat")
    console.log(heats)
    updateCurrent()
    setInterval(updateCurrent, 20000)
  })
})
