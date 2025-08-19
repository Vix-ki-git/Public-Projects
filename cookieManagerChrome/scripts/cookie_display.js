
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  const tabUrl = tabs[0].url;

  chrome.cookies.getAll({ url: tabUrl }, function (cookies) {
    const cookieList = document.getElementById('cookies-list');
    cookies.forEach(cookie => {
      const li = document.createElement('li');
      
      // Create and style the initial text content
      const textSpan = document.createElement('span');
      textSpan.innerHTML = `
        Domain: ${cookie.domain} <br>
        Name: ${cookie.name}<br>
        isSameSite: ${cookie.sameSite}<br>
        isSecure: ${cookie.secure}<br>
        isSession: ${cookie.session}`;
      li.appendChild(textSpan);

      // Create Delete and Value buttons
      const deleteButton = document.createElement('button');
      const valueButton = document.createElement('button');
      valueButton.textContent = 'Value';
      deleteButton.textContent = 'Delete';

      let flag = false;
      const valueSpan = document.createElement('span');
      
      // When the Value button is clicked, toggle the display of the cookie value
      valueButton.onclick = () => {
        if (!flag) {
          valueSpan.textContent = ` Value: ${cookie.value}`;
          li.appendChild(valueSpan);
          flag = true;
        } else {
          li.removeChild(valueSpan);
          flag = false;
        }
      };

      // When the Delete button is clicked, remove the cookie and the list item
      deleteButton.onclick = () => {
        chrome.cookies.remove({ url: tabUrl, name: cookie.name });
        li.remove();
      };

      // Append the buttons to the list item
      li.appendChild(valueButton);
      li.appendChild(deleteButton);
      cookieList.appendChild(li);
    });
  });
});



document.addEventListener('DOMContentLoaded', function () {
  // Get the buttons and file input from popup.html
  const exportButton = document.getElementById('export-button');
  const importButton = document.getElementById('import-button');
  const fileInput = document.getElementById('file-input');

  // Add event listeners to buttons
  exportButton.addEventListener('click', exportCookies);
  importButton.addEventListener('click', () => fileInput.click()); // Trigger file input on import button click

  // Add event listener for file input (for importing cookies)
  fileInput.addEventListener('change', importCookies);
});

// Function to export cookies for the current tab
function exportCookies() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const tabUrl = tabs[0].url;

    chrome.cookies.getAll({ url: tabUrl }, function (cookies) {
      const cookieData = cookies.map(cookie => ({
        domain: cookie.domain,
        name: cookie.name,
        value: cookie.value,
        secure: cookie.secure,
        httpOnly: cookie.httpOnly,
        sameSite: cookie.sameSite,
        expirationDate: cookie.expirationDate || "Session",
      }));

      // Convert to JSON and create a Blob
      const blob = new Blob([JSON.stringify(cookieData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      // Create a temporary download link and trigger the download
      const a = document.createElement('a');
      a.href = url;
      a.download = 'cookies.json';
      a.click();
      
      // Revoke the object URL after download
      URL.revokeObjectURL(url);
    });
  });
}
// Function to handle importing cookies
function importCookies(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    const cookieData = JSON.parse(e.target.result);

    cookieData.forEach(cookie => {
      // For each cookie in the JSON, create the cookie using chrome.cookies.set
      chrome.cookies.set({
        url: `http://${cookie.domain}`, // You can modify this to support https and domain variations
        name: cookie.name,
        value: cookie.value,
        secure: cookie.secure,
        httpOnly: cookie.httpOnly,
        sameSite: cookie.sameSite,
        expirationDate: cookie.expirationDate === "Session" ? undefined : cookie.expirationDate
      });
    });

    alert('Cookies imported successfully!');
  };
  
  reader.readAsText(file);
}

