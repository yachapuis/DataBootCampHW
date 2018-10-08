// Set a variable to the data set from data.js
var tableData = data;


// Get element by tbody, input/id and button/id
var $tbody = document.querySelector("tbody");
var $dateInput = document.querySelector("#datetime");
var $cityInput = document.querySelector("#city");
var $stateInput = document.querySelector("#state");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");
var $searchBtn = document.querySelector("#search");

// Add an event listener to the "Search Button", click to call the function handleSearchButtonClick
$searchBtn.addEventListener("click", handleSearchButtonClick);

// renderTable renders the filteredAddresses to the tbody
function renderTable() {
  $tbody.innerHTML = "";
  for (var i = 0; i < tableData.length; i++) {
    // Get the current address object and its fields
    var address = tableData[i];
    console.log(address)
    var fields = Object.keys(address);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the address object, create a new cell at set its inner text to be the current value at the current address's field
      var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = address[field];
    }
  }
}

function handleSearchButtonClick() {
  // Format the user's search by removing leading and trailing whitespace, lowercase the string
  var filterDate = $dateInput.value;
  var filterCity = $cityInput.value.trim().toLowerCase();
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCountry = $countryInput.value.trim().toLowerCase();
  var filterShape = $shapeInput.value.trim().toLowerCase();

  // Set filteredAddresses to an array of all addresses whose "state" matches the filter
  if (filterDate != ""){
    tableData = data.filter(function(address){
      var addressDate = address.datetime; 
      // If true, add the address to the filteredAddresses, otherwise don't add it to filteredAddresses
    return addressDate === filterDate;
    });
  }
  else {tableData};
  
  if(filterCity != ""){
    tableData = tableData.filter(function(address){
      var addressCity = address.city;
      return addressCity === filterCity;
    });
  }
  else{tableData};

  if(filterState != ""){
    tableData = tableData.filter(function(address){
      var addressState = address.state;
      return addressState === filterState;
    });
  }
  else{tableData};

  if(filterCountry != ""){
    tableData = tableData.filter(function(address){
      var addressCountry = address.country;
      return addressCountry === filterCountry;
    });
  }
  else{tableData};

  if(filterShape != ""){
    tableData = tableData.filter(function(address){
      var addressShape = address.shape;
      return addressShape === filterShape;
    });
  }
  else{tableData};

  renderTable();

}

// Render the table for the first time on page load
renderTable();

//Add pagination to the table to show 10 -100 entries per page
$(document).ready(function() {
  $('#table').DataTable();
});