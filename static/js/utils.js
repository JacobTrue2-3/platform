function getCookie(cookieKey) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(';');
    
    for (let cookie of cookies) {
      cookie = cookie.trim();

      if (cookie.startsWith(cookieKey + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(cookieKey.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}


export async function getAction(url) {
  const response = await fetch(url);

  if (!response.ok) {
    console.error("Request failed", response.status);
    return null;
  }

  return await response.json();
}


export async function postAction(url, formData = null) {
  const config = {
    method: "POST",
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  };

  // Добавляем body только если передан formData
  if (formData) {
    config.body = formData;
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    console.error("Request failed", response.status)
    return null;
  }

  return await response.json();
}
