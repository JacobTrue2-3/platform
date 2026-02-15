import { getAction } from "../../../../static/js/utils.js";


class InfiniteScroll {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.offset = Number(this.container.dataset.initialOffset);
    this.hasMore = this.container.dataset.hasMore === 'True';
    this.batchSize = Number(this.container.dataset.batchSize);
    this.loadMoreUrl = this.container.dataset.loadMoreUrl;
    this.loading = false;

    this.init();
  }

  init() {
    window.addEventListener('scroll', () => {
      if ((window.scrollY + window.innerHeight) > (document.documentElement.scrollHeight - 1)) {
        this.loadMore();
      }
    });
  }

  async loadMore() {
    if (this.loading || !this.hasMore) return;

    this.loading = true;
    this.showLoadingSpinner();

    try {
      const data = await getAction(`${this.loadMoreUrl}?offset=${this.offset}`);

      this.container.insertAdjacentHTML("beforeend", data.html);
      this.offset += this.batchSize;
      this.hasMore = data.has_more;
    } catch (error) {
      console.error("Ошибка загрузки:", error);
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
}

export default InfiniteScroll;
