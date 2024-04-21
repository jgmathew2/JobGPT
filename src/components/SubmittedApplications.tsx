import React, { useState } from 'react';
import ReactDOMServer from 'react-dom/server';

const SubmittedApplications = () => {
  const [companyList, setCompanyList] = useState([""]);

  const [applicationCount, setApplicationCount] = useState(0);

  const getApplied = async () => {

    let text = await window.ipcRenderer.invoke("get_previous_applications", {});

    let array = text.data.split("\n\n")

    setCompanyList(array)

    let count = 0; 

    for(let c of text.data.split('')) {

      if(c == '[') count++; 

    }
    setApplicationCount(count)
  }

  const checkRecurr = async() => {
    setInterval(getApplied, 4000)
    console.log(companyList)

  }

  const ScrollableContent: React.FC = () => {
    return (
      <div style={{ overflowY: 'auto', height: '100%', width: '100%', borderRadius: 10}}>
        
        <p>Applications submitted: {applicationCount}</p>

        {companyList.map((company) => {return <p>{company}</p>})}
      </div>
    );
  };

  const iframeHTML = ReactDOMServer.renderToStaticMarkup(<ScrollableContent />);
  const iframeSrcDoc = `<!DOCTYPE html><html lang="en"><body>${iframeHTML}</body></html>`;


  checkRecurr()

  return (
    <iframe
      srcDoc={iframeSrcDoc}
      style={{ width: '75%', height: '300px', border: 'none', borderRadius: 10, background: "#464545"}}
      sandbox="allow-scripts allow-same-origin"
    />
  );
};

export default SubmittedApplications;
