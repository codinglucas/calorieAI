document.getElementById('uploadBtn').addEventListener('click', async () => {
  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];

  if (!file) {
    alert('Please select an image file first.');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  try {
    // 2. Send the POST request
    const response = await fetch('http://127.0.0.1:5000/upload-endpoint', {
      method: 'POST',
      body: formData // Note: Do NOT manually set Content-Type header when using FormData
    });

    if (!response.ok) {
      throw new Error(`Upload failed with status ${response.status}`);
    }

    // 1. Parse response as JSON (matches Flask return jsonify)
    const data = await response.json();

    // 2. Assign the URL returned by Flask to the <img> element
    const imgElement = document.getElementById('preview');
    imgElement.src = data.imageUrl; // Use the key returned from Flask!
    imgElement.style.display = 'block';

  } catch (error) {
    console.error('Error handling image upload:', error);
  }
});
