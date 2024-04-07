// !Item1~4
const navContainer = document.querySelector('.nav-item-container');

for (let i = 1; i <= 4; i++) {
  // Create a new nav-item element
  const navItem = document.createElement('span');
  navItem.classList.add('nav-item');
  navItem.textContent = `Item ${i}`;

  // Append the grid item to the grid container
  navContainer.appendChild(navItem);
}

// !SmallBoxes(Tab)
const gridContainerTab = document.querySelector('.grid-container-tab');

// Iterate over 3 items
for (let i = 1; i <= 3; i++) {
  // Create a new grid item element
  const gridItem = document.createElement('div');
  gridItem.classList.add('grid-item-tab');

  // Create a img element
  const img = document.createElement('img');
  img.src = 'dune.jpeg';

  // Create a title element
  const title = document.createElement('span');
  title.classList.add('promotion');
  title.textContent = `Promotion ${i}`;

  // Append the title to the grid item
  gridItem.appendChild(img);
  gridItem.appendChild(title);

  // Append the grid item to the grid container
  gridContainerTab.appendChild(gridItem);
}

// !BigBoxes(Img)
const gridContainerImg = document.querySelector('.grid-container-img');

// Iterate over 10 items
for (let i = 1; i <= 10; i++) {
  // Create a new grid item element
  const gridItem = document.createElement('div');
  gridItem.classList.add('grid-item-img');

  // Create a title element
  const title = document.createElement('div');
  title.classList.add('title');
  title.textContent = `Title ${i}`;

  const star = document.createElement('i');
  star.classList.add('fa-solid', 'fa-star');

  // Append the title to the grid item
  gridItem.appendChild(title);
  gridItem.appendChild(star);

  // Append the grid item to the grid container
  gridContainerImg.appendChild(gridItem);
}

// !burger menu 

const mobileNavContainer = document.querySelector('.mobile-nav-item-container');

for (let i = 1; i <= 4; i++) {
  // Create a new nav-item element
  const navItem = document.createElement('div');
  navItem.classList.add('mobile-nav-item');
  navItem.textContent = `Item ${i}`;

  // Append the grid item to the grid container
  mobileNavContainer.appendChild(navItem);
}
