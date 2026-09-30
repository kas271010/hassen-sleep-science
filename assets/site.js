/* mycpapdoctor.com — nav toggle + form submit. No frameworks, no animation. */
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.label').textContent = open ? 'Close menu' : 'Menu';
    });
  }

  var forms = document.querySelectorAll('form[data-web3forms]');
  Array.prototype.forEach.call(forms, function (form) {
    var status = form.querySelector('.form-status');
    var button = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.querySelector('input[name="botcheck"]').checked) { return; }
      var data = {};
      Array.prototype.forEach.call(form.querySelectorAll('input, select, textarea'), function (el) {
        if (el.name && el.name !== 'botcheck') { data[el.name] = el.value; }
      });
      status.className = 'form-status';
      status.textContent = 'Sending…';
      button.disabled = true;
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function (res) {
        if (res.success) {
          status.className = 'form-status ok';
          status.textContent = 'Thank you. I received your message and will get back to you within one business day.';
          form.reset();
        } else { throw new Error(res.message || 'failed'); }
      }).catch(function () {
        status.className = 'form-status err';
        status.textContent = 'The form did not go through. Please call (810) 523-8233 or email khassen@mycpapdoctor.com.';
      }).finally(function () { button.disabled = false; });
    });
  });
  /* better-sleep map: each step opens a details card (tap, click, Enter/Space; Esc or × closes) */
  var panel = document.getElementById('mdetail');
  var dataEl = document.getElementById('stop-data');
  if (panel && dataEl) {
    var D = JSON.parse(dataEl.textContent), cur = null;
    var hide = function () { cur = null; panel.hidden = true;
      Array.prototype.forEach.call(document.querySelectorAll('.mstop'), function (g) { g.classList.remove('on'); }); };
    var show = function (n) {
      if (cur === n) { hide(); return; }
      cur = n; var d = D[n];
      Array.prototype.forEach.call(document.querySelectorAll('.mstop'), function (g) { g.classList.toggle('on', g.getAttribute('data-n') === n); });
      panel.querySelector('.md-num').textContent = 'Step ' + n;
      panel.querySelector('.md-title').textContent = d.title;
      var who = panel.querySelector('.md-who');
      who.textContent = d.mine ? 'With Dr. Hassen' : 'With a partner: ' + d.partner;
      who.className = 'md-who ' + (d.mine ? 'me' : 'pt');
      panel.querySelector('.md-text').textContent = d.text;
      var one = panel.querySelector('.md-one'); one.textContent = d.one; one.hidden = !d.one;
      panel.hidden = false;
      panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    };
    Array.prototype.forEach.call(document.querySelectorAll('.mstop'), function (g) {
      var n = g.getAttribute('data-n');
      g.addEventListener('click', function () { show(n); });
      g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(n); } });
    });
    panel.querySelector('.md-close').addEventListener('click', hide);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { hide(); } });
  }
})();
