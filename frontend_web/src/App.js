import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

function App() {
  const [report, setReport] = useState(null);

  const uploadFile = async (e) => {
    const formData = new FormData();
    formData.append('file', e.target.files[0]);
    const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData);
    setReport(res.data);
  };
return (
  <div style={{ padding: '40px', fontFamily: 'Arial' }}>
    <h1>Chemical Equipment Visualizer</h1>
    
    {/* File Input */}
    <input type="file" accept=".csv" onChange={uploadFile} />
    
    {/* 1. Only show this section if report is NOT null */}
    {report ? (
      <div style={{ marginTop: '30px' }}>
        <h2>Analysis Results</h2>
        <p><strong>Total Equipment:</strong> {report.total_count}</p>
        <p><strong>Avg Pressure:</strong> {report.avg_pressure} bar</p>
        <p><strong>Avg Flowrate:</strong> {report.avg_flowrate} m³/h</p>

        {/* 2. Only show the chart if the distribution data exists */}
        {report.type_distribution && (
          <div style={{ width: '600px', marginTop: '20px' }}>
            <Bar 
              data={{
                labels: Object.keys(report.type_distribution),
                datasets: [{
                  label: 'Equipment Count by Type',
                  data: Object.values(report.type_distribution),
                  backgroundColor: 'rgba(54, 162, 235, 0.6)',
                }]
              }} 
            />
          </div>
        )}
        
        <br />
        <a href="http://127.0.0.1:8000/api/report/" target="_blank" rel="noreferrer">
          <button style={{ padding: '10px 20px', cursor: 'pointer' }}>Download PDF Report</button>
        </a>
      </div>
    ) : (
      // 3. Show this message if no file has been uploaded yet
      <p style={{ marginTop: '20px', color: '#666' }}>Please upload a CSV file to see the analysis.</p>
    )}
  </div>
);
}

export default App;