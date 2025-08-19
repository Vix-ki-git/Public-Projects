// background.js
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const tabId = tabs[0].id;
  
    chrome.cookies.getAll({ url: tabs[0].url }, function (cookies) {
      console.log(cookies); // Here you can display the cookies in the popup
    });
  });
  