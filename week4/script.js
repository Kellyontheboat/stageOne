function validateForm() {
  let agreeCheckbox = document.getElementById("agree");
  if (!agreeCheckbox.checked) {
    alert("Please check the checkbox first.");
    return false; // Prevent form submission
  }
  return true; // Allow form submission
}

