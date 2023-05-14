export const  downloadCSV = (data) => {
    // Convert the array of objects to a CSV string
    const csv = convertToCSV(data);
    
    // Create a Blob object from the CSV string
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    
    // Create a temporary URL for the Blob object
    const url = URL.createObjectURL(blob);
    
    // Create a link element with the URL as its href attribute
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'data.csv');
    
    // Trigger a click event on the link element to download the file
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  function convertToCSV(data) {
    // Extract the keys from the first object in the array
    const keys = Object.keys(data[0]);
    
    // Create the header row of the CSV string
    const headerRow = keys.join(',') + '\n';
    
    // Create the data rows of the CSV string
    const dataRows = data.map(obj => {
      const values = keys.map(key => obj[key]);
      return values.join(',');
    }).join('\n');
    
    // Concatenate the header row and data rows to create the final CSV string
    return headerRow + dataRows;
  }
  
  