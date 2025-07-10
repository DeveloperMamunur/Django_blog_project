// Theme Management
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    this.init();
  }

  init() {
    this.applyTheme();
    this.bindEvents();
  }

  applyTheme() {
    document.documentElement.setAttribute('data-theme', this.theme);
    this.updateThemeIcon();
    
    // Force a repaint to ensure theme changes are applied
    document.body.style.display = 'none';
    document.body.offsetHeight; // Trigger reflow
    document.body.style.display = '';
  }

  updateThemeIcon() {
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
      themeIcon.textContent = this.theme === 'dark' ? '☀️' : '🌙';
    }
  }

  toggleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    this.applyTheme();
  }

  bindEvents() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => this.toggleTheme());
    }
  }
}

// Search Functionality
class SearchManager {
  constructor() {
    this.searchInput = document.getElementById('searchInput');
    this.searchBtn = document.getElementById('searchBtn');
    this.blogCards = document.querySelectorAll('.blog-card');
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    if (this.searchInput) {
      this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
      this.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.handleSearch(e.target.value);
        }
      });
    }

    if (this.searchBtn) {
      this.searchBtn.addEventListener('click', () => {
        this.handleSearch(this.searchInput.value);
      });
    }
  }

  handleSearch(query) {
    const searchTerm = query.toLowerCase().trim();
    
    this.blogCards.forEach(card => {
      const title = card.querySelector('.blog-title a').textContent.toLowerCase();
      const excerpt = card.querySelector('.blog-excerpt').textContent.toLowerCase();
      const category = card.querySelector('.blog-category').textContent.toLowerCase();
      
      const isMatch = title.includes(searchTerm) || 
                     excerpt.includes(searchTerm) || 
                     category.includes(searchTerm);
      
      if (searchTerm === '' || isMatch) {
        card.style.display = 'block';
        card.classList.add('fade-in');
      } else {
        card.style.display = 'none';
        card.classList.remove('fade-in');
      }
    });

    // Show "no results" message if needed
    this.showNoResultsMessage(searchTerm);
  }

  showNoResultsMessage(searchTerm) {
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
      existingMessage.remove();
    }

    if (searchTerm && !document.querySelector('.blog-card[style*="block"]')) {
      const blogGrid = document.getElementById('blogGrid');
      const message = document.createElement('div');
      message.className = 'no-results-message';
      message.innerHTML = `
        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
          <h3>No articles found</h3>
          <p>Try searching with different keywords or browse all articles.</p>
        </div>
      `;
      blogGrid.appendChild(message);
    }
  }
}

// Category Filter
class CategoryFilter {
  constructor() {
    this.filterButtons = document.querySelectorAll('.tag-btn');
    this.blogCards = document.querySelectorAll('.blog-card');
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    this.filterButtons.forEach(button => {
      button.addEventListener('click', (e) => this.handleFilter(e.target));
    });
  }

  handleFilter(button) {
    // Update active button
    this.filterButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');

    const category = button.getAttribute('data-category');
    
    // Clear any existing search to avoid conflicts
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.value = '';
    }
    
    // Remove any "no results" messages
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
      existingMessage.remove();
    }
    
    this.blogCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      
      if (category === 'all' || cardCategory === category) {
        card.style.display = 'block';
        card.style.opacity = '0';
        setTimeout(() => {
          card.style.opacity = '1';
          card.classList.add('fade-in');
        }, 50);
      } else {
        card.style.display = 'none';
        card.classList.remove('fade-in');
      }
    });
  }
}

// Mobile Menu
class MobileMenu {
  constructor() {
    this.toggle = document.getElementById('mobileMenuToggle');
    this.menu = document.querySelector('.nav-menu');
    this.isOpen = false;
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    if (this.toggle) {
      this.toggle.addEventListener('click', () => this.toggleMenu());
    }

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (this.isOpen && !this.toggle.contains(e.target) && !this.menu.contains(e.target)) {
        this.closeMenu();
      }
    });

    // Close menu on window resize
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && this.isOpen) {
        this.closeMenu();
      }
    });
  }

  toggleMenu() {
    this.isOpen ? this.closeMenu() : this.openMenu();
  }

  openMenu() {
    this.isOpen = true;
    this.menu.style.display = 'flex';
    this.menu.style.flexDirection = 'column';
    this.menu.style.position = 'absolute';
    this.menu.style.top = '100%';
    this.menu.style.left = '0';
    this.menu.style.right = '0';
    this.menu.style.backgroundColor = 'var(--bg-primary)';
    this.menu.style.border = '1px solid var(--border-color)';
    this.menu.style.borderRadius = 'var(--border-radius)';
    this.menu.style.padding = '1rem';
    this.menu.style.gap = '1rem';
    this.menu.style.zIndex = '1000';
    this.toggle.classList.add('active');
  }

  closeMenu() {
    this.isOpen = false;
    this.menu.style.display = '';
    this.menu.style.flexDirection = '';
    this.menu.style.position = '';
    this.menu.style.top = '';
    this.menu.style.left = '';
    this.menu.style.right = '';
    this.menu.style.backgroundColor = '';
    this.menu.style.border = '';
    this.menu.style.borderRadius = '';
    this.menu.style.padding = '';
    this.menu.style.gap = '';
    this.menu.style.zIndex = '';
    this.toggle.classList.remove('active');
  }

  // Add this method to the MobileMenu class
  updateMenuStyles() {
    if (this.isOpen) {
      this.menu.style.backgroundColor = 'var(--bg-primary)';
      this.menu.style.border = '1px solid var(--border-color)';
    }
  }
}

// Load More Functionality
class LoadMoreManager {
  constructor() {
    this.loadMoreBtn = document.getElementById('loadMoreBtn');
    this.blogGrid = document.getElementById('blogGrid');
    this.articlesPerLoad = 3;
    this.currentArticles = 6; // Initial articles shown
    this.totalArticles = 12; // Total available articles
    this.init();
  }

  init() {
    this.bindEvents();
    this.updateButtonState();
  }

  bindEvents() {
    if (this.loadMoreBtn) {
      this.loadMoreBtn.addEventListener('click', () => this.loadMoreArticles());
    }
  }

  loadMoreArticles() {
    // Simulate loading more articles
    this.loadMoreBtn.textContent = 'Loading...';
    this.loadMoreBtn.disabled = true;

    setTimeout(() => {
      this.addNewArticles();
      this.currentArticles += this.articlesPerLoad;
      this.updateButtonState();
    }, 1000);
  }

  addNewArticles() {
    const newArticles = this.generateNewArticles();
    newArticles.forEach(article => {
      this.blogGrid.appendChild(article);
      article.classList.add('fade-in');
    });
  }

  generateNewArticles() {
    const articles = [];
    const sampleArticles = [
      {
        category: 'technology',
        title: 'Advanced React Patterns for 2025',
        excerpt: 'Explore advanced React patterns and techniques that will make your applications more maintainable...',
        author: 'David Kim',
        date: 'Dec 1, 2024',
        readTime: '6 min read'
      },
      {
        category: 'design',
        title: 'Typography in Web Design: A Complete Guide',
        excerpt: 'Learn how to choose and implement typography that enhances user experience and readability...',
        author: 'Lisa Park',
        date: 'Nov 28, 2024',
        readTime: '8 min read'
      },
      {
        category: 'lifestyle',
        title: 'Remote Work Best Practices for Developers',
        excerpt: 'Tips for staying productive and maintaining work-life balance while working remotely...',
        author: 'Tom Wilson',
        date: 'Nov 25, 2024',
        readTime: '5 min read'
      }
    ];

    for (let i = 0; i < this.articlesPerLoad && articles.length < 3; i++) {
      const articleData = sampleArticles[i];
      const article = this.createArticleElement(articleData);
      articles.push(article);
    }

    return articles;
  }

  createArticleElement(data) {
    const article = document.createElement('article');
    article.className = 'blog-card';
    article.setAttribute('data-category', data.category);
    
    article.innerHTML = `
      <div class="blog-image">
        <img src="/placeholder.svg?height=200&width=400" alt="${data.title}">
      </div>
      <div class="blog-content">
        <div class="blog-meta">
          <span class="blog-category">${data.category.charAt(0).toUpperCase() + data.category.slice(1)}</span>
          <span class="blog-date">${data.date}</span>
        </div>
        <h4 class="blog-title">
          <a href="post.html">${data.title}</a>
        </h4>
        <p class="blog-excerpt">${data.excerpt}</p>
        <div class="blog-footer">
          <div class="author-info">
            <img src="/placeholder.svg?height=32&width=32" alt="${data.author}" class="author-avatar">
            <span class="author-name">${data.author}</span>
          </div>
          <span class="read-time">${data.readTime}</span>
        </div>
      </div>
    `;

    return article;
  }

  updateButtonState() {
    if (this.currentArticles >= this.totalArticles) {
      this.loadMoreBtn.style.display = 'none';
    } else {
      this.loadMoreBtn.textContent = 'Load More Articles';
      this.loadMoreBtn.disabled = false;
    }
  }
}

// Newsletter Subscription
class NewsletterManager {
  constructor() {
    this.forms = document.querySelectorAll('.newsletter-form');
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    this.forms.forEach(form => {
      const button = form.querySelector('.newsletter-btn');
      const input = form.querySelector('.newsletter-input');
      
      if (button && input) {
        button.addEventListener('click', (e) => {
          e.preventDefault();
          this.handleSubscription(input, button);
        });

        input.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            this.handleSubscription(input, button);
          }
        });
      }
    });
  }

  handleSubscription(input, button) {
    const email = input.value.trim();
    
    if (!this.isValidEmail(email)) {
      this.showMessage(input, 'Please enter a valid email address', 'error');
      return;
    }

    button.textContent = 'Subscribing...';
    button.disabled = true;

    // Simulate API call
    setTimeout(() => {
      this.showMessage(input, 'Successfully subscribed!', 'success');
      input.value = '';
      button.textContent = 'Subscribe';
      button.disabled = false;
    }, 1500);
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  showMessage(input, message, type) {
    // Remove existing message
    const existingMessage = input.parentNode.querySelector('.subscription-message');
    if (existingMessage) {
      existingMessage.remove();
    }

    // Create new message
    const messageEl = document.createElement('div');
    messageEl.className = `subscription-message ${type}`;
    messageEl.textContent = message;
    messageEl.style.cssText = `
      margin-top: 0.5rem;
      padding: 0.5rem;
      border-radius: var(--border-radius);
      font-size: 0.875rem;
      background-color: ${type === 'success' ? '#dcfce7' : '#fef2f2'};
      color: ${type === 'success' ? '#166534' : '#dc2626'};
      border: 1px solid ${type === 'success' ? '#bbf7d0' : '#fecaca'};
    `;

    input.parentNode.appendChild(messageEl);

    // Remove message after 3 seconds
    setTimeout(() => {
      if (messageEl.parentNode) {
        messageEl.remove();
      }
    }, 3000);
  }
}

// Share Functionality (for post pages)
class ShareManager {
  constructor() {
    this.shareButtons = document.querySelectorAll('.share-btn');
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    this.shareButtons.forEach(button => {
      button.addEventListener('click', (e) => this.handleShare(e.target));
    });
  }

  handleShare(button) {
    const url = window.location.href;
    const title = document.querySelector('.post-title')?.textContent || document.title;
    
    if (button.classList.contains('twitter')) {
      this.shareToTwitter(url, title);
    } else if (button.classList.contains('linkedin')) {
      this.shareToLinkedIn(url, title);
    } else if (button.classList.contains('facebook')) {
      this.shareToFacebook(url);
    } else if (button.classList.contains('copy-link')) {
      this.copyToClipboard(url, button);
    }
  }

  shareToTwitter(url, title) {
    const twitterUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
    window.open(twitterUrl, '_blank', 'width=600,height=400');
  }

  shareToLinkedIn(url, title) {
    const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    window.open(linkedInUrl, '_blank', 'width=600,height=400');
  }

  shareToFacebook(url) {
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    window.open(facebookUrl, '_blank', 'width=600,height=400');
  }

  copyToClipboard(url, button) {
    navigator.clipboard.writeText(url).then(() => {
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      button.style.backgroundColor = 'var(--accent-color)';
      
      setTimeout(() => {
        button.textContent = originalText;
        button.style.backgroundColor = '';
      }, 2000);
    }).catch(() => {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = url;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      setTimeout(() => {
        button.textContent = originalText;
      }, 2000);
    });
  }
}

// Smooth Scrolling
class SmoothScroll {
  constructor() {
    this.init();
  }

  init() {
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }
}

// Reading Progress (for post pages)
class ReadingProgress {
  constructor() {
    this.progressBar = this.createProgressBar();
    this.init();
  }

  createProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 3px;
      background-color: var(--primary-color);
      z-index: 1000;
      transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    return progressBar;
  }

  init() {
    if (document.querySelector('.post-content')) {
      this.bindEvents();
    } else {
      this.progressBar.style.display = 'none';
    }
  }

  bindEvents() {
    window.addEventListener('scroll', () => this.updateProgress());
  }

  updateProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrollTop = window.pageYOffset;
    const progress = (scrollTop / documentHeight) * 100;
    
    this.progressBar.style.width = `${Math.min(progress, 100)}%`;
  }
}

// Initialize all managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize theme first
  const themeManager = new ThemeManager();
  
  // Then initialize other components
  new SearchManager();
  new CategoryFilter();
  new MobileMenu();
  new LoadMoreManager();
  new NewsletterManager();
  new ShareManager();
  new SmoothScroll();
  new ReadingProgress();
  
  // Add system theme change listener
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      themeManager.theme = e.matches ? 'dark' : 'light';
      themeManager.applyTheme();
    }
  });
});

// Add some utility functions
const utils = {
  // Debounce function for search
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Format date
  formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(new Date(date));
  },

  // Truncate text
  truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
  },

  // Generate reading time
  calculateReadingTime(text) {
    const wordsPerMinute = 200;
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / wordsPerMinute);
    return `${minutes} min read`;
  }
};

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { utils };
}