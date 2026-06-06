const form = document.getElementById("expense-form");
const amount = document.getElementById("amount");
const category = document.getElementById("category");
const note = document.getElementById("note");
const expenseItems = document.getElementById("expense-items");
const date = document.getElementById("date");
form.addEventListener("submit", function (e) {
  e.preventDefault();

  const amt = amount.value;
  const cat = category.value;
  const nt = note.value;
  const dtRaw = date.value;
  const dtObj = new Date(dtRaw);
  const mm = String(dtObj.getMonth() + 1).padStart(2, '0');
  const dd = String(dtObj.getDate()).padStart(2, '0');
  const yyyy = dtObj.getFullYear();
  const dt = `${mm}/${dd}/${yyyy}`;
  if (amt === "" || cat === "") return;

  const li = document.createElement("li");
  li.textContent = `On  ${dt}  => ₹${amt} had spent for ${cat} . (${nt})`;
  expenseItems.appendChild(li);

 // Clear the form fields after submission
  amount.value = "";
  category.value = "";
  note.value = "";
  date.value = "";
});
//ruppee canvas

const rupeeContainer = document.querySelector('.rupee-container');

function createRupee() {
  const rupee = document.createElement('div');
  rupee.classList.add('rupee');
  rupee.innerText = '₹';

  // ✅ RANDOM horizontal position across the screen
  rupee.style.left = Math.random() * window.innerWidth + 'px';

  // ✅ Random size for variety
  rupee.style.fontSize = Math.random() * 20 + 15 + 'px';

  // ✅ Append to container
  rupeeContainer.appendChild(rupee);

  // ✅ Remove rupee after animation
  setTimeout(() => {
    rupee.remove();
  }, 6000);
}

// ✅ Create new rupee every 300ms
setInterval(createRupee, 300);

