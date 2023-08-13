let ingressInput = document.getElementById("ingressInput");
let button = document.getElementById("setButton");
let responseText = document.getElementById("responseText");

chrome.storage.sync.get("ingress", (data) => {
  ingressInput.value = data.ingress;
});

function handleButtonClick(event) {
  let ingress = ingressInput.value;
  chrome.storage.sync.set({ ingress });
  responseText.innerText = `Ingress service set to ${ingress}`;
}

button.addEventListener("click", handleButtonClick);
