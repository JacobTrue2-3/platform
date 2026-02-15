import { getAction } from "../../../../static/js/utils.js";
import { formatDatesInHTML } from "../../../../static/js/format-dates.js";


class BatchLoader {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.offset = Number(this.container.dataset.initialOffset);
    this.hasMore = this.container.dataset.hasMore === 'True';
    this.batchSize = Number(this.container.dataset.batchSize);
    this.loadMoreUrl = this.container.dataset.loadMoreUrl;
    this.triggerType = this.container.dataset.triggerType; // scroll или button
    this.loading = false;

    this.init();
  }

  init() {
    if (this.triggerType === 'scroll') {
      window.addEventListener('scroll', () => {
        if ((window.scrollY + window.innerHeight) > (document.documentElement.scrollHeight - 1)) {
          this.loadMore();
        }
      });
    } else if (this.triggerType === 'button') {
      this.loadMoreBtn = document.getElementById(this.container.dataset.loadMoreBtnId);
      if (this.loadMoreBtn) {
        this.loadMoreBtn.addEventListener('click', () => {
          this.loadMore();
        });
      }
    }
  }

  async loadMore() {
    if (this.loading || !this.hasMore) return;

    this.loading = true;
    this.showLoadingSpinner();
    if (this.triggerType === 'button') {
      this.hideLoadMoreButton();
    }

    try {
      const data = await getAction(`${this.loadMoreUrl}?offset=${this.offset}`);

      // Форматируем даты
      const html = formatDatesInHTML(data.html);

      this.container.insertAdjacentHTML("beforeend", html);
      this.offset += this.batchSize;
      this.hasMore = data.has_more;
      
      // Если кнопочная версия и посты ещё есть - возвращаем кнопку
      if (this.triggerType === 'button' && this.hasMore) {
        this.showLoadMoreButton();
      }
    } catch (error) {
      console.error("Ошибка загрузки:", error);
      
      if (this.triggerType === 'button') {
        this.showLoadMoreButton();
      }
    } finally {
      this.loading = false;
      this.hideLoadingSpinner();
    }
  }

  showLoadingSpinner() {
    document.getElementById("loadingSpinner")?.classList.remove("d-none");
  }

  hideLoadingSpinner() {
    document.getElementById("loadingSpinner")?.classList.add("d-none");
  }

  showLoadMoreButton() {
    this.loadMoreBtn.classList.remove("d-none");
  }

  hideLoadMoreButton() {
    this.loadMoreBtn.classList.add("d-none");
  }
}

export default BatchLoader;
