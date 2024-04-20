import React, { useState } from 'react';
import ReactDOMServer from 'react-dom/server';

const SubmittedApplications: React.FC = () => {
  const [companyList, setCompanyList] = useState([
    'Google STEP',
    'Meta University',
  ]);
  const [applicationCount, setApplicationCount] = useState(2);

  const ScrollableContent: React.FC = () => {
    return (
      <div style={{ overflowY: 'auto', height: '100%', width: '100%' }}>
        {companyList.map((company, index) => (
          <div key={index}>{company}</div>
        ))}
        <p>Applications submitted: {applicationCount}</p>
      </div>
    );
  };

  const iframeHTML = ReactDOMServer.renderToStaticMarkup(<ScrollableContent />);
  const iframeSrcDoc = `<!DOCTYPE html><html lang="en"><body>${iframeHTML}</body></html>`;

  return (
    <iframe
      srcDoc={iframeSrcDoc}
      style={{ width: '100%', height: '400px', border: 'none' }}
      sandbox="allow-scripts allow-same-origin"
    />
  );
};

export default SubmittedApplications;
