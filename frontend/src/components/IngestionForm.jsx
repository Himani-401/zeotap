import React, { useState } from 'react';
import axios from 'axios';

function IngestionForm({ updateStatus }) {
  const [source, setSource] = useState('clickhouse');
  const [file, setFile] = useState(null);
  const [config, setConfig] = useState({
    host: '',
    port: '',
    user: '',
    jwtToken: '',
    database: '',
    table: '',
    columns: [],
    fileName: '',
    delimiter: ',',
  });

  const handleSourceChange = (e) => setSource(e.target.value);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleColumnSelection = (columns) => setConfig((prev) => ({ ...prev, columns }));

  const handleSubmit = async () => {
    updateStatus('Connecting...');
    try {
      const response = await axios.post('http://localhost:5000/connect-clickhouse', config);
      if (response.data.success) {
        updateStatus('Columns Loaded!');
        // Additional logic for column selection can be added here
      } else {
        updateStatus('Error: ' + response.data.error);
      }
    } catch (error) {
      updateStatus('Error: ' + error.message);
    }
  };

  return (
    <div>
      <div>
        <label>
          Data Source:
          <select onChange={handleSourceChange}>
            <option value="clickhouse">ClickHouse</option>
            <option value="flatfile">Flat File (CSV)</option>
          </select>
        </label>
      </div>

      {source === 'clickhouse' ? (
        <div>
          <input type="text" name="host" placeholder="Host" onChange={handleInputChange} />
          <input type="text" name="port" placeholder="Port" onChange={handleInputChange} />
          <input type="text" name="user" placeholder="User" onChange={handleInputChange} />
          <input type="text" name="jwtToken" placeholder="JWT Token" onChange={handleInputChange} />
          <input type="text" name="database" placeholder="Database" onChange={handleInputChange} />
          <input type="text" name="table" placeholder="Table" onChange={handleInputChange} />
        </div>
      ) : (
        <div>
          <input type="file" onChange={handleFileChange} />
          <input type="text" name="delimiter" placeholder="CSV Delimiter" onChange={handleInputChange} />
        </div>
      )}

      <button onClick={handleSubmit}>Start Ingestion</button>
    </div>
  );
}

export default IngestionForm;
