// blog/js/filter-loader.js
export default class FilterLoader {
    constructor(containerId, loadMoreUrl) {
        this.container = document.getElementById(containerId);
        this.loadMoreUrl = loadMoreUrl;
        this.currentFilter = 'all';
        this.offset = 0;
        this.hasMore = true;
        this.isLoading = false;
        
        // Инициализация
        this.init();
    }
    
    init() {
        // Получаем текущий фильтр из URL
        const urlParams = new URLSearchParams(window.location.search);
        this.currentFilter = urlParams.get('filter') || 'all';
        
        // Добавляем слушатель на кнопки фильтров
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = btn.dataset.filter;
                this.loadFiltered(filter);
            });
        });
    }
    
    async loadFiltered(filter) {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.currentFilter = filter;
        this.offset = 0;
        
        // Показываем загрузку
        const loadingBar = document.getElementById('filterLoading');
        if (loadingBar) loadingBar.classList.add('active');
        
        try {
            const response = await fetch(`${this.loadMoreUrl}?offset=0&filter=${filter}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (data.html) {
                // Анимация исчезновения
                this.container.style.opacity = '0';
                this.container.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    this.container.innerHTML = data.html;
                    this.hasMore = data.has_more;
                    
                    // Анимация появления
                    this.container.style.opacity = '1';
                    this.container.style.transform = 'translateY(0)';
                    
                    // Обновляем анимацию карточек
                    this.animateCards();
                    
                    // Обновляем статистику, если есть функция
                    if (window.updateStats) {
                        window.updateStats();
                    }
                }, 300);
            }
            
        } catch (error) {
            console.error('Filter error:', error);
        } finally {
            this.isLoading = false;
            const loadingBar = document.getElementById('filterLoading');
            if (loadingBar) loadingBar.classList.remove('active');
        }
    }
    
    animateCards() {
        const cards = this.container.querySelectorAll('.card-enter');
        cards.forEach((card, index) => {
            card.style.animation = 'none';
            card.offsetHeight; // reflow
            card.style.animation = `cardFloatIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards`;
            card.style.animationDelay = `${index * 80}ms`;
        });
    }
}