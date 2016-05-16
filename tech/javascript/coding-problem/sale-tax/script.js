var sHTML = "";
var TAX_BASIC = 0.1;
var TAX_IMPORT = 0.05;
var taxRule = [
  {type: "books", basicTax: 0},
  {type: "food", basicTax: 0},
  {type: "medical", basicTax: 0},
  {ifImport: true, importTax: TAX_IMPORT}
];

var input1 = [{
  name: "book", 
  type:"books", 
  price: 12.49, 
  ifImport: false, 
  unit: 1
},{
  name: "music CD", 
  type: "", 
  price: 14.99, 
  ifImport: false, 
  unit: 1
},{
  name: "chocolate bar", 
  type: "food", 
  price: 0.85, 
  ifImport: false, 
  unit: 1
}];

var input2 = [{
  name: "box of chocolates",
  type: "food",
  price: 10.00,
  ifImport: true,
  unit: 1
}, {
  name: "bottle of perfume",
  type: "",
  price: 47.50,
  ifImport: true,
  unit: 1
}];

/*
input3
1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25
*/

var input3 = [{
  name: "bottle of perfume",
  type: "food",
  price: 27.99,
  ifImport: true,
  unit: 1
}, {
  name: "bottle of perfume",
  type: "",
  price: 18.99,
  ifImport: false,
  unit: 1
}, {
  name: "packet of headache pills",
  type: "medical",
  price: 9.75,
  ifImport: false,
  unit: 1
},{
  name: "box of imported chocolates",
  type: "food",
  price: 11.25,
  ifImport: true,
  unit: 1
}];

window.onload = function() {

  genReport(input1);
  genReport(input2);
  genReport(input3);

}

function genReport(input){
  // console.log('runReport');
  totalTax = 0;
  total = 0;
  
  for (let i = 0; i < input.length; i++) {

    item = input[i];
    // console.log('item', item);
    // console.log("i", i);
    // console.log("input.length", input.length);
    // console.log("item.name", item.name);
    
    itemPriceAfterTax = getPriceAfterTax(item);

    sHTML += item.unit + " ";
    if(item.ifImport) { sHTML += 'imported '}
    sHTML += item.name + ": "
      + itemPriceAfterTax.toFixed(2) 
      + "<br/>";

    totalTax += getRoundNumber(getTaxValue(item));
    total += itemPriceAfterTax;
  }

  sHTML += "Sale Taxes: " + totalTax.toFixed(2) + "<br/>";
  sHTML += "Total: " + getRoundNumber(total) + "<br/><br/>";
  document.querySelector("#result").innerHTML = sHTML;
}

function getRoundNumber(num, power) {
  n = power || 1;
  // console.log(n);
  return Math.round(num * 10 * n) / (10 * n);
}

function getPriceAfterTax(item) {
  console.log(item.name);
  //console.log('getBasicTax(item)', getBasicTax(item));
  console.log('origin price', toFixedInFloat(item.price));
  console.log('getTaxValue', getTaxValue(item));
  
  console.log('after tax price', getRoundNumber(toFixedInFloat(item.price) + getTaxValue(item), 2));
  return item.price * (1 + getBasicTax(item) + getImportTax(item));
}

function getTaxValue(item) {
  return getRoundNumber(item.price * getBasicTax(item) + getImportTaxValue(item));
}

function getBasicTax(item){
  var basicTax = TAX_BASIC;
  var improtTax = 0.0;

  for (let i = 0; i < taxRule.length; i++){
    //console.log(item.name);
    //console.log('compareTax', taxRule[i].type == item.type);
    //if (!item.type) {break;}
    if (taxRule[i].type == item.type) {
      basicTax = taxRule[i].basicTax;
      break;
    }
  }

  return basicTax;
}

function getImportTax(item) {
  if(item.ifImport){
    importTax = TAX_IMPORT;
  } else {
    importTax = 0;
  }
  return importTax;
}

function getImportTaxValue(item){
  return getRoundNumber(getImportTax(item) * item.price);
}

function toFixedInFloat(num, length) {
  length = length || 2;
  return parseFloat(num.toFixed(), length);
}
