import { postAction } from "../../../../static/js/utils.js";


const postReactionsElement = document.querySelector("#postReactions");

postReactionsElement.addEventListener('click', async (event) => {
  const btnElement = event.target.closest('.js-reaction-btn');
  
  if (!btnElement) return;

  const isAuthenticated = postReactionsElement.dataset.isAuthenticated === 'true';
  const loginUrl = postReactionsElement.dataset.loginUrl;

  if (!isAuthenticated) {
    window.location.href = loginUrl;
    return;
  }

  if (btnElement.classList.contains('disabled')) {
    return;
  }

  const url = btnElement.dataset.url;

  const data = await postAction(url);

  if (!data) return;

  document.querySelector("#likesCount").textContent = data.likes_count;
  document.querySelector("#dislikesCount").textContent = data.dislikes_count;

  const likeBtnElement = document.querySelector('#likeBtn');
  const dislikeBtnElement = document.querySelector('#dislikeBtn');
  const likeIconElement = likeBtnElement.querySelector('i');
  const dislikeIconElement = dislikeBtnElement.querySelector('i');

  if (data.has_liked) {
    likeBtnElement.classList.replace('btn-outline-primary', 'btn-primary');
    likeIconElement.classList.replace('bi-hand-thumbs-up', 'bi-hand-thumbs-up-fill');
  } else {
    likeBtnElement.classList.replace('btn-primary', 'btn-outline-primary');
    likeIconElement.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up');
  }

  if (data.has_disliked) {
    dislikeBtnElement.classList.replace('btn-outline-danger', 'btn-danger');
    dislikeIconElement.classList.replace('bi-hand-thumbs-down', 'bi-hand-thumbs-down-fill');
  } else {
    dislikeBtnElement.classList.replace('btn-danger', 'btn-outline-danger');
    dislikeIconElement.classList.replace('bi-hand-thumbs-down-fill', 'bi-hand-thumbs-down');
  }
});



import { formatDate } from "../../../../static/js/format-dates.js";

const commentFormElement = document.getElementById('commentForm');
commentFormElement.addEventListener('submit', async function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  const url = this.dataset.addCommentUrl;

  // Скрываем предыдущие ошибки
  const commentErrorsElement = document.getElementById('commentErrors');
  commentErrorsElement.classList.add('d-none');
  commentErrorsElement.textContent = '';

  try {
    const data = await postAction(url, formData);

    if (data.success) {
      // Очищаем текстовое поле
      this.querySelector('textarea').value = '';

      // Добавляем новый комментарий в начало списка
      const commentsListElement = document.getElementById('commentsList');
      const emptyMessageElement = commentsListElement.querySelector('#emptyMessage');

      if (emptyMessageElement) {
        emptyMessageElement.remove();
      }

      commentsListElement.insertAdjacentHTML('afterbegin', data.comment_html);
      
      const newCommentElement = commentsListElement.firstElementChild;
      const dateElement = newCommentElement.querySelector('.date-field');
      formatDate(dateElement);

      // Обновляем счетчик комментариев в заголовке
      const commentsTitleElement = document.querySelector('#commentsTitle');
      commentsTitleElement.textContent = `Комментарии (${data.comments_count})`;
    } else {
      // Показываем ошибку
      commentErrorsElement.textContent = data.error;
      commentErrorsElement.classList.remove('d-none');
    }
  } catch (error) {
    console.error('Ошибка при добавлении комментария:', error);
    commentErrorsElement.textContent = 'Произошла ошибка при отправке комментария';
    commentErrorsElement.classList.remove('d-none');
  }
});
