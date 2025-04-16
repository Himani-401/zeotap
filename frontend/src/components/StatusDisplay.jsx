import React from 'react';

function StatusDisplay({ status, records }) {
  return (
    <div>
      {status && <p>Status: {status}</p>}
      {status === 'Completed' && <p>Records Processed: {records}</p>}
    </div>
  );
}

export default StatusDisplay;
