      var dt_from = "2014/11/01 00:34:44";
      var dt_to = "2014/11/24 16:37:43";

      $('.slider-time').html(dt_from);
      $('.slider-time2').html(dt_to);
      var min_val = Date.parse(dt_from)/1000;
      var max_val = Date.parse(dt_to)/1000;

      function zeroPad(num, places) {
        var zero = places - num.toString().length + 1;
        return Array(+(zero > 0 && zero)).join("0") + num;
      }
      function formatDT(__dt) {
          var year = __dt.getFullYear();
          var month = zeroPad(__dt.getMonth()+1, 2);
          var date = zeroPad(__dt.getDate(), 2);
          var hours = zeroPad(__dt.getHours(), 2);
          var minutes = zeroPad(__dt.getMinutes(), 2);
          var seconds = zeroPad(__dt.getSeconds(), 2);
          return year + '-' + month + '-' + date + ' ' + hours + ':' + minutes + ':' + seconds;
      };


      $("#slider-range").slider({
          range: true,
          min: min_val,
          max: max_val,
          step: 10,
          values: [min_val, max_val],
          slide: function (e, ui) {
              var dt_cur_from = new Date(ui.values[0]*1000); //.format("yyyy-mm-dd hh:ii:ss");
              $('.slider-time').html(formatDT(dt_cur_from));

              var dt_cur_to = new Date(ui.values[1]*1000); //.format("yyyy-mm-dd hh:ii:ss");                
              $('.slider-time2').html(formatDT(dt_cur_to));
          }
      });

