toggleButton.addEventListener('click', function() {
  body.classList.toggle('dark');
  if (body.classList.contains('dark')) {
    toggleButton.classList.remove('btn-primary');
    toggleButton.classList.add('btn-light');
  } else {
    toggleButton.classList.remove('btn-light');
    toggleButton.classList.add('btn-primary');
  }
});