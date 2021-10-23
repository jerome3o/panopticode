// background.js

let ingress = "http://192.168.1.63:8000/browsing_history";

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({ ingress });
  console.log(`Ingress server set to ${ingress}`);
});

chrome.history.onVisited.addListener(historyItem => {
    chrome.storage.sync.get("ingress", data => {
      fetch(
        data.ingress,
        {
          method: "POST",
          headers: {
            "Content-Type": 'application/json'
          },
          body: JSON.stringify(historyItem)
        }
      );
    });
})