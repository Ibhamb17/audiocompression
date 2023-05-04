import React, { useState } from 'react';
import axios from 'axios';

function AudioConverter() {
  const [file, setFile] = useState(null);
  const [format, setFormat] = useState('mp3');
  const [output, setOutput] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFormatChange = (e) => {
    setFormat(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!file) {
      alert('No file selected!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('format', format);

    axios.post('/convert', formData, { responseType: 'blob' })
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        setOutput(url);
        const link = document.createElement('a');
        link.href = url;
        link.download = `converted.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      })
      .catch((error) => {
        console.error(error);
        alert('Error converting file!');
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="file">File:</label>
          <input type="file" id="file" onChange={handleFileChange} />
        </div>
        <div>
          <label htmlFor="format">Format:</label>
          <select id="format" onChange={handleFormatChange} defaultValue={format}>
            <option value="mp3">MP3</option>
            <option value="wav">WAV</option>
            <option value="ogg">OGG</option>
          </select>
        </div>
        <button type="submit">Convert</button>
      </form>
      {output && <audio controls src={output} />}
    </div>
  );
}

export default AudioConverter;
