function validateForm() {
  let agreeCheckbox = document.getElementById("agree");
  if (!agreeCheckbox.checked) {
    alert("Please check the checkbox first.");
    return false; // Prevent form submission
  }
  return true; // Allow form submission
}


function validInt() {
  let inputValue = document.getElementById('enter_int').value;
  // Check if the input is empty or not a number
  if (inputValue === "" || isNaN(inputValue)) {
    alert("Please enter a positive integer");
    return false; // Prevent form submission
  }
  // Convert the input to a number and check if it's a positive integer
  let numberValue = Number(inputValue);
  if (!Number.isInteger(numberValue) || numberValue <= 0) {
    alert("Please enter a positive integer");
    return false; // Prevent form submission
  }
  // No need to redirect here if the input is valid
  return true; // Allow form submission
}



// function validInt() {
//   let inputValue = document.getElementById('enter_int').value;
//   if (isNaN(inputValue) || parseInt(inputValue) <= 0 || parseInt(inputValue) % 1 !== 0) {
//     alert("Please enter a positive integer");
//     return false; // Prevent form submission
//   }
//   //window.location.href = "/square/" + inputValue;
//   return true; // Allow form submission
  
// }

// 