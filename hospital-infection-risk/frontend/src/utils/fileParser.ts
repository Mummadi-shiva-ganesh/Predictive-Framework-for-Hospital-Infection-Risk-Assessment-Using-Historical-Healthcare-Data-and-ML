export function parseCSV(csvText: string): Record<string, string>[] {
  const lines = csvText
    .split(/\r\n|\n/)
    .map(line => line.trim())
    .filter(line => line.length > 0 && !line.startsWith('#'));

  if (lines.length < 2) {
    throw new Error('CSV file is empty or missing data rows.');
  }

  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const rows: Record<string, string>[] = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    if (values.length !== headers.length) {
      continue;
    }
    const rowObj: Record<string, string> = {};
    headers.forEach((header, index) => {
      rowObj[header] = values[index];
    });
    rows.push(rowObj);
  }

  return rows;
}

export function parseUploadedFile(file: File): Promise<any> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    if (file.name.endsWith('.json')) {
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target?.result as string);
          resolve(json);
        } catch (err: any) {
          reject(new Error('Invalid JSON file format: ' + err.message));
        }
      };
      reader.readAsText(file);
    } else {
      // CSV or plain text
      reader.onload = (e) => {
        try {
          const text = e.target?.result as string;
          const records = parseCSV(text);
          resolve(records);
        } catch (err: any) {
          reject(new Error('CSV Parsing Error: ' + err.message));
        }
      };
      reader.readAsText(file);
    }
  });
}
