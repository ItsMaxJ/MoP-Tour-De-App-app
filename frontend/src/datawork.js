document.addEventListener('DOMContentLoaded', () => {
  const footer = document.getElementById('datawork');
  const defaultMessage = 'Hello, world!';

  if (!footer) {
    return;
  }

  const setFooterText = (message = defaultMessage) => {
    footer.textContent = message || defaultMessage;
  };

  if (typeof fetch !== 'function') {
    setFooterText();
    return;
  }

  fetch('http://localhost:3001/api/datawork')
    .then((response) => {
      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      return response.json();
    })
    .then((data) => {
      setFooterText(data && data.message ? data.message : defaultMessage);
    })
    .catch((error) => {
      console.error('Nepodarilo sa načítať footer:', error);
      setFooterText();
    });
});

