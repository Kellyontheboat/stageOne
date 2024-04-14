// !第一題
function findAndPrint(messages, currentStation) {
  const station = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nanjing Fuxing', 'Songjiang Nanjing', 'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall', 'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin', 'Qizhang', 'Xindian City Hall', 'Xindian']
  const sanitizedStation = station.map(stationName => stationName.replace(/[ ,.]/g, '')) //去除每一站名中的空格和標點符號
  const sanitizedCurStat = currentStation.replace(/[ ,.]/g, '')
  let minDifference = station.length //先設定最小差距為所有站名的數量
  let difference = Infinity
  let closestFriend = null

    for (let friend in messages) { //遍歷每個朋友的訊息
      const sanitizedMessage = messages[friend].replace(/[ ,.]/g, '') //去除訊息中的空格和標點符號
      let foundStation = false //設定一個狀態，若訊息中的站名找到配對則停止遍歷sanitizedStation

      //但是若朋友在xiaoBitan，則直接計算與朋友的差距
      if (sanitizedMessage.includes('Xiaobitan')) {
        const qizhangIndex = sanitizedStation.indexOf('Qizhang')
        const satation2 = sanitizedStation.slice(0); // Make a copy of sanitizedStation
        satation2.splice(qizhangIndex + 1, 0, 'Xiaobitan'); // Array Insert Xiaobitan after Qizhang
        difference = Math.abs(satation2.indexOf('Xiaobitan') - satation2.indexOf(sanitizedCurStat))
        if ((satation2.indexOf(sanitizedCurStat))  > satation2.indexOf('Xiaobitan')) { //如果訊息中包含或者當前站名在Qizhang之後
          difference = difference + 1
        }
          if (difference < minDifference) { //如果遍歷的朋友訊息中的站名的差距小於最小差距，則更新最小差距和最接近的朋友
            minDifference = difference
            closestFriend = friend
          }
          foundStation = true
        } else {

      //接著從sanitizedStaion代入每個站名，看是否比對上朋友所在的站
      for (const stationName of sanitizedStation) { //遍歷sanitizedStation中每個站

      if (sanitizedMessage.includes(stationName)) { //如果訊息中包含站名
        difference = Math.abs(sanitizedStation.indexOf(sanitizedCurStat) - sanitizedStation.indexOf(stationName)); //計算與朋友訊息中的站名序號差距
        if (difference < minDifference) { //如果遍歷的朋友訊息中的站名的差距小於最小差距，則更新最小差距和最接近的朋友
          minDifference = difference;
          closestFriend = friend;
        } 
        foundStation = true
        break; // Exit the loop since we found a matching station 

      }else{continue} //如果訊息中不包含站名，則繼續遍歷下一站點

  }

      if (foundStation) { // Check if station is found in the message
        continue; // Move to the next friend，otherwise will continue to the next station 
      }
    }
  }
  console.log(closestFriend)
}

  const messages = {
  "Bob": "I'm at Ximen MRT station.", 
  "Mary": "I have a drink near Jingmei MRT station.",
  "Copper": "I just saw a concert at Taipei Arena.",
  "Leslie": "I'm at home near Xiaobitan station.",
  "Vivian": "I'm at Xindian station waiting for you."
  }

findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian

// !第二題

// Define the createBookingSystem function to encapsulate the booking system logic
function createBookingSystem() {
  const bookedTimes = {};

  // Initialize the booked times array for each consultant
  function initializeBookedTimes(consultants) {
    consultants.forEach(consultant => {
      bookedTimes[consultant.name] = new Array(24).fill(false);
      // {Jonn: Array(24).fill(false), Bob: Array(24).fill(false), Jenny: Array(24).fill(false)}
    });
  }

  // Define the book function
  function book(consultants, hour, duration, criteria) {
    // Check if consultant is available for the given hour and duration
    function isAvailable(consultant, hour, duration) {
      const bookedSlots = bookedTimes[consultant.name];
      for (let i = hour; i < hour + duration; i++) {
        if (bookedSlots[i]) {
          return false; // Overlapping booking found
        }
      }
      return true; // No overlapping booking found
    }

    // Filter available consultants
    let availableConsultants = consultants.filter(consultant => {
      // Check if consultant is available for the given hour and duration
      return isAvailable(consultant, hour, duration);
    });

    if (availableConsultants.length === 0) {
      console.log("No Service");
      return;
    }

    availableConsultants.sort((a, b) => {
      // Sort by criteria
      if (criteria === "price") {
        return a.price - b.price;
      } else if (criteria === "rate") {
        return b.rate - a.rate;
      }
    });

    const selectedConsultant = availableConsultants[0];
    console.log(selectedConsultant.name);

    // Update booked times for the selected consultant
    const bookedSlots = bookedTimes[selectedConsultant.name];
    for (let i = hour; i < hour + duration; i++) {
      bookedSlots[i] = true;
    }
  }

  return { initializeBookedTimes, book };
}

// Create a booking system
const bookingSystem = createBookingSystem();

const consultants = [
  { "name": "John", "rate": 4.5, "price": 1000 },
  { "name": "Bob", "rate": 3, "price": 1200 },
  { "name": "Jenny", "rate": 3.8, "price": 800 }
];

//Using the bookingSystem object, initialize the booked times for each consultant
bookingSystem.initializeBookedTimes(consultants);

// Define the book function as a global function
function book(hour, duration, criteria) {
  bookingSystem.book(consultants, hour, duration, criteria);
}

book(15, 1, "price"); // Jenny
book(11, 2, "price"); // Jenny
book(10, 2, "price"); // John
book(20, 2, "rate"); // John
book(11, 1, "rate"); // Bob
book(11, 2, "rate"); // No Service
book(14, 3, "price"); // John

// !第三題

// collects all the arguments passed to the function into an array named data
//array named data is passed to the map function
function func(...data) {
  //take the middle name of each name and store it in the middleNames array
  let middleNames = data.map(name => {
    let parts = name.split(""); // Split the name into words as an array["彭", "大", "牆]
    if (parts.length === 2) {
      return parts[1];
    } else if (parts.length === 4) {
      return parts[2];
    } else {
      return parts[1];
    }
  });

  let uniqueMiddleName = [];

  middleNames.forEach((name) => { //iterate every middle name of every name
    if (!uniqueMiddleName.includes(name)) {
      uniqueMiddleName.push(name);
    } else if (uniqueMiddleName.includes(name)) {
      uniqueMiddleName.splice(uniqueMiddleName.indexOf(name), 1)
    }
  });

  if (uniqueMiddleName.length !== 0) {
    const nameHasUniqueMid = data.find(name => name.includes(uniqueMiddleName[0]));
    console.log(nameHasUniqueMid);
  } else {
    console.log("沒有");
  }
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安

// !第四題
function getNumber(index) {
  let quotient = Math.floor(index / 3)
  let reminder = index % 3
  let result = quotient * 7 + (reminder * 4)
  console.log(result)
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70

// !第五題

function find(spaces, stat, n) {
  let minSpacesCarIndex = -1
  let minSpaces = Infinity
  stat = stat.map((x, i) => {
    x = x === 0 ? 0 : spaces[i]
    if (x >= n) { //x是空位足夠的車廂空位數，i是車廂序號，n是需要空位
      if (x < minSpaces){
        minSpaces = x
        minSpacesCarIndex = i
      }
    }else{
      return undefined
    }
  })
  console.log(minSpacesCarIndex)
}
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2); // print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2