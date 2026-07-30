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

  // ===== 30秒診断 =====
  initQuiz();
});

function initQuiz() {
  var overlay = document.getElementById('quizOverlay');
  var body = document.getElementById('quizBody');
  var progressBar = document.getElementById('quizProgressBar');
  var closeBtn = document.getElementById('quizClose');
  if (!overlay || !body) return;

  var QUESTIONS = [
    {
      q: '人前に出るのは得意なほう？',
      options: [
        { key: 'A', text: '得意！顔出しで自分らしく話したい' },
        { key: 'B', text: '変身願望あり、アバターやキャラで魅せたい' },
        { key: 'C', text: 'ちょっと苦手だけど話すのは好き' },
        { key: 'D', text: '話すよりモノを紹介する方が得意' },
        { key: 'E', text: '正直、まだよくわからない' }
      ]
    },
    {
      q: '配信や発信に使える時間は？',
      options: [
        { key: 'A', text: '毎日ガッツリ時間を作れる' },
        { key: 'B', text: '週末や好きな時間に集中してやりたい' },
        { key: 'C', text: 'スキマ時間でコツコツ型' },
        { key: 'D', text: '用意した動画や商品紹介ならできる' },
        { key: 'E', text: 'まだ生活リズムの中でどう組み込むか未定' }
      ]
    },
    {
      q: '得意なこと・好きなことは？',
      options: [
        { key: 'A', text: 'トーク・雑談・リアクション' },
        { key: 'B', text: 'イラストやコスプレ、キャラ作り' },
        { key: 'C', text: 'コツコツ継続する作業' },
        { key: 'D', text: '商品やアイテムの紹介・レビュー' },
        { key: 'E', text: '特にこれといって思いつかない' }
      ]
    },
    {
      q: '目指したい収入イメージは？',
      options: [
        { key: 'A', text: '本業級を目指したい' },
        { key: 'B', text: '好きなことで稼げたら理想' },
        { key: 'C', text: '月数万円のお小遣い稼ぎから' },
        { key: 'D', text: '物販・EC的な収入源を作りたい' },
        { key: 'E', text: 'まずは自分に何が向いてるか知りたい' }
      ]
    },
    {
      q: '一歩踏み出すなら？',
      options: [
        { key: 'A', text: 'すぐにでもオーディションに挑戦したい' },
        { key: 'B', text: 'まずはアバターやツールを試したい' },
        { key: 'C', text: '小さく始めて続けられるか試したい' },
        { key: 'D', text: 'TikTok Shopなど物販に挑戦してみたい' },
        { key: 'E', text: '誰かに相談してから決めたい' }
      ]
    }
  ];

  var RESULTS = {
    A: {
      badge: 'TYPE A',
      title: '本格派ライバー予備軍タイプ',
      tagline: '顔出しトークで人を惹きつける、王道ライバー気質！',
      desc: '人前で話すことに抵抗がなく、リアクションや会話でファンを増やせるタイプ。まずは事務所ごとの特徴や還元率を比較して、自分に合う環境を見つけるところから始めると、デビュー後のギャップも少なくなります。',
      image: 'assets/images/quiz-result-a.svg',
      links: [
        { href: 'articles/agency-how-to-choose-10.html', text: '事務所の選び方10のポイント' },
        { href: 'articles/liver-agency-merit-demerit.html', text: '事務所所属のメリット・デメリット' },
        { href: 'articles/how-to-start-liver.html', text: 'ライバーの始め方ガイド' }
      ]
    },
    B: {
      badge: 'TYPE B',
      title: '変身系Vライバー適性タイプ',
      tagline: 'アバターやキャラの力で魅せる、変身願望アリの発信者タイプ！',
      desc: '顔出しは苦手でも、キャラクターやアバターの姿でなら自分を表現できるタイプ。IRIAMやReality、顔出し不要スタイルなど、自分らしく続けられるアプリ・方法から選んでいくのがおすすめです。',
      image: 'assets/images/quiz-result-b.svg',
      links: [
        { href: 'articles/iriam-vliver-guide.html', text: 'IRIAMで始めるVライバー入門' },
        { href: 'articles/faceless-streaming.html', text: '顔出しなしで配信する方法' },
        { href: 'articles/reality-guide.html', text: 'Realityアプリ完全ガイド' }
      ]
    },
    C: {
      badge: 'TYPE C',
      title: 'コツコツ副業ライバータイプ',
      tagline: '無理せず続けられる、着実な副業スタイルが向いている！',
      desc: 'スキマ時間を活かしてコツコツ積み上げるのが得意なタイプ。いきなり本業級を目指すより、副業として無理のないペースで始めて、続けながら収益の仕組みを理解していくのが向いています。',
      image: 'assets/images/quiz-result-c.svg',
      links: [
        { href: 'articles/side-job-liver-start.html', text: '副業からライバーを始める方法' },
        { href: 'articles/liver-income-structure.html', text: 'ライバーの収入の仕組み' },
        { href: 'articles/how-to-continue-streaming.html', text: '配信を無理なく続けるコツ' }
      ]
    },
    D: {
      badge: 'TYPE D',
      title: '物販・TikTok Shop系クリエイタータイプ',
      tagline: '紹介力・提案力を活かせる、物販クリエイター気質！',
      desc: 'トークよりも「モノを魅力的に伝える」ことが得意なタイプ。TikTok Shopのようなライブコマースは、この紹介力がそのまま収益に直結しやすい分野。配信と物販を組み合わせた新しい働き方にチャレンジしてみましょう。',
      image: 'assets/images/quiz-result-d.svg',
      links: [
        { href: 'articles/tiktok-live-guide.html', text: 'TikTok LIVE配信ガイド' },
        { href: 'articles/liver-to-influencer.html', text: 'ライバーからインフルエンサーへ' },
        { href: 'articles/liver-income-structure.html', text: 'ライバーの収入の仕組み' }
      ]
    },
    E: {
      badge: 'TYPE E',
      title: '可能性まだまだ未知数タイプ',
      tagline: '伸びしろは無限大。相談しながら自分の適性を見つけよう！',
      desc: 'まだ何が向いているか分からなくても大丈夫。実際にライバーとして活躍している人の多くも最初は同じ気持ちでした。まずは基礎知識をチェックしつつ、専門スタッフに相談しながら自分に合うスタイルを探してみましょう。',
      image: 'assets/images/quiz-result-e.svg',
      links: [
        { href: 'articles/liver-30s-start.html', text: '30代からのライバーデビュー' },
        { href: 'articles/how-to-start-liver.html', text: 'ライバーの始め方ガイド' },
        { href: 'articles/mom-housewife-streaming.html', text: '主婦・ママ層の配信スタート術' }
      ]
    }
  };

  var current = 0;
  var answers = [];
  var totalSteps = QUESTIONS.length + 1; // +1 for intro

  function setProgress(step) {
    var pct = Math.round((step / totalSteps) * 100);
    progressBar.style.width = pct + '%';
  }

  function openQuiz() {
    current = 0;
    answers = [];
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    renderIntro();
  }

  function closeQuiz() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function renderIntro() {
    setProgress(0);
    body.innerHTML =
      '<div class="quiz-intro">' +
        '<span class="quiz-emoji">✨</span>' +
        '<h3>30秒でわかる！<br>あなたの配信・発信タイプ診断</h3>' +
        '<p>5つの質問に答えるだけで、あなたに向いている発信スタイルとおすすめの一歩がわかります。<br>クリエイター向き？ライバー向き？TikTok Shop向き？さっそくチェックしてみましょう。</p>' +
        '<button type="button" class="btn btn-primary" id="quizStartBtn">診断をはじめる</button>' +
      '</div>';
    var startBtn = document.getElementById('quizStartBtn');
    if (startBtn) startBtn.addEventListener('click', function () { current = 0; renderQuestion(); });
  }

  function renderQuestion() {
    var qi = current;
    var qData = QUESTIONS[qi];
    setProgress(qi + 1);
    var optionsHtml = qData.options.map(function (opt) {
      return '<button type="button" class="quiz-option" data-key="' + opt.key + '">' +
        '<span class="quiz-opt-dot"></span><span>' + opt.text + '</span></button>';
    }).join('');
    body.innerHTML =
      '<div class="quiz-step-label">Q' + (qi + 1) + ' / ' + QUESTIONS.length + '</div>' +
      '<div class="quiz-question">' + qData.q + '</div>' +
      '<div class="quiz-options">' + optionsHtml + '</div>';
    body.querySelectorAll('.quiz-option').forEach(function (btn) {
      btn.addEventListener('click', function () {
        answers.push(btn.getAttribute('data-key'));
        current++;
        if (current < QUESTIONS.length) {
          renderQuestion();
        } else {
          renderResult();
        }
      });
    });
  }

  function computeResult() {
    var tally = { A: 0, B: 0, C: 0, D: 0, E: 0 };
    answers.forEach(function (k) { if (tally.hasOwnProperty(k)) tally[k]++; });
    var order = ['A', 'B', 'C', 'D', 'E'];
    var best = 'A';
    var bestCount = -1;
    order.forEach(function (k) {
      if (tally[k] > bestCount) { bestCount = tally[k]; best = k; }
    });
    return best;
  }

  function renderResult() {
    setProgress(totalSteps);
    var key = computeResult();
    var r = RESULTS[key];
    var linksHtml = r.links.map(function (l) {
      return '<a href="' + l.href + '">' + l.text + '<span aria-hidden="true">→</span></a>';
    }).join('');
    body.innerHTML =
      '<div class="quiz-result">' +
        '<div class="quiz-result-img"><img src="' + r.image + '" alt="' + r.title + '" loading="eager"></div>' +
        '<span class="quiz-badge">' + r.badge + '</span>' +
        '<h3>' + r.title + '</h3>' +
        '<div class="quiz-tagline">' + r.tagline + '</div>' +
        '<p class="quiz-desc">' + r.desc + '</p>' +
        '<div class="quiz-result-links">' + linksHtml + '</div>' +
        '<div class="quiz-result-actions">' +
          '<a href="https://lin.ee/NdrFr7t" target="_blank" rel="noopener" class="btn btn-primary">LINEでCAPに相談してみる</a>' +
          '<button type="button" class="quiz-retry" id="quizRetryBtn">もう一度診断する</button>' +
        '</div>' +
      '</div>';
    var retryBtn = document.getElementById('quizRetryBtn');
    if (retryBtn) retryBtn.addEventListener('click', function () { current = 0; answers = []; renderQuestion(); });
  }

  document.querySelectorAll('.js-quiz-open').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      openQuiz();
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeQuiz);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeQuiz();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) closeQuiz();
  });
}
