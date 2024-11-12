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

document.getElementById('addMoreBtn').addEventListener('click', function() {
    var productFields = document.getElementById('productFields');
    var newField = document.createElement('div');
    newField.className = 'productField';
    newField.innerHTML = `
        <label for="school_name">School Name:</label>
        <input type="text" id="school_name" name="school_name[]" required><br>
        
        <label for="product_name">Item's name:</label>
        <input type="text" id="product_name" name="product_name[]" required><br>
        
        <label for="product_size">Item's size:</label>
        <input type="text" id="product_size" name="product_size[]" required><br>
        
        <label for="product_colour">Item's colour:</label>
        <input type="text" id="product_colour" name="product_colour[]" required><br>
    `;
    productFields.appendChild(newField);
});

function confirmDelete() {
  return confirm("Are you sure you want to delete this user?");
}