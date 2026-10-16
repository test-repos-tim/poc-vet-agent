/**
 * chat.js — Chat widget client for POC Vet Agent Demo
 * Communicates with local Hermes agent API bridge via REST endpoint.
 * Phase 1: Website stub. Chat messages are logged locally until Phase 2 API bridge is built.
 */

(function () {
  const toggle = document.getElementById('chat-toggle');
  const windowEl = document.getElementById('chat-window');
  const closeBtn = document.getElementById('chat-close');
  const messagesEl = document.getElementById('chat-messages');
  const inputEl = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');

  // Local message buffer for Phase 1 (will be wired to Hermes API in Phase 2)
  let messageHistory = [];

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
    messageHistory.push({ text, isUser, ts: Date.now() });
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

    // Phase 1: Simulated responses (will be replaced by Hermes API call in Phase 2)
    const reply = generateBotReply(text);
    setTimeout(() => appendBotReply(reply), 600);
  }

  function generateBotReply(text) {
    const lower = text.toLowerCase();
    if (lower.includes('appoint') || lower.includes('book')) {
      return 'I can help you book an appointment. Please provide: pet name, species, preferred date/time, and reason for visit.';
    }
    if (lower.includes('emergency') || lower.includes('urgent')) {
      return 'If this is an emergency, please call us immediately at (555) 123-4567 or bring your pet to our clinic. We are open Mon-Fri until 8pm.';
    }
    if (lower.includes('prescription') || lower.includes('refill')) {
      return 'For prescription refills, please provide: pet name, medication name, dosage, and your pharmacy contact.';
    }
    if (lower.includes('hour') || lower.includes('open') || lower.includes('time')) {
      return 'Our hours are Monday-Friday 8am-8pm, Saturday 9am-5pm. Closed Sundays.';
    }
    if (lower.includes('hello') || lower.includes('hi') || lower.includes('hey')) {
      return 'Hello! I am the virtual assistant for Paws & Claws Animal Hospital. How can I help your pet today?';
    }
    return 'I am still learning. For urgent questions, please call (555) 123-4567. I can help with appointments, hours, and prescription refills.';
  }
})();