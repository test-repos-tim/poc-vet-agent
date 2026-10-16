/**
 * chat.js — Chat widget client for POC Vet Agent Demo
 * Communicates with local Flask API bridge via REST endpoint.
 */

(function () {
  const toggle = document.getElementById('chat-toggle');
  const windowEl = document.getElementById('chat-window');
  const closeBtn = document.getElementById('chat-close');
  const messagesEl = document.getElementById('chat-messages');
  const inputEl = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');

  // Flask API bridge endpoint (running on localhost:5000)
  const API_URL = 'http://localhost:5000/chat';

  toggle.addEventListener('click', () => {
    windowEl.classList.toggle('hidden');
    if (!windowEl.classList.contains('hidden')) inputEl.focus();
  });

  closeBtn.addEventListener('click', () => windowEl.classList.add('hidden'));

  function addMessage(text, isUser) {
    const div = document.createElement('div');
    div.className = 'message ' + (isUser ? 'user' : 'bot');
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function appendBotReply(text) {
    addMessage(text, false);
  }

  sendBtn.addEventListener('click', handleSend);
  inputEl.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleSend(); });

  async function handleSend() {
    const text = inputEl.value.trim();
    if (!text) return;
    addMessage(text, true);
    inputEl.value = '';

    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot';
    typingDiv.textContent = 'Typing...';
    messagesEl.appendChild(typingDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      if (!response.ok) {
        throw new Error('Network error: ' + response.status);
      }
      const data = await response.json();
      messagesEl.removeChild(typingDiv);
      appendBotReply(data.reply);
    } catch (err) {
      messagesEl.removeChild(typingDiv);
      appendBotReply('Sorry, I am offline right now. Please call (555) 123-4567 for urgent needs.');
      console.error('Chat API error:', err);
    }
  }
})();