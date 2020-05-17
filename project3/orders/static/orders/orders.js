document.addEventListener('DOMContentLoaded', () => {
  const itemElement = document.querySelector('#id_item');
  one = document.querySelector('#id_topping1');
  two = document.querySelector('#id_topping2');
  three = document.querySelector('#id_topping3');
  onelabel = document.querySelector('label[for=id_topping1]');
  twolabel = document.querySelector('label[for=id_topping2]');
  threelabel = document.querySelector('label[for=id_topping3]');

  // start hidden
  one.style.visibility = 'hidden';
  onelabel.innerHTML = '';
  two.style.visibility = 'hidden';
  twolabel.innerHTML = '';
  three.style.visibility = 'hidden';
  threelabel.innerHTML = '';

  itemElement.addEventListener('change', () => {
    console.log(itemElement.value);
    if (itemElement.value == 2 || itemElement.value == 7) {
      one.style.visibility = 'visible';
      one.required = true;
      two.style.visibility = 'hidden';
      two.required = false;
      three.style.visibility = 'hidden';
      three.required = false;

    } else if(itemElement.value == 3 || itemElement.value == 8) {
        one.style.visibility = 'visible';
        one.required = true;
        two.style.visibility = 'visible';
        two.required = true;
        three.style.visibility = 'hidden';
        three.required = false;
    } else if(itemElement.value == 4 || itemElement.value == 9) {
        one.style.visibility = 'visible';
        one.required = true;
        two.style.visibility = 'visible';
        two.required = true;
        three.style.visibility = 'visible';
        three.required = true;
    } else {
        one.style.visibility = 'hidden';
        one.required = false;
        two.style.visibility = 'hidden';
        two.required = false;
        three.style.visibility = 'hidden';
        three.required = false;
    }
  });
});
