let globalUrls;
let globalTitles;
async function fetchUrls() {
  const response = await fetch('spot.csv');
  const csvData = await response.text();
  const lines = csvData.split('\n');
  const urls = [];
  const titles = [];

  lines.forEach(line => {
    const columns = line.split(',');
    const url = columns[4].trim(); //URL is in the fifth column
    const title = columns[0].trim(); //Title is in the first column
    urls.push(url);
    titles.push(title);
  });

  globalUrls = urls;
  globalTitles = titles;

  // Call the function to create elements once globalUrls is available
  createSmallBoxes();
  createBigBoxes();
}

function createSmallBoxes() {
  // !SmallBoxes(Tab)
  const gridContainerTab = document.querySelector('.grid-container-tab');

  // Iterate over the globalUrls array
  for (let i = 0; i < 3; i++) {
    // Create a new grid item element
    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item-tab');

    // Create an img element
    const img = document.createElement('img');
    img.src = globalUrls[i];

    // Create a title element
    const title = document.createElement('span');
    title.classList.add('promotion');
    title.textContent = globalTitles[i];

    // Append the title to the grid item
    gridItem.appendChild(img);
    gridItem.appendChild(title);

    // Append the grid item to the grid container
    gridContainerTab.appendChild(gridItem);
  }
}


function createBigBoxes() {
  // !BigBoxes(Img)
  const gridContainerImg = document.querySelector('.grid-container-img');

  // Iterate over the items in globalUrls starting from the 4th item
  for (let i = 3; i < globalUrls.length; i++) {
    // Create a new grid item element
    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item-img');

    console.log(globalUrls[i]);
    // Set the background image to the URL
    gridItem.style.backgroundImage = `url('${globalUrls[i]}')`; // mind the Url syntax
    gridItem.style.backgroundSize = 'cover';
    gridItem.style.backgroundPosition = 'center';
    gridItem.style.position = 'relative';
    gridItem.style.overflow = 'hidden';

    // Create a title element
    const title = document.createElement('div');
    title.classList.add('title');
    title.textContent = globalTitles[i]; // Adjusted index to start from 4

    const star = document.createElement('i');
    star.classList.add('fa-solid', 'fa-star');

    // Append the title to the grid item
    gridItem.appendChild(title);
    gridItem.appendChild(star);

    // Append the grid item to the grid container
    gridContainerImg.appendChild(gridItem);
  }
}

// Call fetchUrls function to fetch the data and create elements once data is available
fetchUrls();

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
