$(document).ready(function () {
  var stringToColour = function (str) {
    var hash = 0
    for (var i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash)
    }
    var colour = '#'
    for (var i = 0; i < 3; i++) {
      var value = (hash >> (i * 8)) & 0xFF
      colour += ('00' + value.toString(16)).substr(-2)
    }
    return colour
  }

  $('#selectLevel').on('change', function () {
    $('.level').hide()
    $($("input[name='selectLevel']:checked").val()).show()
  })
  $("input[value='#level_1']").button('checked', true).parent().addClass('active').trigger('change')

  $('path').popover({html: true, trigger: 'hover', placement: 'top' })

  function updatePlan (lessons) {
    console.log(lessons)
    d3.selectAll('.classroom')
      .style('fill', '')
    d3.select('#plan').selectAll('path')
      .attr('data-content', '')
      .attr('data-original-title', '')
      .classed('occupied', false)
      .data(lessons, d => d ? d.id : this.id)
      .classed('classroom', true)
      .classed('occupied', true)
      .style('fill', d => stringToColour(d.p))
      .attr('data-content', d => {
        return `<i>${d.p.split('_').join(' ')}</i><br>${d.n}<ul><li>${d.o.join('</li><li>')}</li></ul>`
      })
      .attr('data-original-title', d => `${d.id.split('_').join(' ')}`)
  }

  function setTime (weekday, hours) {
    data.then(d => {
      console.log(d[weekday][hours])
      updatePlan(d[weekday][hours])
      return d
    })
  }

  d3.select('#plan').selectAll('path')
  .datum(function () {
    return { 'id': this.id }
  })

  fetch('/data')
    .then(res => res.json())
    .then(week => week[0])
    .then(hours => {
      s = $('#selectHours')
      s.on('change', function () {
        updatePlan(hours[this.value])
      })
      for (var hour in hours) {
        s.append(`<option>${hour}</option>`)
      }
      return hours['10:00-10:45']
    })
    .then(lessons => updatePlan(lessons))

  const data = fetch('/data')
    .then(res => res.json())
})
