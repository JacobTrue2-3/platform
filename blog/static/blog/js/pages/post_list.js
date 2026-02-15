// blog/js/pages/post_list.js
import BatchLoader from '../batch-loader.js';
import FilterLoader from '../filter-loader.js';

// Инициализируем загрузчик для бесконечного скролла
const batchLoader = new BatchLoader("postsContainer");

// Инициализируем загрузчик фильтров
const filterLoader = new FilterLoader(
    "postsContainer", 
    document.getElementById('postsContainer').dataset.loadMoreUrl
);