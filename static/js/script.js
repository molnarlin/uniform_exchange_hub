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
      defaultDate: new Date(2024, 1, 3),
      setDefaultDate: true
    };
    var elems = document.querySelector('.datepicker');
    var instance = M.Datepicker.init(elems, options);
    // instance.open();
    instance.setDate(new Date(2024, 2, 8));
  });
