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
    var options = {
      setDefaultDate: false
    };
    var elems = document.querySelector('.datepicker');
    var instance = M.Datepicker.init(elems, options);
    // instance.open();
    instance.setDate(new Date());
  });
