<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<style>
table {
  font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
  font-size: 14px;
  text-align: left;
  border-collapse: collapse;
  border-radius: 20px;
  box-shadow: 0 0 0 ;
}
th {
  padding: 10px 8px;
  background: white;
}
table th:first-child {
  border-top-left-radius: 20px;
}
table th:last-child {
  border-top-right-radius: 20px;
}
td {
  padding: 8px;
  background: white;
}
table td:first-child {
  border-bottom-left-radius: 20px;
}
table td:last-child {
  border-bottom-right-radius: 20px;
}

.table-wrap{
	overflow-x:auto;
}	
table.table-1 {
    border-collapse: collapse;
    border-spacing: 0;
    width: 100%;
}
table.table-1 tr {
	background-color: #f8f8f8;
}
table.table-1 th, table.table-1 td {
	text-align: left;
    padding: 8px;
    border: 1px solid #ddd;
}

table.table-1 th{
	font-weight: bold;
}
#myTable tr.header, #myTable tr:hover {
    background-color: #f1f1f1
}

#myInput {
    width: 100%;
    font-size: 16px;
    padding: 12px 20px 12px 40px;
     margin-bottom: 12px;
}

.parent {
    width: 35%;
    height: 90%;
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    align-content: center; 
    /* justify-content: center;  */
    overflow: auto;  
}
.form-group {
  background: #d0ebc1;
  resize: both;
  max-width: 12em;
  max-height: 12em;
  min-width: 6em;
}

#myTable {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  align-content: center; 
  resize: both;
  max-width: 12em;
  margin: 0 auto;
}


</style>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">SecSearch</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav">
      <a class="nav-item nav-link active" href="#">About <span class="sr-only"></span></a>
      <a class="nav-item nav-link" href="#">Crawler</a>
    </div>
  </div>
</nav>

<div class='table-wrap'>
<table id="myTable" class='table-1'>
<div class="parent">
  <form role="form">
    <div class="form-group"></div>
      <input type="text" class="form-control" id="myInput" onkeyup="myFunction()" placeholder="Поиск по заголовку...">
    </div>
  </form>
</div>
<tr class="header">
<th>ID</th>
<th>Name</th>
<th>Count room</th>
<th>Address</th>
<th>Area</th>
<th>Price</th>
<th>Price currency</th>
<th>Phone Number</th>
<th>URL</th>
</tr>
%for col in result:
  <tr>
  <td>{{col[0]}}</td>
  <td>{{col[1]}}</td>
  <td>{{col[2]}}</td>
  <td>{{col[3]}}</td>
  <td>{{col[4]}}</td>
  <td>{{col[5]}}</td>
  <td>{{col[6]}}</td>
  <td>{{col[7]}}</td>
  <td>{{col[8]}}</td>
  </tr>
%end
</table>
</div>
<script>
function myFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}


function makeEditable(e) {
    var cell = e.target;
    if (cell.dataset.editing !== 'true') {
      cell.dataset.editing = true;
      var text = cell.innerHTML;
      cell.innerHTML = '';
      var input = document.createElement('input');
      input.addEventListener('blur', makeNonEditable);
      input.type = 'text'
      input.value = text;
      cell.appendChild(input);
    } 
}

function makeNonEditable(e) {
  var input = e.target;
  var taxt = input.value;
  var cell = input.parentElement;
  if (cell.dataset.editing === 'true') {
    cell.dataset.editing = false;
  }
}


table = document.getElementById("myTable")
var tr = table.getElementsByTagName("tr")
for (i = 0; i < tr.length; i++) {
  td = tr[i].getElementsByTagName("td")[0];
  if (td) {
    td.addEventListener('mousedown', makeEditable);
  }
}
</script>
</html>