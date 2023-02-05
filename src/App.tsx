import React, {useState, useEffect} from 'react';


function App() {
  const [url, setUrl] = useState<string | undefined>('');

  useEffect(() => {
    const queryInfo = {active: true, lastFocusedWindow: true};

    chrome.tabs && chrome.tabs.query(queryInfo, tabs => {
      const currentURL = tabs[0].url;
      setUrl(currentURL);
    });
  }, []);


  return (
    <div className="App">
      <header className="App-header">
        <p>{url}</p>
      </header>
    </div>
  );
}

export default App;
