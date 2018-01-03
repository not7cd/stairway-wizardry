'use strict'

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

  $('#nextHours').click(function () {
    const n = $('#selectHours option:selected').next()
    if (n) {
      n.prop('selected', true)
      .prev()
      .prop('selected', false)
      .parent().trigger('change')
    }
  })

  $('#prevHours').click(function () {
    const p = $('#selectHours option:selected').prev()
    console.log(p)
    if (p) {
      p.prop('selected', true)
      .next()
      .prop('selected', false)
      .parent().trigger('change')
    }
  })

  $('#nextWeekday').click(function () {
    const n = $('#selectWeekday option:selected').next()
    if (n) {
      n.prop('selected', true)
      .prev()
      .prop('selected', false)
      .parent().trigger('change')
    }
  })

  $('#prevWeekday').click(function () {
    const p = $('#selectWeekday option:selected').prev()
    console.log(p)
    if (p) {
      p.prop('selected', true)
      .next()
      .prop('selected', false)
      .parent().trigger('change')
    }
  })

  $('path').popover({html: true, trigger: 'hover', placement: 'top' })

  function updatePlan (lessons) {
    console.log(lessons)
    d3.selectAll('.classroom')
      .style('fill', '')
    d3.select('#plan').selectAll('path')
      .attr('data-content', d => d ? `${d.id.split('_').join(' ')}` : '')
      .attr('data-original-title', '')
      .classed('occupied', false)
      .data(lessons, d => d ? d.id : null)
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
    return this.id.startsWith('path') ? null : { 'id': this.id }
  })

  let week_
  let hours_
  fetch('/data')
    .then(res => res.json())
    .then(week => {
      week_ = week
      hours_ = week[0]

      let s = $('#selectHours')
      for (var hour in hours_) {
        s.append(`<option>${hour}</option>`)
      }
      s.trigger('change')
      const getWeek = function (w) {
        console.log(week_)
        return week_[w]
      }
      const getHours = _ => { return hours_ }

      $('#selectHours').on('change', function () {
        updatePlan(getWeek($('#selectWeekday').val())[this.value])
      })

      $('#selectWeekday').prop('disabled', false)
      .on('change', function () {
        $('#selectHours').trigger('change')
      })
    })
    .then(_ => $('#selectHours').trigger('change'))

  const data = fetch('/data')
    .then(res => res.json())
})
