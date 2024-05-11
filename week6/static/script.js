function submitForm() {
  //event.preventDefault();
  let nameInput = document.getElementById("name").value;
  let usernameInput = document.getElementById("username").value;
  let passwordInput = document.getElementById("password").value;

  if (!nameInput || !usernameInput || !passwordInput){
    alert("Please fill all fields.");
  }
}

function validateForm() {
  let agreeCheckbox = document.getElementById("agree");
  if (!agreeCheckbox.checked) {
    alert("Please check the checkbox first.");
    return false; // Prevent form submission
  }
  return true; // Allow form submission
}


function updateFormActionAndValidate() {
  let inputValue = document.getElementById('enter_int').value;
  // Check if the input is empty or not a number
  if (isNaN(inputValue)) {
    alert("Please enter a positive integer");
    return false;
  }

  // Convert the input to a number and check if it's a positive integer
  let numberValue = Number(inputValue);
  if (!Number.isInteger(numberValue) || numberValue <= 0) {
    alert("Please enter a positive integer");
    return false;
  }

  // Redirect to the URL with the entered positive number as a query parameter
  window.location.href = "/square/" + inputValue;
}

// function validInt() {
//   let inputValue = document.getElementById('enter_int').value;
//   // Check if the input is empty or not a number
//   if (inputValue === "" || isNaN(inputValue)) {
//     alert("Please enter a positive integer");
//     return false; // Prevent form submission
//   }
//   // Convert the input to a number and check if it's a positive integer
//   let numberValue = Number(inputValue);
//   if (!Number.isInteger(numberValue) || numberValue <= 0) {
//     alert("Please enter a positive integer");
//     return false; // Prevent form submission
//   }
//   // Redirect  to the URL appended the entered positive number
//   window.location.href = "/square/" + inputValue;
//   // Prevent form submission
//   return false;
// }

