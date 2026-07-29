// LIVER COMPASS by CAP — 共通スクリプト
document.addEventListener('DOMContentLoaded', function () {

  // scroll reveal
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(function (item) {
    item.addEventListener('click', function () {
      item.classList.toggle('open');
    });
  });

  // Article tabs (filter by data-category)
  var tabs = document.querySelectorAll('.tab[data-filter]');
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');
        var filter = tab.getAttribute('data-filter');
        document.querySelectorAll('[data-category]').forEach(function (card) {
          var show = (filter === 'all' || card.getAttribute('data-category') === filter);
          card.style.display = show ? '' : 'none';
        });
      });
    });
  }
});
