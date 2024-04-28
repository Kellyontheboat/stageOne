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
  // Redirect  to the URL appended the entered positive number
  window.location.href = "/square/" + inputValue;
  // Prevent form submission
  return false;
}

