/* ===== script.js ===== */
// ===== CHAT TOGGLE =====
function toggleChat(force) {
  const panel = document.getElementById('chatPanel');
  if (force === true) {
    panel.classList.add('open');
  } else if (force === false) {
    panel.classList.remove('open');
  } else {
    panel.classList.toggle('open');
  }
}

// ===== FAQ TOGGLE =====
function toggleFaq(el) {
  const item = el.parentElement;
  item.classList.toggle('open');
  // Update plus sign
  const plus = el.querySelector('.faq-plus');
  if (plus) {
    plus.textContent = item.classList.contains('open') ? '−' : '+';
  }
}

// ===== MOCK RESPONSES =====
// In production, replace sendChat() with a fetch() call to your RAG backend.
const mockAnswers = [
  { match: /schol/i, text: 'Scholarship forms for 2025-26 are due by 20 August.', src: 'Scholarship Notice 2025-26.pdf, page 1' },
  { match: /document|admission/i, text: 'You will need your SSC marksheet, leaving certificate, caste certificate (if applicable), and 4 passport photographs.', src: 'Documents Required.pdf, page 1' },
  { match: /fee/i, text: 'The fee structure for the incoming batch was revised as of 5 July 2025. Check the fee structure notice for exact figures.', src: 'Fee Structure Notice.pdf, page 1' },
  { match: /exam/i, text: 'Winter term exam forms follow the schedule published on 27 July 2025.', src: 'Exam Form Schedule.pdf, page 1' },
  { match: /branch|change/i, text: 'Branch change requests are considered at the end of first year, subject to seat vacancy and merit.', src: 'Branch Change Policy.pdf, page 2' },
  { match: /lateral|entry/i, text: 'Lateral entry to second year is available for eligible vocational and ITI backgrounds, subject to seat availability.', src: 'Lateral Entry Guidelines.pdf, page 1' },
  { match: /scholarship|reserved|category/i, text: 'Government scholarship schemes apply per category. Check the current scholarship notice for deadlines and required forms.', src: 'Scholarship Notice 2025-26.pdf, page 2' }
];

// ===== SEND CHAT =====
function sendChat() {
  const input = document.getElementById('chatInput');
  const body = document.getElementById('chatBody');
  const q = input.value.trim();
  if (!q) return;

  // Append user message
  const qBubble = document.createElement('div');
  qBubble.className = 'bubble q';
  qBubble.textContent = q;
  body.appendChild(qBubble);
  input.value = '';
  body.scrollTop = body.scrollHeight;

  // Simulate response delay
  setTimeout(() => {
    const found = mockAnswers.find(a => a.match.test(q));
    const aBubble = document.createElement('div');
    aBubble.className = 'bubble a';

    if (found) {
      aBubble.innerHTML = found.text + '<span class="src">Source: ' + found.src + '</span>';
    } else {
      aBubble.textContent = "I couldn't find that in the current documents. Try asking about admission, fees, scholarships, exams, branch change, or lateral entry.";
    }
    body.appendChild(aBubble);
    body.scrollTop = body.scrollHeight;
  }, 500);
}

// ===== KEYBOARD SHORTCUT: Enter to send =====
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('chatInput');
  if (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendChat();
      }
    });
  }

  // Close chat panel when clicking outside (optional enhancement)
  document.addEventListener('click', function (e) {
    const panel = document.getElementById('chatPanel');
    const bubble = document.querySelector('.chat-bubble');
    if (panel && panel.classList.contains('open')) {
      const isClickInside = panel.contains(e.target) || bubble.contains(e.target);
      if (!isClickInside) {
        panel.classList.remove('open');
      }
    }
  });
});