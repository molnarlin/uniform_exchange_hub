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
    var elems = document.querySelectorAll('.datepicker');
    if (elems.length > 0) {
      elems.forEach(function(elem) {
          var instance = M.Datepicker.init(elem, options);
          instance.setDate(new Date());
      });
    } else {
      console.error('No element found with the class "datepicker"');
    }
});
