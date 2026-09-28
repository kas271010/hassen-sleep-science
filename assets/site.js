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
})();
