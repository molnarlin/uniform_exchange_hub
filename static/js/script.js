document.addEventListener('DOMContentLoaded', function() {
  var headers = document.querySelectorAll('.collapsible-header');
  
  headers.forEach(function(header) {
      header.addEventListener('click', function() {
          var body = this.nextElementSibling;
          
          if (body.style.display === 'block') {
              body.style.display = 'none';
          } else {
              body.style.display = 'block';
          }
      });
  });
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
  });
