const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function loadScript(document, fetchImpl) {
  const source = fs.readFileSync(
    path.resolve(__dirname, '../frontend/src/datawork.js'),
    'utf8'
  );

  const context = {
    document,
    console,
    fetch: fetchImpl,
  };

  vm.runInNewContext(source, context);
  return document;
}

test('footer displays the backend value when the API responds', async () => {
  let footer = { textContent: '' };
  const document = {
    _onDomContentLoaded: null,
    getElementById(id) {
      if (id === 'datawork') return footer;
      return null;
    },
    addEventListener(event, callback) {
      if (event === 'DOMContentLoaded') {
        this._onDomContentLoaded = callback;
      }
    },
  };

  loadScript(document, async () => ({
    ok: true,
    json: async () => ({ message: 'Ahoj, svet!' }),
  }));

  document._onDomContentLoaded();
  await new Promise((resolve) => setImmediate(resolve));

  assert.equal(footer.textContent, 'Ahoj, svet!');
});

test('footer falls back to the default value when fetch is unavailable', () => {
  let footer = { textContent: '' };
  const document = {
    _onDomContentLoaded: null,
    getElementById(id) {
      if (id === 'datawork') return footer;
      return null;
    },
    addEventListener(event, callback) {
      if (event === 'DOMContentLoaded') {
        this._onDomContentLoaded = callback;
      }
    },
  };

  loadScript(document, undefined);

  document._onDomContentLoaded();

  assert.equal(footer.textContent, 'Hello, world!');
});
