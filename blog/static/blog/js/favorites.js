import { postAction } from "../../../../static/js/utils.js";

// Делегирование событий на контейнере
document.addEventListener('click', async (event) => {
  if (event.target.closest('.favorite-btn')) {
    const favoriteBtnElement = event.target.closest('.favorite-btn');

    const isAuthenticated = favoriteBtnElement.dataset.isAuthenticated === 'true';
    if (!isAuthenticated) {
      window.location.href = favoriteBtnElement.dataset.loginUrl;
      return;
    }

    const url = favoriteBtnElement.dataset.postFavoriteToggleUrl;
    
    const postCardElement = favoriteBtnElement.closest('.post-card');
    const favoriteIconElement = postCardElement.querySelector('.favorite-icon');
    const favoritesCountElement = postCardElement.querySelector('.favorites-count');

    const data = await postAction(url);

    if (data.is_favorite) {
      favoriteIconElement.classList.replace('bi-bookmark', 'bi-bookmark-fill');
    } else {
      favoriteIconElement.classList.replace('bi-bookmark-fill', 'bi-bookmark');
      
      removePostFromFavorites(postCardElement);
    }

    favoritesCountElement.textContent = data.favorites_count;
  }
});

// Функция для проверки, находимся ли на странице избранных
function isFavoritePostsPage() {
    // Проверяем по data-атрибуту
    return document.querySelector('[data-page-type="favorite-posts"]') !== null;
}

// Функция для удаления поста со страницы избранных
function removePostFromFavorites(postCardElement) {
  if (isFavoritePostsPage()) {
    // Удаляем карточку поста
    postCardElement.remove();
    
    // Проверяем, остались ли посты на странице
    const remainingPosts = document.querySelectorAll('.post-card');
    if (remainingPosts.length === 0) {
      showEmptyFavoritesMessage();
    }
  }
}

// Функция для показа сообщения о пустом списке избранных
function showEmptyFavoritesMessage() {
  const container = document.querySelector('.container');
  
  container.innerHTML = '<p class="text-center">Пока нет избранных постов.</p>';
}
