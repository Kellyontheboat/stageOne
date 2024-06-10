// !方法一
class ArrayDB {   
  constructor() {
    this.data = [];
    this.size = 0;
  }


  push(value) {   // O(n)
    if(!this.contain(value)){
      this.data.push(value);
      this.size++;
    }
    
  }

  contain(value) {  // O(n)
    for (let i = 0; i < this.data.length; i ++) {
      if (this.data[i] === value) {
        return true;
      }else{
        return false;
      }

    }
  }

    list(){  // O(nlogn)
      return this.data.toSorted();
    }
  
  }

let db1 = new ArrayDB();
for(let i = 0; i < 100000; i ++){
  db1.push(Math.random()*100000)
}

console.time();
console.log(db1.contain(1000));
console.timeEnd();
// db1.push(1);
// db1.push(2);
// db1.push(3);
// db1.push(4);
// db1.push(2.5);
// console.log(db1.list());
// console.log(db1.size);

// !方法二
class Node {
  constructor(value, left, right) {
    this.value = value;
    this.left = left;
    this.right = right;
  }
}

class BSTDB {
  constructor() {
    this.root = null;
    this.size = 0;
  }

  push(value) {  // O(logn)
    let node = this.root;
    if (node === null) {
      this.root = new Node(value, null, null);
      this.size++;
      return;
    }
    while (true) { // 一次loop就是看要插入的值是在節點的右邊或左邊
      if (value === node.value) { // 要放的值剛好等於節點值
        return;
      } else if (value > node.value) { // 要放的資料比較大，往右邊找
        if (node.right === null) {
          node.right = new Node(value, null, null);
          this.size ++;
          break;
        } else { 
        node = node.right // 繼續
        }
      } else { // 要放的資料比較小，往左邊找
        if (node.left === null) {
          node.left = new Node(value, null, null);
          this.size ++;
          break;
        } else {
          node = node.left
        }
      }
    }
  }


  contain(value) {  // O(logn)
    let node = this.root;
    if (node === null) { // 先排除如果樹中沒有任何資料
      return false;
    }
    while (true) { // 一次loop就是看要插入的值是在節點的右邊或左邊
      if (value === node.value) { // 要放的值剛好等於節點值
        return true;
      } else if (value > node.value) { // 要放的資料比較大，往右邊找
        if (node.right === null) {
          break;
        }
        node = node.right;
      } else { // 要放的資料比較小，往左邊找
        if (node.left === null) {
          break;
        } else {
          node = node.left;
        }
      }
    }
    return false;

  }

  list() { // O(n)
    let node = this.root;
    let result = [];
    let stack = []; // 存放根左邊的節點
    while (node || stack.length > 0) { // loop直到stack空了
      while (node) {// 從根節點往左邊追，直到追到最左邊
        stack.push(node); // stack沿路蒐集左邊的節點
        node = node.left; // 如果還有左邊的節點，就繼續往左邊找
      } // stack蒐集完之後node就不會有值了(已收集最小值)，結束while(node)loop進行下方
      node = stack.pop(); // 追完後把stack中最大的pop出來
      result.push(node.value);
      node = node.right; // 往右邊蒐集
    }
    return result;
  }
}

let db2 = new BSTDB();
for(let i = 0; i < 100000; i ++) {
  db2.push(Math.random()*100000)
};
console.time();
console.log(db2.contain(1000));
console.timeEnd();
// db2.push(1);
// db2.push(2);
// db2.push(3);
// db2.push(4);
// db2.push(2.5);
// console.log(db2.list());
// console.log(db2.size);