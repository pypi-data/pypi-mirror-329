wiki.theme = {};

wiki.theme.body = document.body;
wiki.theme.html = document.documentElement;

wiki.theme.viewportHeight;
wiki.theme.tableOfContents = document.querySelector('.table-of-contents');
wiki.theme.tableOfContentsContainer = document.querySelector('.columns-table-of-contents');
wiki.theme.tocInViewport = '';
wiki.theme.docsNavigationContainer = document.querySelector('.columns-docs-navigation');
wiki.theme.searchResults = document.getElementById('mkdocs-search-results');
wiki.theme.page404 = document.getElementById('page404');
wiki.theme.mainSection = document.querySelector('.main');
wiki.theme.mainSectionHeight;
wiki.theme.headerSection = document.querySelector('.header');
wiki.theme.sticky = wiki.theme.tableOfContentsContainer.offsetTop;
wiki.theme.stickyController = wiki.theme.mainSection.offsetTop;
wiki.theme.internalLinks = wiki.theme.tableOfContents.querySelectorAll('a');
wiki.theme.contentsEl = document.querySelector('.contents');
wiki.theme.images = wiki.theme.contentsEl.querySelectorAll('img');

wiki.theme.toggleModalImg = function() {
  wiki.theme.body.classList.toggle('show-modal-img');
}

wiki.theme.toggleDocsNav = function() {
  wiki.theme.body.classList.toggle("show-docs-nav");
}

wiki.theme.toggleTocNavChild = function(e) {
  e = e || window.event;
  let targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode;
  let parent = targ.parentElement;
  if (parent.classList.contains("show-nav-child")) {
    parent.classList.remove("show-nav-child");
  } else {
    let tocChildren = document.querySelectorAll('.table-of-contents .has-children');
    tocChildren.forEach(function(tocChild) {
      tocChild.classList.remove("show-nav-child");
    });
    parent.classList.add("show-nav-child");
  }
}

wiki.theme.toggleNavChild = function(e) {
  e = e || window.event;
  let targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode;
  let parent = targ.parentElement;
  parent.classList.toggle("show-nav-child");
}

wiki.theme.isInViewport = function(element) {
  const rect = element.getBoundingClientRect();
  return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight / 4 || document.documentElement.clientHeight / 4) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

wiki.theme.onScroll = function() {
  let scrollValue = window.scrollY || window.scrollTop || document.querySelector('html').scrollTop;
  if (wiki.theme.mainSectionHeight >= (wiki.theme.viewportHeight*2)) {
    if (scrollValue >= wiki.theme.stickyController) {
      wiki.theme.tableOfContentsContainer.classList.add("sticky");
    } else {
      wiki.theme.tableOfContentsContainer.classList.remove("sticky");
    }
    if (scrollValue >= ((wiki.theme.mainSectionHeight + wiki.theme.headerSectionHeight) - wiki.theme.viewportHeight)) {
      wiki.theme.tableOfContentsContainer.classList.add("hide");
    } else {
      wiki.theme.tableOfContentsContainer.classList.remove("hide");
    }
  }

  // Check if .contents h2 and .contents are in the viewport and get their IDs
  document.querySelectorAll('.contents h2, .contents h3').forEach(function(element) {
    if (wiki.theme.isInViewport(element)) {
      wiki.theme.tocInViewport = element.id;
    }
  });

  if (wiki.theme.tocInViewport) {
    document.querySelectorAll('.table-of-contents a').forEach(function(link) {
      link.classList.remove('current');
    });
    let activeLink = document.querySelector('.table-of-contents a[href="#' + wiki.theme.tocInViewport + '"]');
    if (activeLink) {
      activeLink.classList.add('current');
      let toc = document.querySelectorAll('.table-of-contents .has-children');
      toc.forEach(function(tocItem) {
        if (tocItem.querySelector('.current')) {
          tocItem.classList.add('show-nav-child');
        } else {
          tocItem.classList.remove('show-nav-child');
        }
      });
    }
  }
}

wiki.theme.internalLinks.forEach(function(link) {
  link.onclick = function(e) {
    e = e || window.event;
    let targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    let internalLinksHref = targ.getAttribute("href");
    let internalAnchorId = internalLinksHref.replace('#','');
    let titleEl = document.getElementById(internalAnchorId);
    titleEl.classList.add("highlight");
    let parent = targ.parentElement;
    if (parent.classList.contains("has-children")) {
      wiki.theme.toggleTocNavChild(e);
    }
    setTimeout(function(){
      titleEl.classList.remove("highlight");
    }, 1200);
  };
});

/**
 * 
 * Use images title as caption
 */
wiki.theme.images.forEach(function(image) {
  let title = image.getAttribute('title');
  if (title) {
    let imageContainer = image.parentNode;
    let caption = imageContainer.querySelector('figcaption');
    if (!caption) {
      caption = document.createElement('figcaption');
      caption.innerHTML = title;
      imageContainer.insertBefore(caption, image.nextSibling);
    }
  }
  image.onclick = function(e) {
    let targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    e = e || window.event;
    if (targ.alt != "inline-icon") {
      let modal = document.querySelector('.modal');
      modal.classList.add('modal-zoomed-img');
      let contents = [];
      let imgModal = document.createElement('div');
      imgModal.setAttribute('id', 'modal-inner-content-image');
      let src = targ.src;
      let alt = targ.alt;
      let classList = targ.classList;
      imgModal.innerHTML = "<img src='" + src + "' class='" + classList + "' alt='" + alt + "'>";
      contents.push(imgModal);
      let cfg = {
        contents: contents,
        additionalCls: 'show-modal-zoomed-img'
      };
      wiki.modal.buildModal(cfg);      
    }
  };
});

window.addEventListener("scroll", wiki.theme.onScroll);

wiki.theme.body.onresize = function() {
  wiki.theme.viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  wiki.theme.mainSectionHeight = wiki.theme.mainSection.clientHeight;
  wiki.theme.headerSectionHeight = wiki.theme.headerSection.clientHeight;
};

document.addEventListener('DOMContentLoaded', function() {
  wiki.theme.mainSectionHeight = wiki.theme.mainSection.clientHeight;
  wiki.theme.headerSectionHeight = wiki.theme.headerSection.clientHeight;
  wiki.theme.viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  let navChild = document.querySelectorAll('.nav-child');
  navChild.forEach(function(item) {
    let navChildItemActive = item.querySelectorAll('.active');
    if (navChildItemActive.length) {
      item.parentElement.classList.add('show-nav-child');
    }
  });

  if (wiki.theme.page404) {
    wiki.theme.body.classList.add("page-404");
  }
  if (wiki.theme.searchResults) {
    wiki.theme.body.classList.add("search-page");
  }
});
