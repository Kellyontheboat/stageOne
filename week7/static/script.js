document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("signupButton").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default form submission
    submitForm();

  function submitForm() {
    let nameInput = document.getElementById("signup_name").value;
    let usernameInput = document.getElementById("signup_username").value;
    let passwordInput = document.getElementById("signup_password").value;

    if (!nameInput || !usernameInput || !passwordInput) {
      alert("Please fill all fields.");
      return false; // prevent form submission
    }
    // If all fields are filled,submit the form
    document.getElementById("signupForm").submit();
  }
 })
});

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

async function searchUser() {
  const username = document.getElementById("search_username").value;

  // Check if the foundResult element exists, if not, create it
  let foundResult = document.getElementById("found_result");
  if (!foundResult) {
    foundResult = document.createElement("div");
    foundResult.id = "found_result";
    document.getElementById("search_container").appendChild(foundResult); // Append it to the body or a suitable parent element
  }

  try {
    const response = await fetch(`/member?q=${username}`);
    const result = await response.json();

    if (result.data && result.data !== "null") {
      // Assuming 'data' is an object
      const userData = result.data;
      const displayText = `${userData.name}(${userData.username})`;
      foundResult.innerHTML = displayText;
    } else {
      foundResult.innerHTML = "No Data.";
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    foundResult.innerHTML = "Error fetching user data.";
  }
}

async function updateName() {
  const newName = document.getElementById("update_name").value;
  if (newName) {
    try {
      const response = await fetch(`/api/member?new_name=${newName}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newName })
      });

      const data = await response.json();
      console.log(data);
      const updateResult = document.createElement("div");
      document.getElementById("update_container").appendChild(updateResult);
      if (response.ok) {
        document.getElementById('welcome_message').innerText = newName + '，歡迎登入系統';
        updateResult.innerHTML = "更新成功";
      } else {
        updateResult.innerHTML = "更新失敗";
      }
    } catch (error) {
      console.error('Error:', error);
    }

  }
}
